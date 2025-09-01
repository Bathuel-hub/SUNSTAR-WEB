#!/usr/bin/env python3
"""
Multiple Image Upload Test Suite for Sun Star International
Tests the new bulk image upload functionality
"""

import asyncio
import aiohttp
import json
import os
import sys
import tempfile
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path
import io

# Test configuration
BACKEND_URL = "https://intl-biz-portal.preview.emergentagent.com/api"
TEST_TIMEOUT = 30

class MultipleImageUploadTester:
    def __init__(self):
        self.session = None
        self.test_results = []
        self.uploaded_files = []  # Track uploaded files for cleanup
        
    async def setup(self):
        """Setup test session"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
        )
        
    async def cleanup(self):
        """Cleanup test session and uploaded files"""
        # Clean up uploaded test files
        for filename in self.uploaded_files:
            try:
                async with self.session.delete(f"{BACKEND_URL}/upload/image/{filename}") as response:
                    if response.status == 200:
                        print(f"Cleaned up test file: {filename}")
            except Exception as e:
                print(f"Failed to cleanup file {filename}: {e}")
        
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, success: bool, message: str, details: Dict = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details:
            for key, value in details.items():
                print(f"    {key}: {value}")
        print()
    
    def create_test_image(self, size_mb: float = 0.1, format: str = "JPEG") -> bytes:
        """Create a test image file in memory"""
        try:
            from PIL import Image
            
            # Calculate dimensions for desired file size
            target_pixels = int((size_mb * 1024 * 1024) * 10 / 3)
            width = height = int(target_pixels ** 0.5)
            
            # Create a simple colored image
            img = Image.new('RGB', (width, height), color='red')
            
            # Save to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format=format, quality=85)
            img_bytes.seek(0)
            
            return img_bytes.getvalue()
        except ImportError:
            # Fallback: create a simple file with repeated data
            target_size = int(size_mb * 1024 * 1024)
            # Create minimal JPEG header + data
            jpeg_header = b'\xff\xd8\xff\xe0\x10JFIF\x01\x01\x01HH'
            jpeg_footer = b'\xff\xd9'
            data_size = target_size - len(jpeg_header) - len(jpeg_footer)
            data = b'A' * max(0, data_size)
            return jpeg_header + data + jpeg_footer
    
    def create_test_text_file(self) -> bytes:
        """Create a test text file"""
        return b"This is a test text file, not an image."
    
    async def test_health_check(self):
        """Test API health check endpoint"""
        try:
            async with self.session.get(f"{BACKEND_URL}/") as response:
                if response.status == 200:
                    data = await response.json()
                    self.log_test(
                        "API Health Check",
                        True,
                        "Backend API is accessible and healthy",
                        {"status_code": response.status, "response": data}
                    )
                    return True
                else:
                    self.log_test(
                        "API Health Check",
                        False,
                        f"Unexpected status code: {response.status}",
                        {"status_code": response.status}
                    )
                    return False
        except Exception as e:
            self.log_test(
                "API Health Check",
                False,
                f"Failed to connect to backend: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    async def test_bulk_upload_valid_images(self):
        """Test uploading multiple valid image files"""
        try:
            # Create 3 test images
            test_images = []
            for i in range(3):
                image_data = self.create_test_image(0.1, "JPEG")
                test_images.append((f'test_bulk_{i+1}.jpg', image_data, 'image/jpeg'))
            
            # Prepare multipart form data
            data = aiohttp.FormData()
            for filename, image_data, content_type in test_images:
                data.add_field('files', image_data, filename=filename, content_type=content_type)
            
            async with self.session.post(f"{BACKEND_URL}/upload/images", data=data) as response:
                response_text = await response.text()
                
                if response.status == 200:
                    try:
                        result = await response.json()
                        if result.get("success") and result.get("data", {}).get("uploaded_files"):
                            uploaded_files = result["data"]["uploaded_files"]
                            upload_count = result["data"]["upload_count"]
                            
                            # Track uploaded files for cleanup
                            for file_info in uploaded_files:
                                filename = file_info.get("filename")
                                if filename:
                                    self.uploaded_files.append(filename)
                            
                            self.log_test(
                                "Bulk Upload Valid Images",
                                True,
                                f"Successfully uploaded {upload_count} images",
                                {
                                    "status_code": response.status,
                                    "upload_count": upload_count,
                                    "total_files": len(test_images),
                                    "uploaded_files": [f["filename"] for f in uploaded_files]
                                }
                            )
                            return True, uploaded_files
                        else:
                            self.log_test(
                                "Bulk Upload Valid Images",
                                False,
                                "Invalid response format",
                                {"response": result}
                            )
                            return False, []
                    except json.JSONDecodeError:
                        self.log_test(
                            "Bulk Upload Valid Images",
                            False,
                            "Invalid JSON response",
                            {"response_text": response_text}
                        )
                        return False, []
                else:
                    self.log_test(
                        "Bulk Upload Valid Images",
                        False,
                        f"HTTP error: {response.status}",
                        {"status_code": response.status, "response": response_text}
                    )
                    return False, []
                    
        except Exception as e:
            self.log_test(
                "Bulk Upload Valid Images",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False, []
    
    async def test_bulk_upload_file_limit(self):
        """Test uploading more than 10 images (should fail)"""
        try:
            # Create 12 test images (exceeds limit of 10)
            test_images = []
            for i in range(12):
                image_data = self.create_test_image(0.05, "JPEG")  # Smaller images
                test_images.append((f'test_limit_{i+1}.jpg', image_data, 'image/jpeg'))
            
            # Prepare multipart form data
            data = aiohttp.FormData()
            for filename, image_data, content_type in test_images:
                data.add_field('files', image_data, filename=filename, content_type=content_type)
            
            async with self.session.post(f"{BACKEND_URL}/upload/images", data=data) as response:
                response_text = await response.text()
                
                # Should return 400 error for exceeding file limit
                if response.status == 400:
                    try:
                        result = await response.json()
                        if "maximum" in result.get("detail", "").lower() or "10" in result.get("detail", ""):
                            self.log_test(
                                "Bulk Upload File Limit",
                                True,
                                "File limit correctly enforced",
                                {
                                    "status_code": response.status,
                                    "error_message": result.get("detail"),
                                    "files_attempted": len(test_images)
                                }
                            )
                            return True
                    except json.JSONDecodeError:
                        pass
                    
                    # Even if JSON decode fails, 400 status is correct
                    self.log_test(
                        "Bulk Upload File Limit",
                        True,
                        "File limit correctly enforced (400 status)",
                        {"status_code": response.status, "response": response_text}
                    )
                    return True
                else:
                    self.log_test(
                        "Bulk Upload File Limit",
                        False,
                        f"Expected 400 error but got {response.status}",
                        {"status_code": response.status, "response": response_text}
                    )
                    return False
                    
        except Exception as e:
            self.log_test(
                "Bulk Upload File Limit",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    async def test_bulk_upload_mixed_files(self):
        """Test uploading mix of valid images and invalid files"""
        try:
            # Create mix of files: 3 valid images + 2 text files
            files_data = []
            
            # Valid images
            for i in range(3):
                image_data = self.create_test_image(0.1, "JPEG")
                files_data.append((f'valid_image_{i+1}.jpg', image_data, 'image/jpeg'))
            
            # Invalid text files
            for i in range(2):
                text_data = self.create_test_text_file()
                files_data.append((f'invalid_file_{i+1}.txt', text_data, 'text/plain'))
            
            # Prepare multipart form data
            data = aiohttp.FormData()
            for filename, file_data, content_type in files_data:
                data.add_field('files', file_data, filename=filename, content_type=content_type)
            
            async with self.session.post(f"{BACKEND_URL}/upload/images", data=data) as response:
                response_text = await response.text()
                
                if response.status == 200:
                    try:
                        result = await response.json()
                        if result.get("success"):
                            uploaded_files = result["data"].get("uploaded_files", [])
                            errors = result["data"].get("errors", [])
                            
                            # Track uploaded files for cleanup
                            for file_info in uploaded_files:
                                filename = file_info.get("filename")
                                if filename:
                                    self.uploaded_files.append(filename)
                            
                            # Should have 3 successful uploads and 2 errors
                            success = len(uploaded_files) == 3 and len(errors) == 2
                            
                            self.log_test(
                                "Bulk Upload Mixed Files",
                                success,
                                f"Processed mixed files: {len(uploaded_files)} uploaded, {len(errors)} errors",
                                {
                                    "status_code": response.status,
                                    "uploaded_count": len(uploaded_files),
                                    "error_count": len(errors),
                                    "errors": errors
                                }
                            )
                            return success, uploaded_files
                        else:
                            self.log_test(
                                "Bulk Upload Mixed Files",
                                False,
                                "Invalid response format",
                                {"response": result}
                            )
                            return False, []
                    except json.JSONDecodeError:
                        self.log_test(
                            "Bulk Upload Mixed Files",
                            False,
                            "Invalid JSON response",
                            {"response_text": response_text}
                        )
                        return False, []
                else:
                    self.log_test(
                        "Bulk Upload Mixed Files",
                        False,
                        f"HTTP error: {response.status}",
                        {"status_code": response.status, "response": response_text}
                    )
                    return False, []
                    
        except Exception as e:
            self.log_test(
                "Bulk Upload Mixed Files",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False, []
    
    async def test_bulk_file_serving(self, uploaded_files: List[Dict]):
        """Test accessing bulk uploaded images via file serving"""
        if not uploaded_files:
            self.log_test(
                "Bulk File Serving",
                False,
                "No uploaded files provided for testing",
                {}
            )
            return False
        
        success_count = 0
        total_files = len(uploaded_files)
        
        for file_info in uploaded_files:
            file_url = file_info.get("file_url")
            filename = file_info.get("filename")
            
            if not file_url or not filename:
                continue
            
            try:
                # Test file serving endpoint
                async with self.session.get(f"{BACKEND_URL}/uploads/{filename}") as response:
                    if response.status == 200:
                        content_type = response.headers.get('content-type', '')
                        if content_type.startswith('image/'):
                            success_count += 1
                            print(f"  ✅ {filename}: Accessible")
                        else:
                            print(f"  ❌ {filename}: Wrong content type - {content_type}")
                    else:
                        print(f"  ❌ {filename}: HTTP {response.status}")
                        
            except Exception as e:
                print(f"  ❌ {filename}: Error - {str(e)}")
        
        success_rate = success_count / total_files if total_files > 0 else 0
        
        self.log_test(
            "Bulk File Serving",
            success_rate >= 0.8,
            f"File serving test: {success_count}/{total_files} files accessible",
            {
                "total_files": total_files,
                "accessible_files": success_count,
                "success_rate": f"{success_rate:.1%}"
            }
        )
        
        return success_rate >= 0.8
    
    async def test_product_creation_multiple_images(self, image_urls: List[str]):
        """Test creating a product with multiple image URLs"""
        if not image_urls:
            self.log_test(
                "Product Creation Multiple Images",
                False,
                "No image URLs provided for product creation test",
                {}
            )
            return False
        
        try:
            product_data = {
                "category_id": "test-category-123",
                "name": "Multi-Image Test Product",
                "description": "This is a test product created with multiple uploaded images for testing the new bulk upload functionality.",
                "price": "Contact for Price",
                "image_urls": image_urls,
                "is_featured": True,
                "is_available": True
            }
            
            async with self.session.post(
                f"{BACKEND_URL}/admin/products",
                json=product_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                response_text = await response.text()
                
                if response.status == 200:
                    try:
                        result = await response.json()
                        if result.get("success") and result.get("data", {}).get("product_id"):
                            self.log_test(
                                "Product Creation Multiple Images",
                                True,
                                "Product created successfully with multiple images",
                                {
                                    "status_code": response.status,
                                    "product_id": result["data"]["product_id"],
                                    "image_count": len(image_urls),
                                    "image_urls": image_urls,
                                    "message": result.get("message")
                                }
                            )
                            return True, result["data"]["product_id"]
                        else:
                            self.log_test(
                                "Product Creation Multiple Images",
                                False,
                                "Invalid response format",
                                {"response": result}
                            )
                            return False, None
                    except json.JSONDecodeError:
                        self.log_test(
                            "Product Creation Multiple Images",
                            False,
                            "Invalid JSON response",
                            {"response_text": response_text}
                        )
                        return False, None
                else:
                    self.log_test(
                        "Product Creation Multiple Images",
                        False,
                        f"HTTP error: {response.status}",
                        {"status_code": response.status, "response": response_text}
                    )
                    return False, None
                    
        except Exception as e:
            self.log_test(
                "Product Creation Multiple Images",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False, None
    
    async def run_all_tests(self):
        """Run all multiple image upload tests"""
        print("🚀 Starting Multiple Image Upload System Tests")
        print("=" * 60)
        
        await self.setup()
        
        try:
            # Test sequence for multiple image upload functionality
            tests = [
                ("API Health Check", self.test_health_check),
                ("Bulk Upload Valid Images", self.test_bulk_upload_valid_images),
                ("Bulk Upload File Limit", self.test_bulk_upload_file_limit),
                ("Bulk Upload Mixed Files", self.test_bulk_upload_mixed_files)
            ]
            
            passed = 0
            total = len(tests)
            bulk_uploaded_files = []
            mixed_uploaded_files = []
            
            for test_name, test_func in tests:
                print(f"Running: {test_name}")
                try:
                    if test_name == "Bulk Upload Valid Images":
                        result, uploaded_files = await test_func()
                        if result:
                            passed += 1
                            bulk_uploaded_files = uploaded_files
                    elif test_name == "Bulk Upload Mixed Files":
                        result, uploaded_files = await test_func()
                        if result:
                            passed += 1
                            mixed_uploaded_files = uploaded_files
                    else:
                        result = await test_func()
                        if result:
                            passed += 1
                except Exception as e:
                    self.log_test(test_name, False, f"Test execution failed: {str(e)}", {"error": str(e)})
                
                print("-" * 40)
            
            # Additional tests that depend on successful bulk uploads
            if bulk_uploaded_files:
                print("Running: Bulk File Serving")
                try:
                    result = await self.test_bulk_file_serving(bulk_uploaded_files)
                    if result:
                        passed += 1
                    total += 1
                except Exception as e:
                    self.log_test("Bulk File Serving", False, f"Test execution failed: {str(e)}", {"error": str(e)})
                    total += 1
                print("-" * 40)
                
                # Extract image URLs for product creation test
                image_urls = [file_info["file_url"] for file_info in bulk_uploaded_files]
                
                print("Running: Product Creation Multiple Images")
                try:
                    result, product_id = await self.test_product_creation_multiple_images(image_urls)
                    if result:
                        passed += 1
                    total += 1
                except Exception as e:
                    self.log_test("Product Creation Multiple Images", False, f"Test execution failed: {str(e)}", {"error": str(e)})
                    total += 1
                print("-" * 40)
            
            # Summary
            print("\n📊 MULTIPLE IMAGE UPLOAD TEST SUMMARY")
            print("=" * 60)
            print(f"Total Tests: {total}")
            print(f"Passed: {passed}")
            print(f"Failed: {total - passed}")
            print(f"Success Rate: {passed/total:.1%}")
            
            if passed == total:
                print("\n🎉 ALL MULTIPLE IMAGE UPLOAD TESTS PASSED! System is working correctly.")
            elif passed >= total * 0.8:
                print("\n⚠️  Most tests passed, but some issues detected.")
            else:
                print("\n❌ Multiple test failures detected. System needs attention.")
            
            return passed, total
            
        finally:
            await self.cleanup()

async def main():
    """Main test execution"""
    print("🔧 Sun Star International Multiple Image Upload Test Suite")
    print("=" * 80)
    
    # Run Multiple Image Upload Tests
    tester = MultipleImageUploadTester()
    try:
        passed, total = await tester.run_all_tests()
        
        # Print detailed results
        print("\n📋 DETAILED TEST RESULTS")
        print("=" * 80)
        
        for result in tester.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['message']}")
            
            if result["details"]:
                for key, value in result["details"].items():
                    print(f"    {key}: {value}")
            print()
        
        # Exit with appropriate code
        sys.exit(0 if passed == total else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Add backend directory to Python path
    sys.path.insert(0, '/app')
    
    # Run tests
    asyncio.run(main())
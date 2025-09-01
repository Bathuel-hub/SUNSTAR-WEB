#!/usr/bin/env python3
"""
Backward Compatibility Test for Single Image Upload using Bulk Endpoint
"""

import asyncio
import aiohttp
import json
import sys
import io
from datetime import datetime

# Test configuration
BACKEND_URL = "https://intl-biz-portal.preview.emergentagent.com/api"
TEST_TIMEOUT = 30

class BackwardCompatibilityTester:
    def __init__(self):
        self.session = None
        self.test_results = []
        self.uploaded_files = []
        
    async def setup(self):
        """Setup test session"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
        )
        
    async def cleanup(self):
        """Cleanup test session and uploaded files"""
        for filename in self.uploaded_files:
            try:
                async with self.session.delete(f"{BACKEND_URL}/upload/image/{filename}") as response:
                    if response.status == 200:
                        print(f"Cleaned up test file: {filename}")
            except Exception as e:
                print(f"Failed to cleanup file {filename}: {e}")
        
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, success: bool, message: str, details: dict = None):
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
            
            target_pixels = int((size_mb * 1024 * 1024) * 10 / 3)
            width = height = int(target_pixels ** 0.5)
            
            img = Image.new('RGB', (width, height), color='blue')
            
            img_bytes = io.BytesIO()
            img.save(img_bytes, format=format, quality=85)
            img_bytes.seek(0)
            
            return img_bytes.getvalue()
        except ImportError:
            # Fallback
            target_size = int(size_mb * 1024 * 1024)
            jpeg_header = b'\xff\xd8\xff\xe0\x10JFIF\x01\x01\x01HH'
            jpeg_footer = b'\xff\xd9'
            data_size = target_size - len(jpeg_header) - len(jpeg_footer)
            data = b'B' * max(0, data_size)
            return jpeg_header + data + jpeg_footer
    
    async def test_single_image_via_bulk_endpoint(self):
        """Test uploading single image using new bulk endpoint"""
        try:
            # Create a single test image
            image_data = self.create_test_image(0.1, "JPEG")
            
            # Prepare multipart form data for bulk endpoint
            data = aiohttp.FormData()
            data.add_field('files', image_data, filename='single_image_test.jpg', content_type='image/jpeg')
            
            async with self.session.post(f"{BACKEND_URL}/upload/images", data=data) as response:
                response_text = await response.text()
                
                if response.status == 200:
                    try:
                        result = await response.json()
                        if result.get("success") and result.get("data", {}).get("uploaded_files"):
                            uploaded_files = result["data"]["uploaded_files"]
                            
                            if len(uploaded_files) == 1:
                                file_info = uploaded_files[0]
                                filename = file_info.get("filename")
                                if filename:
                                    self.uploaded_files.append(filename)
                                
                                self.log_test(
                                    "Single Image via Bulk Endpoint",
                                    True,
                                    "Single image uploaded successfully using bulk endpoint",
                                    {
                                        "status_code": response.status,
                                        "filename": filename,
                                        "file_url": file_info.get("file_url"),
                                        "upload_count": result["data"]["upload_count"]
                                    }
                                )
                                return True, file_info.get("file_url"), filename
                            else:
                                self.log_test(
                                    "Single Image via Bulk Endpoint",
                                    False,
                                    f"Expected 1 file but got {len(uploaded_files)}",
                                    {"uploaded_files": uploaded_files}
                                )
                                return False, None, None
                        else:
                            self.log_test(
                                "Single Image via Bulk Endpoint",
                                False,
                                "Invalid response format",
                                {"response": result}
                            )
                            return False, None, None
                    except json.JSONDecodeError:
                        self.log_test(
                            "Single Image via Bulk Endpoint",
                            False,
                            "Invalid JSON response",
                            {"response_text": response_text}
                        )
                        return False, None, None
                else:
                    self.log_test(
                        "Single Image via Bulk Endpoint",
                        False,
                        f"HTTP error: {response.status}",
                        {"status_code": response.status, "response": response_text}
                    )
                    return False, None, None
                    
        except Exception as e:
            self.log_test(
                "Single Image via Bulk Endpoint",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False, None, None
    
    async def test_old_single_endpoint_removed(self):
        """Test that old single image endpoint returns 404"""
        try:
            image_data = self.create_test_image(0.1, "JPEG")
            
            data = aiohttp.FormData()
            data.add_field('file', image_data, filename='test_old_endpoint.jpg', content_type='image/jpeg')
            
            async with self.session.post(f"{BACKEND_URL}/upload/image", data=data) as response:
                if response.status == 404:
                    self.log_test(
                        "Old Single Endpoint Removed",
                        True,
                        "Old single image endpoint correctly returns 404 (removed as expected)",
                        {"status_code": response.status}
                    )
                    return True
                else:
                    self.log_test(
                        "Old Single Endpoint Removed",
                        False,
                        f"Expected 404 but got {response.status}",
                        {"status_code": response.status}
                    )
                    return False
                    
        except Exception as e:
            self.log_test(
                "Old Single Endpoint Removed",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    async def test_single_image_product_creation(self, image_url: str):
        """Test creating product with single image using new format"""
        if not image_url:
            self.log_test(
                "Single Image Product Creation",
                False,
                "No image URL provided",
                {}
            )
            return False
        
        try:
            product_data = {
                "category_id": "test-category-single",
                "name": "Single Image Test Product",
                "description": "Testing backward compatibility with single image in new format",
                "price": "Contact for Price",
                "image_urls": [image_url],  # Single image in new array format
                "is_featured": False,
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
                                "Single Image Product Creation",
                                True,
                                "Product created successfully with single image in new format",
                                {
                                    "status_code": response.status,
                                    "product_id": result["data"]["product_id"],
                                    "image_url": image_url
                                }
                            )
                            return True
                        else:
                            self.log_test(
                                "Single Image Product Creation",
                                False,
                                "Invalid response format",
                                {"response": result}
                            )
                            return False
                    except json.JSONDecodeError:
                        self.log_test(
                            "Single Image Product Creation",
                            False,
                            "Invalid JSON response",
                            {"response_text": response_text}
                        )
                        return False
                else:
                    self.log_test(
                        "Single Image Product Creation",
                        False,
                        f"HTTP error: {response.status}",
                        {"status_code": response.status, "response": response_text}
                    )
                    return False
                    
        except Exception as e:
            self.log_test(
                "Single Image Product Creation",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    async def run_all_tests(self):
        """Run all backward compatibility tests"""
        print("🚀 Starting Backward Compatibility Tests")
        print("=" * 60)
        
        await self.setup()
        
        try:
            passed = 0
            total = 0
            
            # Test 1: Old endpoint should be removed
            print("Running: Old Single Endpoint Removed")
            result = await self.test_old_single_endpoint_removed()
            if result:
                passed += 1
            total += 1
            print("-" * 40)
            
            # Test 2: Single image via new bulk endpoint
            print("Running: Single Image via Bulk Endpoint")
            result, image_url, filename = await self.test_single_image_via_bulk_endpoint()
            if result:
                passed += 1
            total += 1
            print("-" * 40)
            
            # Test 3: Product creation with single image
            if image_url:
                print("Running: Single Image Product Creation")
                result = await self.test_single_image_product_creation(image_url)
                if result:
                    passed += 1
                total += 1
                print("-" * 40)
            
            # Summary
            print("\n📊 BACKWARD COMPATIBILITY TEST SUMMARY")
            print("=" * 60)
            print(f"Total Tests: {total}")
            print(f"Passed: {passed}")
            print(f"Failed: {total - passed}")
            print(f"Success Rate: {passed/total:.1%}")
            
            if passed == total:
                print("\n🎉 ALL BACKWARD COMPATIBILITY TESTS PASSED!")
                print("✅ Single images can be uploaded using the new bulk endpoint")
                print("✅ Products can be created with single images in new format")
                print("✅ Old endpoint properly removed (no conflicts)")
            elif passed >= total * 0.8:
                print("\n⚠️  Most backward compatibility tests passed")
            else:
                print("\n❌ Backward compatibility issues detected")
            
            return passed, total
            
        finally:
            await self.cleanup()

async def main():
    """Main test execution"""
    print("🔧 Backward Compatibility Test Suite")
    print("=" * 80)
    
    tester = BackwardCompatibilityTester()
    try:
        passed, total = await tester.run_all_tests()
        
        print("\n📋 DETAILED TEST RESULTS")
        print("=" * 80)
        
        for result in tester.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['message']}")
            
            if result["details"]:
                for key, value in result["details"].items():
                    print(f"    {key}: {value}")
            print()
        
        sys.exit(0 if passed == total else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    sys.path.insert(0, '/app')
    asyncio.run(main())
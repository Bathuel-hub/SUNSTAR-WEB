#!/usr/bin/env python3
"""
Backend Test Suite for Sun Star International
Tests the email service integration and file upload functionality
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

class FileUploadTester:
    def __init__(self):
        self.session = None
        self.test_results = []
        self.uploaded_files = []  # Track uploaded files for cleanup
        self.bulk_uploaded_files = []  # Track bulk uploaded files for cleanup
        
    async def setup(self):
        """Setup test session"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
        )
        
    async def cleanup(self):
        """Cleanup test session and uploaded files"""
        # Clean up uploaded test files (single upload)
        for filename in self.uploaded_files:
            try:
                async with self.session.delete(f"{BACKEND_URL}/upload/image/{filename}") as response:
                    if response.status == 200:
                        print(f"Cleaned up test file: {filename}")
            except Exception as e:
                print(f"Failed to cleanup file {filename}: {e}")
        
        # Clean up bulk uploaded test files
        for filename in self.bulk_uploaded_files:
            try:
                async with self.session.delete(f"{BACKEND_URL}/upload/image/{filename}") as response:
                    if response.status == 200:
                        print(f"Cleaned up bulk test file: {filename}")
            except Exception as e:
                print(f"Failed to cleanup bulk file {filename}: {e}")
        
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
            # Rough estimation: JPEG compression ~10:1, RGB = 3 bytes per pixel
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
            jpeg_header = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00'
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
    
    async def test_upload_valid_image(self):
        """Test uploading a valid image file"""
        try:
            # Create a small test image (100KB)
            image_data = self.create_test_image(0.1, "JPEG")
            
            # Prepare multipart form data
            data = aiohttp.FormData()
            data.add_field('file', 
                          image_data, 
                          filename='test_image.jpg', 
                          content_type='image/jpeg')
            
            async with self.session.post(f"{BACKEND_URL}/upload/image", data=data) as response:
                response_text = await response.text()
                
                if response.status == 200:
                    try:
                        result = await response.json()
                        if result.get("success") and result.get("data", {}).get("file_url"):
                            filename = result["data"].get("filename")
                            if filename:
                                self.uploaded_files.append(filename)
                            
                            self.log_test(
                                "Upload Valid Image",
                                True,
                                "Valid image uploaded successfully",
                                {
                                    "status_code": response.status,
                                    "file_url": result["data"]["file_url"],
                                    "filename": result["data"]["filename"],
                                    "file_size": result["data"]["size"]
                                }
                            )
                            return True, result["data"]["file_url"], result["data"]["filename"]
                        else:
                            self.log_test(
                                "Upload Valid Image",
                                False,
                                "Invalid response format",
                                {"response": result}
                            )
                            return False, None, None
                    except json.JSONDecodeError:
                        self.log_test(
                            "Upload Valid Image",
                            False,
                            "Invalid JSON response",
                            {"response_text": response_text}
                        )
                        return False, None, None
                else:
                    self.log_test(
                        "Upload Valid Image",
                        False,
                        f"HTTP error: {response.status}",
                        {"status_code": response.status, "response": response_text}
                    )
                    return False, None, None
                    
        except Exception as e:
            self.log_test(
                "Upload Valid Image",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False, None, None
    
    async def test_upload_invalid_file_type(self):
        """Test uploading a non-image file (should fail)"""
        try:
            # Create a text file
            text_data = self.create_test_text_file()
            
            # Prepare multipart form data
            data = aiohttp.FormData()
            data.add_field('file', 
                          text_data, 
                          filename='test_file.txt', 
                          content_type='text/plain')
            
            async with self.session.post(f"{BACKEND_URL}/upload/image", data=data) as response:
                response_text = await response.text()
                
                # Should return 400 error for invalid file type
                if response.status == 400:
                    try:
                        result = await response.json()
                        if "image" in result.get("detail", "").lower():
                            self.log_test(
                                "Upload Invalid File Type",
                                True,
                                "Non-image file correctly rejected",
                                {
                                    "status_code": response.status,
                                    "error_message": result.get("detail")
                                }
                            )
                            return True
                    except json.JSONDecodeError:
                        pass
                    
                    # Even if JSON decode fails, 400 status is correct
                    self.log_test(
                        "Upload Invalid File Type",
                        True,
                        "Non-image file correctly rejected (400 status)",
                        {"status_code": response.status, "response": response_text}
                    )
                    return True
                else:
                    self.log_test(
                        "Upload Invalid File Type",
                        False,
                        f"Expected 400 error but got {response.status}",
                        {"status_code": response.status, "response": response_text}
                    )
                    return False
                    
        except Exception as e:
            self.log_test(
                "Upload Invalid File Type",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    async def test_upload_oversized_file(self):
        """Test uploading a file over 5MB (should fail)"""
        try:
            # Create a large test image (6MB)
            image_data = self.create_test_image(6.0, "JPEG")
            
            # Prepare multipart form data
            data = aiohttp.FormData()
            data.add_field('file', 
                          image_data, 
                          filename='large_image.jpg', 
                          content_type='image/jpeg')
            
            async with self.session.post(f"{BACKEND_URL}/upload/image", data=data) as response:
                response_text = await response.text()
                
                # Should return 400 error for oversized file
                if response.status == 400:
                    try:
                        result = await response.json()
                        if "5mb" in result.get("detail", "").lower() or "size" in result.get("detail", "").lower():
                            self.log_test(
                                "Upload Oversized File",
                                True,
                                "Oversized file correctly rejected",
                                {
                                    "status_code": response.status,
                                    "error_message": result.get("detail"),
                                    "file_size_mb": len(image_data) / (1024 * 1024)
                                }
                            )
                            return True
                    except json.JSONDecodeError:
                        pass
                    
                    # Even if JSON decode fails, 400 status is correct
                    self.log_test(
                        "Upload Oversized File",
                        True,
                        "Oversized file correctly rejected (400 status)",
                        {
                            "status_code": response.status, 
                            "response": response_text,
                            "file_size_mb": len(image_data) / (1024 * 1024)
                        }
                    )
                    return True
                else:
                    self.log_test(
                        "Upload Oversized File",
                        False,
                        f"Expected 400 error but got {response.status}",
                        {
                            "status_code": response.status, 
                            "response": response_text,
                            "file_size_mb": len(image_data) / (1024 * 1024)
                        }
                    )
                    return False
                    
        except Exception as e:
            self.log_test(
                "Upload Oversized File",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    async def test_static_file_serving(self, file_url: str, filename: str):
        """Test accessing uploaded image via static file serving"""
        if not file_url or not filename:
            self.log_test(
                "Static File Serving",
                False,
                "No file URL provided for testing",
                {}
            )
            return False
        
        try:
            # Construct full URL for static file access
            static_url = f"{BACKEND_URL.replace('/api', '')}{file_url}"
            
            async with self.session.get(static_url) as response:
                if response.status == 200:
                    content_type = response.headers.get('content-type', '')
                    content_length = response.headers.get('content-length', '0')
                    
                    # Verify it's an image
                    if content_type.startswith('image/'):
                        self.log_test(
                            "Static File Serving",
                            True,
                            "Uploaded image accessible via static serving",
                            {
                                "status_code": response.status,
                                "content_type": content_type,
                                "content_length": content_length,
                                "static_url": static_url
                            }
                        )
                        return True
                    else:
                        self.log_test(
                            "Static File Serving",
                            False,
                            f"File accessible but wrong content type: {content_type}",
                            {
                                "status_code": response.status,
                                "content_type": content_type,
                                "static_url": static_url
                            }
                        )
                        return False
                else:
                    self.log_test(
                        "Static File Serving",
                        False,
                        f"File not accessible: HTTP {response.status}",
                        {
                            "status_code": response.status,
                            "static_url": static_url
                        }
                    )
                    return False
                    
        except Exception as e:
            self.log_test(
                "Static File Serving",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e), "static_url": static_url if 'static_url' in locals() else "N/A"}
            )
            return False
    
    async def test_file_deletion(self, filename: str):
        """Test file deletion endpoint"""
        if not filename:
            self.log_test(
                "File Deletion",
                False,
                "No filename provided for deletion test",
                {}
            )
            return False
        
        try:
            async with self.session.delete(f"{BACKEND_URL}/upload/image/{filename}") as response:
                response_text = await response.text()
                
                if response.status == 200:
                    try:
                        result = await response.json()
                        if result.get("success"):
                            # Remove from our tracking list since it's deleted
                            if filename in self.uploaded_files:
                                self.uploaded_files.remove(filename)
                            
                            self.log_test(
                                "File Deletion",
                                True,
                                "File deleted successfully",
                                {
                                    "status_code": response.status,
                                    "filename": filename,
                                    "message": result.get("message")
                                }
                            )
                            return True
                        else:
                            self.log_test(
                                "File Deletion",
                                False,
                                "Deletion response indicates failure",
                                {"response": result}
                            )
                            return False
                    except json.JSONDecodeError:
                        self.log_test(
                            "File Deletion",
                            False,
                            "Invalid JSON response for deletion",
                            {"response_text": response_text}
                        )
                        return False
                elif response.status == 404:
                    self.log_test(
                        "File Deletion",
                        True,
                        "File not found (already deleted or never existed)",
                        {"status_code": response.status, "filename": filename}
                    )
                    return True
                else:
                    self.log_test(
                        "File Deletion",
                        False,
                        f"Unexpected status code: {response.status}",
                        {"status_code": response.status, "response": response_text}
                    )
                    return False
                    
        except Exception as e:
            self.log_test(
                "File Deletion",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    async def test_admin_product_creation_with_image(self, image_url: str):
        """Test creating a product with uploaded image URL"""
        if not image_url:
            self.log_test(
                "Admin Product Creation with Image",
                False,
                "No image URL provided for product creation test",
                {}
            )
            return False
        
        try:
            product_data = {
                "name": "Test Product with Image",
                "description": "This is a test product created with an uploaded image",
                "category": "Test Category",
                "price": "Contact for Price",
                "image_url": image_url,
                "specifications": ["High Quality", "Durable", "Reliable"],
                "availability": "In Stock"
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
                                "Admin Product Creation with Image",
                                True,
                                "Product created successfully with uploaded image",
                                {
                                    "status_code": response.status,
                                    "product_id": result["data"]["product_id"],
                                    "image_url": image_url,
                                    "message": result.get("message")
                                }
                            )
                            return True, result["data"]["product_id"]
                        else:
                            self.log_test(
                                "Admin Product Creation with Image",
                                False,
                                "Invalid response format",
                                {"response": result}
                            )
                            return False, None
                    except json.JSONDecodeError:
                        self.log_test(
                            "Admin Product Creation with Image",
                            False,
                            "Invalid JSON response",
                            {"response_text": response_text}
                        )
                        return False, None
                else:
                    self.log_test(
                        "Admin Product Creation with Image",
                        False,
                        f"HTTP error: {response.status}",
                        {"status_code": response.status, "response": response_text}
                    )
                    return False, None
                    
        except Exception as e:
            self.log_test(
                "Admin Product Creation with Image",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False, None
    
    async def test_multiple_image_formats(self):
        """Test uploading different image formats"""
        formats = [
            ("JPEG", "image/jpeg", ".jpg"),
            ("PNG", "image/png", ".png")
        ]
        
        success_count = 0
        
        for format_name, content_type, extension in formats:
            try:
                # Create test image in specific format
                image_data = self.create_test_image(0.1, format_name)
                
                # Prepare multipart form data
                data = aiohttp.FormData()
                data.add_field('file', 
                              image_data, 
                              filename=f'test_image{extension}', 
                              content_type=content_type)
                
                async with self.session.post(f"{BACKEND_URL}/upload/image", data=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get("success"):
                            filename = result["data"].get("filename")
                            if filename:
                                self.uploaded_files.append(filename)
                            success_count += 1
                            print(f"  ✅ {format_name}: Success")
                        else:
                            print(f"  ❌ {format_name}: Invalid response")
                    else:
                        print(f"  ❌ {format_name}: HTTP {response.status}")
                        
            except Exception as e:
                print(f"  ❌ {format_name}: Error - {str(e)}")
        
        success_rate = success_count / len(formats)
        
        self.log_test(
            "Multiple Image Formats",
            success_rate >= 0.8,
            f"Tested {len(formats)} image formats, {success_count} successful",
            {
                "total_formats": len(formats),
                "successful": success_count,
                "success_rate": f"{success_rate:.1%}"
            }
        )
        
        return success_rate >= 0.8
    
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
                                    self.bulk_uploaded_files.append(filename)
                            
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
                                    self.bulk_uploaded_files.append(filename)
                            
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
    
    async def test_backward_compatibility(self):
        """Test backward compatibility with single image upload"""
        try:
            # Test single image upload endpoint still works
            image_data = self.create_test_image(0.1, "JPEG")
            
            # Prepare multipart form data
            data = aiohttp.FormData()
            data.add_field('file', 
                          image_data, 
                          filename='backward_compat_test.jpg', 
                          content_type='image/jpeg')
            
            async with self.session.post(f"{BACKEND_URL}/upload/image", data=data) as response:
                response_text = await response.text()
                
                if response.status == 200:
                    try:
                        result = await response.json()
                        if result.get("success") and result.get("data", {}).get("file_url"):
                            filename = result["data"].get("filename")
                            if filename:
                                self.uploaded_files.append(filename)
                            
                            # Test creating product with single image_url (legacy format)
                            single_image_url = result["data"]["file_url"]
                            
                            # Test product creation with legacy single image format
                            legacy_product_data = {
                                "category_id": "test-category-legacy",
                                "name": "Legacy Single Image Product",
                                "description": "Testing backward compatibility with single image",
                                "price": "Contact for Price",
                                "image_urls": [single_image_url],  # New format but single image
                                "is_featured": False,
                                "is_available": True
                            }
                            
                            async with self.session.post(
                                f"{BACKEND_URL}/admin/products",
                                json=legacy_product_data,
                                headers={"Content-Type": "application/json"}
                            ) as prod_response:
                                
                                if prod_response.status == 200:
                                    prod_result = await prod_response.json()
                                    if prod_result.get("success"):
                                        self.log_test(
                                            "Backward Compatibility",
                                            True,
                                            "Single image upload and product creation working",
                                            {
                                                "single_upload_status": response.status,
                                                "product_creation_status": prod_response.status,
                                                "product_id": prod_result["data"]["product_id"],
                                                "image_url": single_image_url
                                            }
                                        )
                                        return True
                                    else:
                                        self.log_test(
                                            "Backward Compatibility",
                                            False,
                                            "Product creation failed with single image",
                                            {"product_response": prod_result}
                                        )
                                        return False
                                else:
                                    self.log_test(
                                        "Backward Compatibility",
                                        False,
                                        f"Product creation HTTP error: {prod_response.status}",
                                        {"status_code": prod_response.status}
                                    )
                                    return False
                        else:
                            self.log_test(
                                "Backward Compatibility",
                                False,
                                "Single image upload failed - invalid response",
                                {"response": result}
                            )
                            return False
                    except json.JSONDecodeError:
                        self.log_test(
                            "Backward Compatibility",
                            False,
                            "Single image upload failed - invalid JSON",
                            {"response_text": response_text}
                        )
                        return False
                else:
                    self.log_test(
                        "Backward Compatibility",
                        False,
                        f"Single image upload HTTP error: {response.status}",
                        {"status_code": response.status, "response": response_text}
                    )
                    return False
                    
        except Exception as e:
            self.log_test(
                "Backward Compatibility",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    async def test_complete_image_display_workflow(self):
        """Test the complete image display workflow as requested in review"""
        print("🎯 Testing Complete Image Display Workflow")
        print("=" * 60)
        
        try:
            # Step 1: Upload test images using bulk upload endpoint
            print("Step 1: Uploading test images via bulk upload...")
            success, uploaded_files = await self.test_bulk_upload_valid_images()
            
            if not success or not uploaded_files:
                self.log_test(
                    "Complete Image Display Workflow",
                    False,
                    "Failed at Step 1: Bulk image upload failed",
                    {"step": 1, "uploaded_files": uploaded_files}
                )
                return False
            
            # Extract image URLs for product creation
            image_urls = [file_info["file_url"] for file_info in uploaded_files]
            print(f"✅ Step 1 Complete: Uploaded {len(image_urls)} images")
            
            # Step 2: Create a test product with uploaded images
            print("Step 2: Creating test product with uploaded images...")
            product_success, product_id = await self.test_product_creation_multiple_images(image_urls)
            
            if not product_success or not product_id:
                self.log_test(
                    "Complete Image Display Workflow",
                    False,
                    "Failed at Step 2: Product creation with images failed",
                    {"step": 2, "product_id": product_id, "image_urls": image_urls}
                )
                return False
            
            print(f"✅ Step 2 Complete: Created product {product_id} with {len(image_urls)} images")
            
            # Step 3: Verify product creation shows images in admin panel
            print("Step 3: Verifying product appears in admin products list...")
            admin_products_success = await self.test_admin_products_list_contains_images(product_id, image_urls)
            
            if not admin_products_success:
                self.log_test(
                    "Complete Image Display Workflow",
                    False,
                    "Failed at Step 3: Product not found in admin list or images missing",
                    {"step": 3, "product_id": product_id}
                )
                return False
            
            print(f"✅ Step 3 Complete: Product found in admin list with correct images")
            
            # Step 4: Test image accessibility via URLs
            print("Step 4: Testing image accessibility via URLs...")
            image_access_success = await self.test_bulk_file_serving(uploaded_files)
            
            if not image_access_success:
                self.log_test(
                    "Complete Image Display Workflow",
                    False,
                    "Failed at Step 4: Images not accessible via URLs",
                    {"step": 4, "image_urls": image_urls}
                )
                return False
            
            print(f"✅ Step 4 Complete: All images accessible via URLs")
            
            # All steps successful
            self.log_test(
                "Complete Image Display Workflow",
                True,
                "✅ COMPLETE WORKFLOW SUCCESS: All steps passed - images upload, product creation, admin display, and URL access working",
                {
                    "product_id": product_id,
                    "image_count": len(image_urls),
                    "image_urls": image_urls,
                    "uploaded_files": [f["filename"] for f in uploaded_files],
                    "workflow_steps": "1. Bulk Upload ✅, 2. Product Creation ✅, 3. Admin Display ✅, 4. Image Access ✅"
                }
            )
            return True
            
        except Exception as e:
            self.log_test(
                "Complete Image Display Workflow",
                False,
                f"Workflow failed with exception: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    async def test_admin_products_list_contains_images(self, expected_product_id: str, expected_image_urls: List[str]):
        """Test that admin products list contains the created product with correct images"""
        try:
            async with self.session.get(f"{BACKEND_URL}/admin/products") as response:
                if response.status == 200:
                    products = await response.json()
                    
                    # Find our test product
                    test_product = None
                    for product in products:
                        if product.get("id") == expected_product_id:
                            test_product = product
                            break
                    
                    if not test_product:
                        self.log_test(
                            "Admin Products List Contains Images",
                            False,
                            f"Product {expected_product_id} not found in admin products list",
                            {"expected_product_id": expected_product_id, "total_products": len(products)}
                        )
                        return False
                    
                    # Check if image_urls array is populated correctly
                    product_image_urls = test_product.get("image_urls", [])
                    
                    if not product_image_urls:
                        self.log_test(
                            "Admin Products List Contains Images",
                            False,
                            "Product found but image_urls array is empty",
                            {"product": test_product}
                        )
                        return False
                    
                    # Check if all expected images are present
                    missing_images = []
                    for expected_url in expected_image_urls:
                        if expected_url not in product_image_urls:
                            missing_images.append(expected_url)
                    
                    if missing_images:
                        self.log_test(
                            "Admin Products List Contains Images",
                            False,
                            f"Product found but missing {len(missing_images)} images",
                            {
                                "product_id": expected_product_id,
                                "expected_images": expected_image_urls,
                                "actual_images": product_image_urls,
                                "missing_images": missing_images
                            }
                        )
                        return False
                    
                    # All checks passed
                    self.log_test(
                        "Admin Products List Contains Images",
                        True,
                        f"Product found in admin list with all {len(expected_image_urls)} images correctly stored",
                        {
                            "product_id": expected_product_id,
                            "product_name": test_product.get("name"),
                            "image_count": len(product_image_urls),
                            "image_urls": product_image_urls
                        }
                    )
                    return True
                    
                else:
                    self.log_test(
                        "Admin Products List Contains Images",
                        False,
                        f"Failed to fetch admin products: HTTP {response.status}",
                        {"status_code": response.status}
                    )
                    return False
                    
        except Exception as e:
            self.log_test(
                "Admin Products List Contains Images",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    async def run_image_display_workflow_test(self):
        """Run the specific image display workflow test as requested in review"""
        print("🎯 Starting Image Display Workflow Test")
        print("=" * 60)
        
        await self.setup()
        
        try:
            # First ensure API is healthy
            health_check = await self.test_health_check()
            if not health_check:
                print("❌ API Health Check failed - cannot proceed with workflow test")
                return False
            
            # Run the complete workflow test
            workflow_success = await self.test_complete_image_display_workflow()
            
            # Summary
            print("\n📊 IMAGE DISPLAY WORKFLOW TEST SUMMARY")
            print("=" * 60)
            
            if workflow_success:
                print("🎉 ✅ IMAGE DISPLAY WORKFLOW TEST PASSED!")
                print("   - Bulk image upload working")
                print("   - Product creation with multiple images working")
                print("   - Admin products list showing images correctly")
                print("   - Image URLs accessible and serving files")
                print("   - Store page should now display images correctly")
                return True
            else:
                print("❌ IMAGE DISPLAY WORKFLOW TEST FAILED!")
                print("   - Check individual test results above for details")
                return False
            
        finally:
            await self.cleanup()

    async def run_file_upload_tests(self):
        """Run all file upload tests"""
        print("🚀 Starting File Upload System Tests")
        print("=" * 60)
        
        await self.setup()
        
        try:
            # Test sequence for file upload functionality
            tests = [
                ("API Health Check", self.test_health_check),
                ("Upload Valid Image", self.test_upload_valid_image),
                ("Upload Invalid File Type", self.test_upload_invalid_file_type),
                ("Upload Oversized File", self.test_upload_oversized_file),
                ("Multiple Image Formats", self.test_multiple_image_formats)
            ]
            
            passed = 0
            total = len(tests)
            uploaded_file_url = None
            uploaded_filename = None
            
            for test_name, test_func in tests:
                print(f"Running: {test_name}")
                try:
                    if test_name == "Upload Valid Image":
                        result, file_url, filename = await test_func()
                        if result:
                            passed += 1
                            uploaded_file_url = file_url
                            uploaded_filename = filename
                    else:
                        result = await test_func()
                        if result:
                            passed += 1
                except Exception as e:
                    self.log_test(test_name, False, f"Test execution failed: {str(e)}", {"error": str(e)})
                
                print("-" * 40)
            
            # Additional tests that depend on successful upload
            if uploaded_file_url and uploaded_filename:
                print("Running: Static File Serving")
                try:
                    result = await self.test_static_file_serving(uploaded_file_url, uploaded_filename)
                    if result:
                        passed += 1
                    total += 1
                except Exception as e:
                    self.log_test("Static File Serving", False, f"Test execution failed: {str(e)}", {"error": str(e)})
                    total += 1
                print("-" * 40)
                
                print("Running: Admin Product Creation with Image")
                try:
                    result, product_id = await self.test_admin_product_creation_with_image(uploaded_file_url)
                    if result:
                        passed += 1
                    total += 1
                except Exception as e:
                    self.log_test("Admin Product Creation with Image", False, f"Test execution failed: {str(e)}", {"error": str(e)})
                    total += 1
                print("-" * 40)
                
                print("Running: File Deletion")
                try:
                    result = await self.test_file_deletion(uploaded_filename)
                    if result:
                        passed += 1
                    total += 1
                except Exception as e:
                    self.log_test("File Deletion", False, f"Test execution failed: {str(e)}", {"error": str(e)})
                    total += 1
                print("-" * 40)
            
            # Summary
            print("\n📊 FILE UPLOAD TEST SUMMARY")
            print("=" * 60)
            print(f"Total Tests: {total}")
            print(f"Passed: {passed}")
            print(f"Failed: {total - passed}")
            print(f"Success Rate: {passed/total:.1%}")
            
            if passed == total:
                print("\n🎉 ALL FILE UPLOAD TESTS PASSED! File upload system is working correctly.")
            elif passed >= total * 0.8:
                print("\n⚠️  Most file upload tests passed, but some issues detected.")
            else:
                print("\n❌ Multiple file upload test failures detected. System needs attention.")
            
            return passed, total
            
        finally:
            await self.cleanup()


class EmailServiceTester:
    def __init__(self):
        self.session = None
        self.test_results = []
        
    async def setup(self):
        """Setup test session"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
        )
        
    async def cleanup(self):
        """Cleanup test session"""
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
    
    async def test_contact_inquiry_basic(self):
        """Test basic contact inquiry submission"""
        test_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "company": "Test Company Ltd",
            "inquiry_type": "Product Inquiry",
            "message": "I'm interested in your automotive parts catalog. Please send me more information about brake pads and engine components."
        }
        
        try:
            async with self.session.post(
                f"{BACKEND_URL}/contact/inquiry",
                json=test_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                response_text = await response.text()
                
                if response.status == 200:
                    try:
                        data = await response.json()
                        if data.get("success") and data.get("data", {}).get("inquiry_id"):
                            self.log_test(
                                "Contact Inquiry Basic",
                                True,
                                "Contact inquiry submitted successfully",
                                {
                                    "status_code": response.status,
                                    "inquiry_id": data["data"]["inquiry_id"],
                                    "message": data.get("message", "")
                                }
                            )
                            return True
                        else:
                            self.log_test(
                                "Contact Inquiry Basic",
                                False,
                                "Invalid response format",
                                {"response": data}
                            )
                            return False
                    except json.JSONDecodeError:
                        self.log_test(
                            "Contact Inquiry Basic",
                            False,
                            "Invalid JSON response",
                            {"response_text": response_text}
                        )
                        return False
                else:
                    self.log_test(
                        "Contact Inquiry Basic",
                        False,
                        f"HTTP error: {response.status}",
                        {"status_code": response.status, "response": response_text}
                    )
                    return False
                    
        except Exception as e:
            self.log_test(
                "Contact Inquiry Basic",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    async def test_different_inquiry_types(self):
        """Test different inquiry types"""
        inquiry_types = [
            "General",
            "Product Inquiry", 
            "Partnership",
            "Technical Support",
            "Pricing Information"
        ]
        
        success_count = 0
        
        for inquiry_type in inquiry_types:
            test_data = {
                "name": f"Test Customer {inquiry_type}",
                "email": f"test.{inquiry_type.lower().replace(' ', '')}@example.com",
                "phone": "+971551234567",
                "company": f"{inquiry_type} Testing Co.",
                "inquiry_type": inquiry_type,
                "message": f"This is a test message for {inquiry_type} inquiry type. Please process this request accordingly."
            }
            
            try:
                async with self.session.post(
                    f"{BACKEND_URL}/contact/inquiry",
                    json=test_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        if data.get("success"):
                            success_count += 1
                            print(f"  ✅ {inquiry_type}: Success")
                        else:
                            print(f"  ❌ {inquiry_type}: Invalid response")
                    else:
                        print(f"  ❌ {inquiry_type}: HTTP {response.status}")
                        
            except Exception as e:
                print(f"  ❌ {inquiry_type}: Error - {str(e)}")
        
        success_rate = success_count / len(inquiry_types)
        
        self.log_test(
            "Different Inquiry Types",
            success_rate >= 0.8,  # 80% success rate required
            f"Tested {len(inquiry_types)} inquiry types, {success_count} successful",
            {
                "total_types": len(inquiry_types),
                "successful": success_count,
                "success_rate": f"{success_rate:.1%}"
            }
        )
        
        return success_rate >= 0.8
    
    async def test_validation_errors(self):
        """Test validation and error handling"""
        test_cases = [
            {
                "name": "Missing Required Fields",
                "data": {"name": "Test"},
                "expected_error": True
            },
            {
                "name": "Invalid Email Format",
                "data": {
                    "name": "Test User",
                    "email": "invalid-email",
                    "inquiry_type": "General",
                    "message": "Test message"
                },
                "expected_error": True
            },
            {
                "name": "Empty Message",
                "data": {
                    "name": "Test User",
                    "email": "test@example.com",
                    "inquiry_type": "General",
                    "message": ""
                },
                "expected_error": True
            }
        ]
        
        success_count = 0
        
        for test_case in test_cases:
            try:
                async with self.session.post(
                    f"{BACKEND_URL}/contact/inquiry",
                    json=test_case["data"],
                    headers={"Content-Type": "application/json"}
                ) as response:
                    
                    # For validation errors, we expect 4xx status codes
                    if test_case["expected_error"]:
                        if response.status >= 400:
                            success_count += 1
                            print(f"  ✅ {test_case['name']}: Correctly rejected (HTTP {response.status})")
                        else:
                            print(f"  ❌ {test_case['name']}: Should have been rejected but got HTTP {response.status}")
                    else:
                        if response.status == 200:
                            success_count += 1
                            print(f"  ✅ {test_case['name']}: Correctly accepted")
                        else:
                            print(f"  ❌ {test_case['name']}: Should have been accepted but got HTTP {response.status}")
                            
            except Exception as e:
                print(f"  ❌ {test_case['name']}: Error - {str(e)}")
        
        success_rate = success_count / len(test_cases)
        
        self.log_test(
            "Validation & Error Handling",
            success_rate >= 0.8,
            f"Tested {len(test_cases)} validation cases, {success_count} handled correctly",
            {
                "total_cases": len(test_cases),
                "correct_handling": success_count,
                "success_rate": f"{success_rate:.1%}"
            }
        )
        
        return success_rate >= 0.8
    
    async def test_email_service_configuration(self):
        """Test email service configuration"""
        try:
            # Check if email password is configured
            from backend.email_service import email_service
            
            has_password = bool(email_service.sender_password)
            correct_sender = email_service.sender_email == "sunstarintl.ae@gmail.com"
            correct_recipient = email_service.recipient_email == "sunstarintl.ae@gmail.com"
            correct_smtp = email_service.smtp_server == "smtp.gmail.com"
            
            all_correct = has_password and correct_sender and correct_recipient and correct_smtp
            
            self.log_test(
                "Email Service Configuration",
                all_correct,
                "Email service configuration validated",
                {
                    "has_password": has_password,
                    "sender_email": email_service.sender_email,
                    "recipient_email": email_service.recipient_email,
                    "smtp_server": email_service.smtp_server,
                    "smtp_port": email_service.smtp_port
                }
            )
            
            return all_correct
            
        except Exception as e:
            self.log_test(
                "Email Service Configuration",
                False,
                f"Failed to check email configuration: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    async def test_email_template_generation(self):
        """Test email template generation"""
        try:
            from backend.email_service import email_service
            
            # Test data for template
            test_inquiry_data = {
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '+1234567890',
                'company': 'Test Company Ltd',
                'inquiry_type': 'Product Inquiry',
                'message': 'Test message for email template',
                'submitted_at': '2025-01-27 10:30:00 UTC',
                'ip_address': '192.168.1.1'
            }
            
            # Generate HTML template
            html_content = email_service.create_contact_email_html(test_inquiry_data)
            
            # Basic validation of HTML content
            required_elements = [
                'New Customer Inquiry',
                'John Doe',
                'john.doe@example.com',
                'Product Inquiry',
                'Test message for email template',
                'Sun Star International'
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in html_content:
                    missing_elements.append(element)
            
            template_valid = len(missing_elements) == 0
            
            self.log_test(
                "Email Template Generation",
                template_valid,
                "Email HTML template generated successfully" if template_valid else f"Missing elements: {missing_elements}",
                {
                    "template_length": len(html_content),
                    "has_html_structure": "<html>" in html_content and "</html>" in html_content,
                    "has_table": "<table" in html_content,
                    "missing_elements": missing_elements
                }
            )
            
            return template_valid
            
        except Exception as e:
            self.log_test(
                "Email Template Generation",
                False,
                f"Failed to generate email template: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    async def test_comprehensive_email_flow(self):
        """Test complete email flow with realistic data"""
        test_data = {
            "name": "Ahmed Al-Mansouri",
            "email": "ahmed.mansouri@constructionco.ae",
            "phone": "+971501234567",
            "company": "Al-Mansouri Construction LLC",
            "inquiry_type": "Partnership",
            "message": "We are interested in establishing a long-term partnership for heavy equipment supply. Our company specializes in large-scale construction projects across the UAE and we require reliable suppliers for excavators, bulldozers, and related machinery. Please provide information about your product range, pricing structure, and delivery capabilities."
        }
        
        try:
            async with self.session.post(
                f"{BACKEND_URL}/contact/inquiry",
                json=test_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    
                    # Wait a moment for background email task
                    await asyncio.sleep(2)
                    
                    self.log_test(
                        "Comprehensive Email Flow",
                        True,
                        "Complete email flow test successful",
                        {
                            "status_code": response.status,
                            "inquiry_id": data.get("data", {}).get("inquiry_id"),
                            "message": data.get("message"),
                            "email_should_be_sent": "Check backend logs for email confirmation"
                        }
                    )
                    return True
                else:
                    response_text = await response.text()
                    self.log_test(
                        "Comprehensive Email Flow",
                        False,
                        f"HTTP error: {response.status}",
                        {"status_code": response.status, "response": response_text}
                    )
                    return False
                    
        except Exception as e:
            self.log_test(
                "Comprehensive Email Flow",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    async def run_all_tests(self):
        """Run all email service tests"""
        print("🚀 Starting Email Service Integration Tests")
        print("=" * 60)
        
        await self.setup()
        
        try:
            # Test sequence
            tests = [
                ("API Health Check", self.test_health_check),
                ("Email Service Configuration", self.test_email_service_configuration),
                ("Email Template Generation", self.test_email_template_generation),
                ("Contact Inquiry Basic", self.test_contact_inquiry_basic),
                ("Different Inquiry Types", self.test_different_inquiry_types),
                ("Validation & Error Handling", self.test_validation_errors),
                ("Comprehensive Email Flow", self.test_comprehensive_email_flow)
            ]
            
            passed = 0
            total = len(tests)
            
            for test_name, test_func in tests:
                print(f"Running: {test_name}")
                try:
                    result = await test_func()
                    if result:
                        passed += 1
                except Exception as e:
                    self.log_test(test_name, False, f"Test execution failed: {str(e)}", {"error": str(e)})
                
                print("-" * 40)
            
            # Summary
            print("\n📊 TEST SUMMARY")
            print("=" * 60)
            print(f"Total Tests: {total}")
            print(f"Passed: {passed}")
            print(f"Failed: {total - passed}")
            print(f"Success Rate: {passed/total:.1%}")
            
            if passed == total:
                print("\n🎉 ALL TESTS PASSED! Email service is working correctly.")
            elif passed >= total * 0.8:
                print("\n⚠️  Most tests passed, but some issues detected.")
            else:
                print("\n❌ Multiple test failures detected. Email service needs attention.")
            
            return passed, total
            
        finally:
            await self.cleanup()

async def main():
    """Main test execution with workflow option"""
    import sys
    
    # Check for workflow test argument
    if len(sys.argv) > 1 and sys.argv[1].lower() == "workflow":
        print("🎯 Running Image Display Workflow Test (as requested in review)")
        print("=" * 80)
        
        tester = FileUploadTester()
        success = await tester.run_image_display_workflow_test()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
    
    # Default: Run all tests
    print("🔧 Sun Star International Backend Test Suite")
    print("=" * 80)
    
    # Run File Upload Tests
    file_tester = FileUploadTester()
    try:
        file_passed, file_total = await file_tester.run_file_upload_tests()
        
        print("\n" + "=" * 80)
        
        # Run Email Service Tests
        email_tester = EmailServiceTester()
        email_passed, email_total = await email_tester.run_all_tests()
        
        # Combined Summary
        total_passed = file_passed + email_passed
        total_tests = file_total + email_total
        
        print("\n🎯 OVERALL TEST SUMMARY")
        print("=" * 80)
        print(f"File Upload Tests: {file_passed}/{file_total} passed")
        print(f"Email Service Tests: {email_passed}/{email_total} passed")
        print(f"Total Tests: {total_passed}/{total_tests} passed")
        print(f"Overall Success Rate: {total_passed/total_tests:.1%}")
        
        # Print detailed results
        print("\n📋 DETAILED TEST RESULTS")
        print("=" * 80)
        
        print("\n🔧 File Upload Test Results:")
        for result in file_tester.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['message']}")
            
            if result["details"]:
                for key, value in result["details"].items():
                    print(f"    {key}: {value}")
            print()
        
        print("\n📧 Email Service Test Results:")
        for result in email_tester.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['message']}")
            
            if result["details"]:
                for key, value in result["details"].items():
                    print(f"    {key}: {value}")
            print()
        
        # Exit with appropriate code
        sys.exit(0 if total_passed == total_tests else 1)
        
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
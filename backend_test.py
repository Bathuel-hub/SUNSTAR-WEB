#!/usr/bin/env python3
"""
Backend Test Suite for Sun Star International Email Service Integration
Tests the contact form email functionality and API endpoints
"""

import asyncio
import aiohttp
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, List

# Test configuration
BACKEND_URL = "https://intl-biz-portal.preview.emergentagent.com/api"
TEST_TIMEOUT = 30

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
    """Main test execution"""
    tester = EmailServiceTester()
    
    try:
        passed, total = await tester.run_all_tests()
        
        # Print detailed results
        print("\n📋 DETAILED TEST RESULTS")
        print("=" * 60)
        
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
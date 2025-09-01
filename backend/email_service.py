import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        # For now, we'll use a simple SMTP setup
        # In production, you'd want to use services like SendGrid, Mailgun, etc.
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "sunstarintl.ae@gmail.com"
        self.sender_password = os.environ.get("EMAIL_PASSWORD", "")
        self.recipient_email = "sunstarintl.ae@gmail.com"
    
    def create_contact_email_html(self, inquiry_data):
        """Create beautifully formatted HTML email with table"""
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>New Contact Inquiry - Sun Star International</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                }
                .header {
                    background: linear-gradient(135deg, #dc2626, #f59e0b);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }
                .header h1 {
                    margin: 0;
                    font-size: 24px;
                    font-weight: 600;
                }
                .header p {
                    margin: 10px 0 0 0;
                    opacity: 0.9;
                }
                .content {
                    padding: 30px;
                }
                .inquiry-table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    background-color: white;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }
                .inquiry-table th {
                    background-color: #f8f9fa;
                    color: #495057;
                    font-weight: 600;
                    padding: 15px;
                    text-align: left;
                    border-bottom: 2px solid #dee2e6;
                    width: 30%;
                }
                .inquiry-table td {
                    padding: 15px;
                    border-bottom: 1px solid #dee2e6;
                    vertical-align: top;
                }
                .inquiry-table tr:last-child td {
                    border-bottom: none;
                }
                .inquiry-table tr:nth-child(even) {
                    background-color: #f8f9fa;
                }
                .message-cell {
                    background-color: #fff3cd !important;
                    border-left: 4px solid #f59e0b;
                }
                .priority-high {
                    background-color: #fee2e2 !important;
                    border-left: 4px solid #dc2626;
                }
                .badge {
                    display: inline-block;
                    padding: 4px 12px;
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: 600;
                    text-transform: uppercase;
                }
                .badge-new {
                    background-color: #10b981;
                    color: white;
                }
                .badge-urgent {
                    background-color: #dc2626;
                    color: white;
                }
                .footer {
                    background-color: #f8f9fa;
                    padding: 20px 30px;
                    text-align: center;
                    border-top: 1px solid #dee2e6;
                }
                .footer p {
                    margin: 0;
                    color: #6c757d;
                    font-size: 14px;
                }
                .action-buttons {
                    margin: 20px 0;
                    text-align: center;
                }
                .btn {
                    display: inline-block;
                    padding: 12px 24px;
                    margin: 0 10px;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 14px;
                }
                .btn-primary {
                    background-color: #dc2626;
                    color: white;
                }
                .btn-secondary {
                    background-color: #f59e0b;
                    color: white;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌟 New Customer Inquiry</h1>
                    <p>Sun Star International FZ-LLC</p>
                    <span class="badge badge-new">New Inquiry</span>
                </div>
                
                <div class="content">
                    <h2 style="color: #dc2626; margin-top: 0;">Contact Form Submission</h2>
                    
                    <table class="inquiry-table">
                        <tr>
                            <th>👤 Customer Name</th>
                            <td><strong>{{ name }}</strong></td>
                        </tr>
                        <tr>
                            <th>📧 Email Address</th>
                            <td><a href="mailto:{{ email }}">{{ email }}</a></td>
                        </tr>
                        <tr>
                            <th>📞 Phone Number</th>
                            <td>
                                {% if phone %}
                                    <a href="tel:{{ phone }}">{{ phone }}</a>
                                {% else %}
                                    <em style="color: #6c757d;">Not provided</em>
                                {% endif %}
                            </td>
                        </tr>
                        <tr>
                            <th>🏢 Company</th>
                            <td>
                                {% if company %}
                                    <strong>{{ company }}</strong>
                                {% else %}
                                    <em style="color: #6c757d;">Not provided</em>
                                {% endif %}
                            </td>
                        </tr>
                        <tr>
                            <th>🎯 Inquiry Type</th>
                            <td>
                                <span class="badge" style="background-color: #dc2626; color: white;">
                                    {{ inquiry_type | title }}
                                </span>
                            </td>
                        </tr>
                        <tr class="priority-high">
                            <th>💬 Customer Message</th>
                            <td class="message-cell">
                                <div style="white-space: pre-wrap; font-family: 'Courier New', monospace; background-color: white; padding: 15px; border-radius: 6px; border: 1px solid #dee2e6;">{{ message }}</div>
                            </td>
                        </tr>
                        <tr>
                            <th>🕐 Submitted On</th>
                            <td><strong>{{ submitted_at }}</strong></td>
                        </tr>
                        <tr>
                            <th>🌐 IP Address</th>
                            <td><code style="background-color: #f8f9fa; padding: 2px 6px; border-radius: 4px;">{{ ip_address }}</code></td>
                        </tr>
                    </table>
                    
                    <div class="action-buttons">
                        <a href="mailto:{{ email }}?subject=Re: Your inquiry about {{ inquiry_type }}" class="btn btn-primary">
                            📧 Reply to Customer
                        </a>
                        <a href="tel:{{ phone }}" class="btn btn-secondary">
                            📞 Call Customer
                        </a>
                    </div>
                </div>
                
                <div class="footer">
                    <p><strong>Sun Star International FZ-LLC</strong></p>
                    <p>License No: 5034384 | RAKEZ Licensed | RAK UAE</p>
                    <p><em>This inquiry was submitted through your website contact form.</em></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        template = Template(html_template)
        
        return template.render(
            name=inquiry_data.get('name', 'Unknown'),
            email=inquiry_data.get('email', 'No email provided'),
            phone=inquiry_data.get('phone', ''),
            company=inquiry_data.get('company', ''),
            inquiry_type=inquiry_data.get('inquiry_type', 'General'),
            message=inquiry_data.get('message', 'No message provided'),
            submitted_at=inquiry_data.get('submitted_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')),
            ip_address=inquiry_data.get('ip_address', 'Unknown')
        )
    
    async def send_contact_email(self, inquiry):
        """Send the contact form email"""
        try:
            # Prepare inquiry data
            inquiry_data = {
                'name': inquiry.name,
                'email': inquiry.email,
                'phone': inquiry.phone,
                'company': inquiry.company,
                'inquiry_type': inquiry.inquiry_type,
                'message': inquiry.message,
                'submitted_at': inquiry.created_at.strftime('%Y-%m-%d %H:%M:%S UTC'),
                'ip_address': inquiry.ip_address
            }
            
            # Create HTML email
            html_content = self.create_contact_email_html(inquiry_data)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"🌟 New Customer Inquiry - {inquiry.inquiry_type.title()} - {inquiry.name}"
            
            # Attach HTML
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email via Gmail SMTP
            if self.sender_password:
                logger.info(f"📧 Sending email to {self.recipient_email}")
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
                server.quit()
                logger.info("✅ Email sent successfully!")
                return True
            else:
                logger.warning("⚠️ EMAIL_PASSWORD not set - email not sent")
                return False
            
        except Exception as e:
            logger.error(f"❌ Failed to send email: {e}")
            return False

# Create global instance
email_service = EmailService()
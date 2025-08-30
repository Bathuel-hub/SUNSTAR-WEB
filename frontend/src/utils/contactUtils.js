// Utility functions for contact interactions

export const contactActions = {
  // WhatsApp contact
  openWhatsApp: (phoneNumber, message = '') => {
    const cleanPhone = phoneNumber.replace(/[^\d+]/g, '');
    const encodedMessage = encodeURIComponent(message);
    const whatsappUrl = `https://wa.me/${cleanPhone}?text=${encodedMessage}`;
    window.open(whatsappUrl, '_blank');
  },

  // Phone call
  makeCall: (phoneNumber) => {
    const cleanPhone = phoneNumber.replace(/[^\d+]/g, '');
    window.location.href = `tel:${cleanPhone}`;
  },

  // Email
  sendEmail: (emailAddress, subject = '', body = '') => {
    const encodedSubject = encodeURIComponent(subject);
    const encodedBody = encodeURIComponent(body);
    const emailUrl = `mailto:${emailAddress}?subject=${encodedSubject}&body=${encodedBody}`;
    window.location.href = emailUrl;
  },

  // Request quote email with pre-filled content
  requestQuote: (companyEmail, productType = '') => {
    const subject = `Quote Request from ${window.location.hostname}`;
    const body = `Hello Sun Star International,

I am interested in requesting a quote for ${productType || 'your products/services'}.

Please provide me with:
- Product specifications
- Pricing information  
- Delivery timeframe
- Payment terms

Company Details:
- Company Name: [Please fill]
- Contact Person: [Please fill]
- Phone: [Please fill]
- Location: [Please fill]

Thank you for your time.

Best regards,
[Your Name]`;

    contactActions.sendEmail(companyEmail, subject, body);
  },

  // General inquiry email
  contactUs: (companyEmail) => {
    const subject = `General Inquiry from ${window.location.hostname}`;
    const body = `Hello Sun Star International,

I would like to inquire about your services.

[Please describe your inquiry here]

Best regards,
[Your Name]
[Your Contact Information]`;

    contactActions.sendEmail(companyEmail, subject, body);
  }
};

export default contactActions;
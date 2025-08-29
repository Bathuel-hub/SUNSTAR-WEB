import React, { useState } from 'react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { Label } from '../components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Badge } from '../components/ui/badge';
import { 
  Phone, Mail, MapPin, Clock, MessageCircle, 
  Send, Building2, Globe, Headphones, Loader2, CheckCircle
} from 'lucide-react';
import { useCompanyInfo } from '../hooks/useApi';
import { api } from '../services/api';

const Contact = () => {
  const { data: companyInfo } = useCompanyInfo();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    inquiry_type: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [submitError, setSubmitError] = useState(null);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name || !formData.email || !formData.inquiry_type || !formData.message) {
      setSubmitError('Please fill in all required fields');
      return;
    }
    
    setIsSubmitting(true);
    setSubmitError(null);
    
    try {
      const response = await api.submitContactInquiry(formData);
      console.log('Form submitted successfully:', response);
      
      setSubmitSuccess(true);
      
      // Reset form
      setFormData({
        name: '',
        email: '',
        phone: '',
        company: '',
        inquiry_type: '',
        message: ''
      });
      
      // Hide success message after 5 seconds
      setTimeout(() => setSubmitSuccess(false), 5000);
      
    } catch (error) {
      console.error('Form submission failed:', error);
      setSubmitError(error.response?.data?.message || 'Failed to submit inquiry. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const contactMethods = [
    {
      icon: Phone,
      title: 'Phone Numbers',
      details: [
        { label: 'UAE Office', value: companyInfo?.contact?.phoneUAE },
        { label: 'Ethiopia Office', value: companyInfo?.contact?.phoneEthiopia }
      ],
      action: 'Call Us'
    },
    {
      icon: MessageCircle,
      title: 'WhatsApp',
      details: [
        { label: 'Quick Response', value: companyInfo.contact.whatsapp }
      ],
      action: 'Chat Now'
    },
    {
      icon: Mail,
      title: 'Email',
      details: [
        { label: 'General Inquiries', value: companyInfo.contact.email }
      ],
      action: 'Send Email'
    }
  ];

  const officeHours = [
    { day: 'Monday - Friday', time: '8:00 AM - 6:00 PM GST' },
    { day: 'Saturday', time: '9:00 AM - 4:00 PM GST' },
    { day: 'Sunday', time: 'Closed' }
  ];

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-slate-900 to-slate-800 text-white py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <Badge className="mb-6 bg-blue-600 hover:bg-blue-700 text-white">
              Get in Touch
            </Badge>
            <h1 className="text-4xl lg:text-5xl font-bold mb-6">
              Contact Sun Star International
            </h1>
            <p className="text-xl text-slate-300 max-w-3xl mx-auto">
              Ready to start your next project? Reach out to our team for competitive quotes, product inquiries, or partnership opportunities.
            </p>
          </div>
        </div>
      </section>

      {/* Contact Methods */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-slate-800 mb-4">
              Multiple Ways to Reach Us
            </h2>
            <p className="text-xl text-slate-600">
              Choose your preferred method of communication
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {contactMethods.map((method, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                <CardContent className="p-8">
                  <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                    <method.icon className="h-8 w-8 text-blue-600" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-800 mb-4">
                    {method.title}
                  </h3>
                  <div className="space-y-3 mb-6">
                    {method.details.map((detail, idx) => (
                      <div key={idx}>
                        <div className="text-sm text-slate-600 font-medium">{detail.label}</div>
                        <div className="font-semibold text-slate-800">{detail.value}</div>
                      </div>
                    ))}
                  </div>
                  <Button variant="outline" className="w-full">
                    {method.action}
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Form & Info */}
      <section className="py-16 bg-slate-50">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
            {/* Contact Form */}
            <Card>
              <CardHeader>
                <CardTitle className="text-2xl text-slate-800">Send Us a Message</CardTitle>
                <p className="text-slate-600">
                  Fill out the form below and we'll get back to you within 24 hours.
                </p>
              </CardHeader>
              <CardContent className="space-y-6">
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="name">Full Name *</Label>
                      <Input
                        id="name"
                        type="text"
                        value={formData.name}
                        onChange={(e) => handleInputChange('name', e.target.value)}
                        required
                        className="mt-1"
                      />
                    </div>
                    <div>
                      <Label htmlFor="email">Email Address *</Label>
                      <Input
                        id="email"
                        type="email"
                        value={formData.email}
                        onChange={(e) => handleInputChange('email', e.target.value)}
                        required
                        className="mt-1"
                      />
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="phone">Phone / WhatsApp</Label>
                      <Input
                        id="phone"
                        type="tel"
                        value={formData.phone}
                        onChange={(e) => handleInputChange('phone', e.target.value)}
                        className="mt-1"
                      />
                    </div>
                    <div>
                      <Label htmlFor="company">Company Name</Label>
                      <Input
                        id="company"
                        type="text"
                        value={formData.company}
                        onChange={(e) => handleInputChange('company', e.target.value)}
                        className="mt-1"
                      />
                    </div>
                  </div>
                  
                  <div>
                    <Label htmlFor="inquiryType">Inquiry Type *</Label>
                    <Select value={formData.inquiry_type} onValueChange={(value) => handleInputChange('inquiry_type', value)}>
                      <SelectTrigger className="mt-1">
                        <SelectValue placeholder="Select inquiry type" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="vehicles">New Passenger Vehicles</SelectItem>
                        <SelectItem value="auto-parts">Auto Spare Parts</SelectItem>
                        <SelectItem value="machinery-parts">Heavy Machinery Parts</SelectItem>
                        <SelectItem value="construction">Construction Equipment</SelectItem>
                        <SelectItem value="custom">Custom Sourcing</SelectItem>
                        <SelectItem value="partnership">Partnership Opportunity</SelectItem>
                        <SelectItem value="other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div>
                    <Label htmlFor="message">Message *</Label>
                    <Textarea
                      id="message"
                      value={formData.message}
                      onChange={(e) => handleInputChange('message', e.target.value)}
                      placeholder="Please provide details about your requirements, quantities, specifications, or any other relevant information..."
                      rows={6}
                      required
                      className="mt-1"
                    />
                  </div>
                  
                  {submitError && (
                    <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-md text-destructive text-sm">
                      {submitError}
                    </div>
                  )}
                  
                  {submitSuccess && (
                    <div className="p-3 bg-green-100 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-md text-green-700 dark:text-green-300 text-sm flex items-center gap-2">
                      <CheckCircle className="h-4 w-4" />
                      Thank you for your inquiry! We will contact you within 24 hours.
                    </div>
                  )}
                  
                  <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700" disabled={isSubmitting}>
                    {isSubmitting ? (
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    ) : (
                      <Send className="mr-2 h-4 w-4" />
                    )}
                    {isSubmitting ? 'Sending...' : 'Send Message'}
                  </Button>
                </form>
              </CardContent>
            </Card>

            {/* Company Information */}
            <div className="space-y-8">
              {/* Office Location */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Building2 className="h-5 w-5 text-blue-600" />
                    Office Location
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <div className="font-semibold text-slate-800 mb-2">{companyInfo?.name}</div>
                      <div className="text-slate-600 space-y-1">
                        <div>{companyInfo?.address?.building}</div>
                        <div>{companyInfo?.address?.zone}</div>
                        <div>{companyInfo?.address?.city}, {companyInfo?.address?.country}</div>
                      </div>
                    </div>
                    
                    <div className="pt-4 border-t">
                      <Badge className="bg-green-100 text-green-700">
                        Licensed by RAKEZ • License: {companyInfo.licenseNo}
                      </Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Office Hours */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Clock className="h-5 w-5 text-blue-600" />
                    Office Hours
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {officeHours.map((schedule, index) => (
                      <div key={index} className="flex justify-between items-center">
                        <span className="font-medium text-slate-800">{schedule.day}</span>
                        <span className="text-slate-600">{schedule.time}</span>
                      </div>
                    ))}
                  </div>
                  <div className="mt-4 pt-4 border-t">
                    <div className="flex items-center gap-2 text-blue-600">
                      <Headphones className="h-4 w-4" />
                      <span className="text-sm font-medium">Emergency support available 24/7</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Map Placeholder */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <MapPin className="h-5 w-5 text-blue-600" />
                    Find Us
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="bg-slate-200 h-64 rounded-lg flex items-center justify-center">
                    <div className="text-center text-slate-600">
                      <MapPin className="h-12 w-12 mx-auto mb-4" />
                      <div className="font-medium">Interactive Map</div>
                      <div className="text-sm">Al Hulaila Industrial Zone</div>
                      <div className="text-sm">Ras Al Khaimah, UAE</div>
                    </div>
                  </div>
                  <Button variant="outline" className="w-full mt-4">
                    <Globe className="mr-2 h-4 w-4" />
                    Open in Google Maps
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Emergency Contact */}
      <section className="py-16 bg-gradient-to-r from-blue-600 to-blue-700 text-white">
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl lg:text-4xl font-bold mb-6">
              Need Immediate Assistance?
            </h2>
            <p className="text-xl mb-8 opacity-90">
              For urgent inquiries or immediate support, reach out to us directly via WhatsApp or phone.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" variant="secondary" className="text-lg px-8">
                <MessageCircle className="mr-2 h-5 w-5" />
                WhatsApp Us
              </Button>
              <Button size="lg" variant="outline" className="text-lg px-8 border-white text-white hover:bg-white hover:text-blue-600">
                <Phone className="mr-2 h-5 w-5" />
                Call Now
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Contact;
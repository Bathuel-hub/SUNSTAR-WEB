import React from 'react';
import { Link } from 'react-router-dom';
import { Star, Phone, Mail, MapPin, Linkedin, MessageCircle, Facebook } from 'lucide-react';
import { useCompanyInfo } from '../hooks/useApi';
import { contactActions } from '../utils/contactUtils';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  const { data: companyInfo } = useCompanyInfo();

  return (
    <footer className="bg-card border-t border-border">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="lg:col-span-2">
            <div className="flex items-center gap-3 mb-6">
              <div className="relative">
                <img 
                  src="/sunstar-logo.png" 
                  alt="Sunstar International" 
                  className="h-10 w-10 object-contain rounded-full bg-white/10 p-1 border-2 border-primary/20"
                />
              </div>
              <div>
                <div className="font-bold text-lg text-foreground">SUNSTAR</div>
                <div className="text-sm text-muted-foreground -mt-1">INTERNATIONAL FZ-LLC</div>
              </div>
            </div>
            
            <p className="text-muted-foreground mb-6 max-w-md">
              {companyInfo?.mission || 'To connect global markets with high-quality cars, spare parts, and heavy equipment.'}
            </p>
            
            <div className="space-y-3 text-sm">
              <div className="flex items-start gap-2">
                <MapPin className="h-4 w-4 text-primary mt-1 flex-shrink-0" />
                <div>
                  <div>{companyInfo?.address?.building}</div>
                  <div>{companyInfo?.address?.zone}</div>
                  <div>{companyInfo?.address?.city}, {companyInfo?.address?.country}</div>
                </div>
              </div>
              
              <div className="flex items-center gap-2 cursor-pointer hover:text-primary transition-colors" onClick={() => contactActions.makeCall(companyInfo?.contact?.phoneUAE || '+971-XXX-XXXXXX')}>
                <Phone className="h-4 w-4 text-primary" />
                <span>UAE: {companyInfo?.contact?.phoneUAE}</span>
              </div>
              
              <div className="flex items-center gap-2 cursor-pointer hover:text-primary transition-colors" onClick={() => contactActions.makeCall(companyInfo?.contact?.phoneEthiopia || '+251-911373857')}>
                <Phone className="h-4 w-4 text-primary" />
                <span>Ethiopia: {companyInfo?.contact?.phoneEthiopia}</span>
              </div>
              
              <div className="flex items-center gap-2 cursor-pointer hover:text-primary transition-colors" onClick={() => contactActions.sendEmail(companyInfo?.contact?.email || 'info@sunstarintl.ae')}>
                <Mail className="h-4 w-4 text-primary" />
                <span>{companyInfo?.contact?.email}</span>
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold text-foreground mb-4">Quick Links</h3>
            <div className="space-y-2">
              <Link to="/" className="block text-muted-foreground hover:text-primary transition-colors">
                Home
              </Link>
              <Link to="/about" className="block text-muted-foreground hover:text-primary transition-colors">
                About Us
              </Link>
              <Link to="/products" className="block text-muted-foreground hover:text-primary transition-colors">
                Products & Services
              </Link>
              <Link to="/store" className="block text-muted-foreground hover:text-primary transition-colors">
                Store
              </Link>
              <Link to="/why-choose-us" className="block text-muted-foreground hover:text-primary transition-colors">
                Why Choose Us
              </Link>
              <Link to="/contact" className="block text-muted-foreground hover:text-primary transition-colors">
                Contact
              </Link>
            </div>
          </div>

          {/* Legal & Social */}
          <div>
            <h3 className="font-semibold text-foreground mb-4">Legal & Social</h3>
            <div className="space-y-3 text-sm text-muted-foreground">
              <div>
                <div className="font-medium text-foreground">License Information</div>
                <div>License No: {companyInfo?.license_no}</div>
                <div>Licensed by: {companyInfo?.license?.authority}</div>
                <div>Manager: {companyInfo?.manager}</div>
              </div>
              
              <div className="pt-4">
                <div className="font-medium text-foreground mb-2">Follow Us</div>
                <div className="flex gap-3">
                  <button 
                    onClick={() => window.open('https://linkedin.com/company/sun-star-international', '_blank')}
                    className="text-muted-foreground hover:text-primary transition-colors"
                    aria-label="LinkedIn"
                  >
                    <Linkedin className="h-5 w-5" />
                  </button>
                  <button 
                    onClick={() => contactActions.openWhatsApp(companyInfo?.contact?.whatsapp || companyInfo?.contact?.phoneUAE || '+971-XXX-XXXXXX', 'Hello Sun Star International, I am interested in your services.')}
                    className="text-muted-foreground hover:text-secondary transition-colors"
                    aria-label="WhatsApp"
                  >
                    <MessageCircle className="h-5 w-5" />
                  </button>
                  <button 
                    onClick={() => window.open('https://web.facebook.com/profile.php?id=61580036196630', '_blank')}
                    className="text-muted-foreground hover:text-primary transition-colors"
                    aria-label="Facebook"
                  >
                    <Facebook className="h-5 w-5" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-border mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center text-sm text-muted-foreground">
            <div>
              © {currentYear} {companyInfo?.name || 'Sun Star International FZ-LLC'}. All rights reserved.
            </div>
            <div className="mt-4 md:mt-0">
              Licensed by Ras Al Khaimah Economic Zone (RAKEZ)
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
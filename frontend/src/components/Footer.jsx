import React from 'react';
import { Link } from 'react-router-dom';
import { Star, Phone, Mail, MapPin, Linkedin, MessageCircle, Facebook } from 'lucide-react';
import { companyInfo } from '../mock';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-slate-900 text-slate-100">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="lg:col-span-2">
            <div className="flex items-center gap-2 mb-6">
              <div className="relative">
                <Star className="h-8 w-8 text-blue-400 fill-current" />
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="w-3 h-3 bg-slate-300 rounded-full"></div>
                </div>
              </div>
              <div>
                <div className="font-bold text-lg text-white">SUN STAR</div>
                <div className="text-sm text-slate-400 -mt-1">INTERNATIONAL FZ-LLC</div>
              </div>
            </div>
            
            <p className="text-slate-300 mb-6 max-w-md">
              {companyInfo.mission}
            </p>
            
            <div className="space-y-3 text-sm">
              <div className="flex items-start gap-2">
                <MapPin className="h-4 w-4 text-blue-400 mt-1 flex-shrink-0" />
                <div>
                  <div>{companyInfo.address.building}</div>
                  <div>{companyInfo.address.zone}</div>
                  <div>{companyInfo.address.city}, {companyInfo.address.country}</div>
                </div>
              </div>
              
              <div className="flex items-center gap-2">
                <Phone className="h-4 w-4 text-blue-400" />
                <span>UAE: {companyInfo.contact.phoneUAE}</span>
              </div>
              
              <div className="flex items-center gap-2">
                <Phone className="h-4 w-4 text-blue-400" />
                <span>Ethiopia: {companyInfo.contact.phoneEthiopia}</span>
              </div>
              
              <div className="flex items-center gap-2">
                <Mail className="h-4 w-4 text-blue-400" />
                <span>{companyInfo.contact.email}</span>
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold text-white mb-4">Quick Links</h3>
            <div className="space-y-2">
              <Link to="/" className="block text-slate-300 hover:text-blue-400 transition-colors">
                Home
              </Link>
              <Link to="/about" className="block text-slate-300 hover:text-blue-400 transition-colors">
                About Us
              </Link>
              <Link to="/products" className="block text-slate-300 hover:text-blue-400 transition-colors">
                Products & Services
              </Link>
              <Link to="/why-choose-us" className="block text-slate-300 hover:text-blue-400 transition-colors">
                Why Choose Us
              </Link>
              <Link to="/contact" className="block text-slate-300 hover:text-blue-400 transition-colors">
                Contact
              </Link>
            </div>
          </div>

          {/* Legal & Social */}
          <div>
            <h3 className="font-semibold text-white mb-4">Legal & Social</h3>
            <div className="space-y-3 text-sm text-slate-300">
              <div>
                <div className="font-medium text-white">License Information</div>
                <div>License No: {companyInfo.licenseNo}</div>
                <div>Licensed by: {companyInfo.license.authority}</div>
                <div>Manager: {companyInfo.manager}</div>
              </div>
              
              <div className="pt-4">
                <div className="font-medium text-white mb-2">Follow Us</div>
                <div className="flex gap-3">
                  <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors">
                    <Linkedin className="h-5 w-5" />
                  </a>
                  <a href="#" className="text-slate-400 hover:text-green-400 transition-colors">
                    <MessageCircle className="h-5 w-5" />
                  </a>
                  <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors">
                    <Facebook className="h-5 w-5" />
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-slate-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center text-sm text-slate-400">
            <div>
              © {currentYear} {companyInfo.name}. All rights reserved.
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
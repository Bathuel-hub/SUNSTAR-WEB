import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button } from './ui/button';
import { Sheet, SheetContent, SheetTrigger } from './ui/sheet';
import { Menu, Star, Phone, Mail } from 'lucide-react';

const Header = () => {
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(false);

  const navItems = [
    { name: 'Home', path: '/' },
    { name: 'About', path: '/about' },
    { name: 'Products & Services', path: '/products' },
    { name: 'Why Choose Us', path: '/why-choose-us' },
    { name: 'Contact', path: '/contact' }
  ];

  const Logo = () => (
    <div className="flex items-center gap-2">
      <div className="relative">
        <Star className="h-8 w-8 text-blue-600 fill-current" />
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-3 h-3 bg-slate-300 rounded-full"></div>
        </div>
      </div>
      <div>
        <div className="font-bold text-lg text-slate-800">SUN STAR</div>
        <div className="text-xs text-slate-600 -mt-1">INTERNATIONAL</div>
      </div>
    </div>
  );

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
      <div className="container mx-auto px-4">
        {/* Top bar with contact info */}
        <div className="hidden md:flex justify-between items-center py-2 text-sm text-slate-600 border-b border-slate-100">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1">
              <Phone className="h-3 w-3" />
              <span>UAE: +971-XXX-XXXXXX</span>
            </div>
            <div className="flex items-center gap-1">
              <Mail className="h-3 w-3" />
              <span>info@sunstarintl.ae</span>
            </div>
          </div>
          <div className="text-blue-600 font-medium">
            Licensed by RAKEZ | License: 5034384
          </div>
        </div>

        {/* Main navigation */}
        <div className="flex items-center justify-between py-4">
          <Link to="/" className="hover:opacity-80 transition-opacity">
            <Logo />
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center space-x-8">
            {navItems.map((item) => (
              <Link
                key={item.name}
                to={item.path}
                className={`text-sm font-medium transition-colors hover:text-blue-600 ${
                  location.pathname === item.path
                    ? 'text-blue-600 border-b-2 border-blue-600 pb-1'
                    : 'text-slate-700'
                }`}
              >
                {item.name}
              </Link>
            ))}
          </nav>

          {/* Contact CTA - Desktop */}
          <div className="hidden lg:flex items-center gap-3">
            <Button variant="outline" size="sm">
              Request Quote
            </Button>
            <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
              Contact Us
            </Button>
          </div>

          {/* Mobile Menu */}
          <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetTrigger asChild className="lg:hidden">
              <Button variant="ghost" size="sm">
                <Menu className="h-5 w-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-80">
              <div className="flex flex-col space-y-6 mt-6">
                <Logo />
                <nav className="flex flex-col space-y-4">
                  {navItems.map((item) => (
                    <Link
                      key={item.name}
                      to={item.path}
                      className={`text-lg font-medium transition-colors hover:text-blue-600 ${
                        location.pathname === item.path
                          ? 'text-blue-600'
                          : 'text-slate-700'
                      }`}
                      onClick={() => setIsOpen(false)}
                    >
                      {item.name}
                    </Link>
                  ))}
                </nav>
                <div className="flex flex-col gap-3 pt-4 border-t">
                  <Button variant="outline">Request Quote</Button>
                  <Button className="bg-blue-600 hover:bg-blue-700">
                    Contact Us
                  </Button>
                </div>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
};

export default Header;
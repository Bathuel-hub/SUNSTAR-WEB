import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button } from './ui/button';
import { Sheet, SheetContent, SheetTrigger } from './ui/sheet';
import { Menu, Star, Phone, Mail } from 'lucide-react';
import ThemeToggle from './ThemeToggle';
import { useCompanyInfo } from '../hooks/useApi';

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
        <Star className="h-8 w-8 text-primary fill-current" />
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-3 h-3 bg-secondary rounded-full"></div>
        </div>
      </div>
      <div>
        <div className="font-bold text-lg text-foreground">SUN STAR</div>
        <div className="text-xs text-muted-foreground -mt-1">INTERNATIONAL</div>
      </div>
    </div>
  );

  return (
    <header className="bg-card border-b border-border sticky top-0 z-50 shadow-sm">
      <div className="container mx-auto px-4">
        {/* Top bar with contact info */}
        <div className="hidden md:flex justify-between items-center py-2 text-sm text-muted-foreground border-b border-border/50">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1">
              <Phone className="h-3 w-3" />
              <span>UAE: +971-XXX-XXXXXX</span>
            </div>
            <div className="flex items-center gap-1">
              <Phone className="h-3 w-3" />
              <span>Ethiopia: +251-911373857</span>
            </div>
            <div className="flex items-center gap-1">
              <Mail className="h-3 w-3" />
              <span>info@sunstarintl.ae</span>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-primary font-medium">
              Licensed by RAKEZ | License: 5034384
            </div>
            <ThemeToggle />
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
                className={`text-sm font-medium transition-colors hover:text-primary ${
                  location.pathname === item.path
                    ? 'text-primary border-b-2 border-primary pb-1'
                    : 'text-muted-foreground'
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
            <Button size="sm" className="bg-primary hover:bg-primary/90">
              Contact Us
            </Button>
          </div>

          {/* Mobile Menu */}
          <div className="lg:hidden flex items-center gap-2">
            <ThemeToggle />
            <Sheet open={isOpen} onOpenChange={setIsOpen}>
              <SheetTrigger asChild>
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
                        className={`text-lg font-medium transition-colors hover:text-primary ${
                          location.pathname === item.path
                            ? 'text-primary'
                            : 'text-muted-foreground'
                        }`}
                        onClick={() => setIsOpen(false)}
                      >
                        {item.name}
                      </Link>
                    ))}
                  </nav>
                  <div className="flex flex-col gap-3 pt-4 border-t border-border">
                    <Button variant="outline">Request Quote</Button>
                    <Button className="bg-primary hover:bg-primary/90">
                      Contact Us
                    </Button>
                  </div>
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
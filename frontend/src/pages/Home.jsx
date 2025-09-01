import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { ArrowRight, Car, Wrench, Truck, Building2, Star, Quote, Loader2 } from 'lucide-react';
import { useCompanyInfo, useProductCategories, useTestimonials } from '../hooks/useApi';
import { contactActions } from '../utils/contactUtils';
import { heroImage } from '../mock';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const { data: companyInfo, loading: companyLoading, error: companyError } = useCompanyInfo();
  const { data: productCategories, loading: productsLoading, error: productsError } = useProductCategories();
  const { data: testimonials, loading: testimonialsLoading, error: testimonialsError } = useTestimonials();

  const quickNavItems = [
    { title: 'Cars', icon: Car, path: '/products', color: 'bg-primary/10 text-primary dark:bg-primary/20' },
    { title: 'Spare Parts', icon: Wrench, path: '/products', color: 'bg-secondary/10 text-secondary dark:bg-secondary/20' },
    { title: 'Machinery', icon: Truck, path: '/products', color: 'bg-primary/10 text-primary dark:bg-primary/20' }
  ];

  // Loading state
  if (companyLoading || productsLoading || testimonialsLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="flex items-center gap-2">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <span className="text-lg text-foreground">Loading...</span>
        </div>
      </div>
    );
  }

  // Error state
  if (companyError || productsError || testimonialsError) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="text-lg text-foreground mb-4">Failed to load data</div>
          <Button onClick={() => window.location.reload()}>
            Try Again
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-card via-background to-card text-foreground overflow-hidden border-b border-border">
        <div 
          className="absolute inset-0 bg-cover bg-center opacity-20 dark:opacity-15"
          style={{ backgroundImage: `url(${heroImage})` }}
        />
        <div className="absolute inset-0 bg-gradient-to-r from-background/90 to-card/80 dark:from-background/95 dark:to-background/90" />
        
        <div className="relative container mx-auto px-4 py-20 lg:py-32">
          <div className="max-w-4xl mx-auto text-center">
            <Badge className="mb-6 bg-primary hover:bg-primary/90 text-primary-foreground">
              Licensed by RAKEZ • License No: {companyInfo?.license_no}
            </Badge>
            
            <h1 className="text-4xl lg:text-6xl font-bold mb-6 leading-tight">
              {companyInfo?.tagline && companyInfo.tagline.split('.').map((part, index) => (
                <span key={index} className="block">
                  {part.trim()}{index === 0 ? '.' : ''}
                  {index === 1 && (
                    <span className="text-primary"> {part.trim()}.</span>
                  )}
                </span>
              ))}
            </h1>
            
            <p className="text-xl lg:text-2xl text-muted-foreground mb-8 max-w-3xl mx-auto">
              Your trusted partner for new passenger vehicles, automotive parts, and heavy construction equipment across the Middle East and beyond.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg" 
                className="bg-primary hover:bg-primary/90 text-lg px-8"
                onClick={() => contactActions.requestQuote(companyInfo?.contact?.email || 'info@sunstarintl.ae')}
              >
                Request Quote
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Link to="/products">
                <Button variant="outline" size="lg" className="text-lg px-8 border-foreground text-foreground hover:bg-foreground hover:text-background">
                  View Products
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Quick Navigation */}
      <section className="py-16 bg-card">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-foreground mb-4">
              What Are You Looking For?
            </h2>
            <p className="text-xl text-muted-foreground">
              Quick access to our main product categories
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {quickNavItems.map((item, index) => (
              <Card key={index} className="group cursor-pointer hover:shadow-xl transition-all duration-300 hover:-translate-y-2">
                <CardContent className="p-8 text-center">
                  <div className={`inline-flex p-4 rounded-full ${item.color} mb-6 group-hover:scale-110 transition-transform`}>
                    <item.icon className="h-8 w-8" />
                  </div>
                  <h3 className="text-xl font-semibold text-foreground mb-4">{item.title}</h3>
                  <Link to={item.path}>
                    <Button variant="ghost" className="group-hover:text-primary w-full">
                      Browse {item.title}
                      <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-16 bg-muted">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-foreground mb-4">
              Our Product Categories
            </h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              From passenger vehicles to heavy construction equipment, we provide comprehensive trading solutions
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {productCategories?.map((category) => (
              <Card key={category.id} className="group overflow-hidden hover:shadow-xl transition-all duration-300">
                <div className="relative h-64 overflow-hidden">
                  <img 
                    src={category.image} 
                    alt={category.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                  <div className="absolute bottom-4 left-4 right-4 text-white">
                    <h3 className="text-xl font-bold mb-2">{category.name}</h3>
                  </div>
                </div>
                <CardContent className="p-6">
                  <p className="text-muted-foreground mb-4">{category.description}</p>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {category.products.slice(0, 3).map((product, idx) => (
                      <Badge key={idx} variant="secondary" className="text-xs">
                        {product}
                      </Badge>
                    ))}
                    {category.products.length > 3 && (
                      <Badge variant="outline" className="text-xs">
                        +{category.products.length - 3} more
                      </Badge>
                    )}
                  </div>
                  <Link to="/products">
                    <Button variant="ghost" className="w-full group-hover:text-primary">
                      Learn More
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 bg-card">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-foreground mb-4">
              What Our Clients Say
            </h2>
            <p className="text-xl text-muted-foreground">
              Trusted by businesses across the region
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {testimonials?.map((testimonial) => (
              <Card key={testimonial.id} className="hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <Quote className="h-8 w-8 text-blue-600 mb-4" />
                  <p className="text-muted-foreground mb-6 italic">"{testimonial.text}"</p>
                  <div className="flex items-center gap-2 mb-2">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="h-4 w-4 text-secondary fill-current" />
                    ))}
                  </div>
                  <div className="font-semibold text-foreground">{testimonial.name}</div>
                  <div className="text-sm text-muted-foreground">{testimonial.company}</div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-primary to-primary/80 text-primary-foreground">
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl lg:text-4xl font-bold mb-6">
              Ready to Start Trading With Us?
            </h2>
            <p className="text-xl mb-8 opacity-90">
              Get in touch today for competitive quotes and reliable service across all our product categories.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg" 
                variant="secondary" 
                className="text-lg px-8"
                onClick={() => contactActions.requestQuote(companyInfo?.contact?.email || 'info@sunstarintl.ae')}
              >
                <Building2 className="mr-2 h-5 w-5" />
                Request Quote
              </Button>
              <Link to="/contact">
                <Button size="lg" variant="outline" className="text-lg px-8 border-primary-foreground text-primary-foreground hover:bg-primary-foreground hover:text-primary">
                  Contact Us Today
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
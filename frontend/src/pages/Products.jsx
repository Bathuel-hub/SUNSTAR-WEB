import React, { useState } from 'react';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Car, Wrench, Cog, Truck, ArrowRight, Phone, Mail } from 'lucide-react';
import { productCategories } from '../mock';

const Products = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');

  const categoryIcons = {
    1: Car,
    2: Wrench, 
    3: Cog,
    4: Truck
  };

  const sampleProducts = {
    1: [
      { name: 'Toyota Camry 2024', specs: '2.5L Engine, CVT, LED Headlights', price: 'Contact for Price' },
      { name: 'Honda Accord 2024', specs: '1.5L Turbo, Hybrid Available', price: 'Contact for Price' },
      { name: 'Nissan Altima 2024', specs: '2.0L VC-Turbo, ProPILOT Assist', price: 'Contact for Price' },
      { name: 'Hyundai Sonata 2024', specs: '2.5L GDI, SmartSense Safety', price: 'Contact for Price' }
    ],
    2: [
      { name: 'Engine Oil Filters', specs: 'Compatible with major brands', price: 'From $15' },
      { name: 'Brake Pads Set', specs: 'Ceramic & Semi-Metallic options', price: 'From $45' },
      { name: 'Transmission Parts', specs: 'OEM & Aftermarket quality', price: 'Contact for Price' },
      { name: 'Air Intake Systems', specs: 'Performance & Standard grades', price: 'From $120' }
    ],
    3: [
      { name: 'Hydraulic Cylinders', specs: 'Various bore sizes available', price: 'Contact for Price' },
      { name: 'Track Chains', specs: 'Heavy-duty steel construction', price: 'Contact for Price' },
      { name: 'Engine Overhaul Kits', specs: 'Complete rebuild packages', price: 'Contact for Price' },
      { name: 'Hydraulic Pumps', specs: 'OEM replacements available', price: 'Contact for Price' }
    ],
    4: [
      { name: 'Excavator CAT 320', specs: '20-ton operating weight', price: 'Contact for Price' },
      { name: 'Bulldozer D6T', specs: 'Track-type tractor', price: 'Contact for Price' },
      { name: 'Mobile Crane 50T', specs: 'Hydraulic telescopic boom', price: 'Contact for Price' },
      { name: 'Concrete Mixer Truck', specs: '8-12 cubic meter capacity', price: 'Contact for Price' }
    ]
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-card to-background text-foreground py-20 border-b border-border">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <Badge className="mb-6 bg-blue-600 hover:bg-blue-700 text-white">
              Comprehensive Product Range
            </Badge>
            <h1 className="text-4xl lg:text-5xl font-bold mb-6">
              Products & Services
            </h1>
            <p className="text-xl text-slate-300 max-w-3xl mx-auto">
              From passenger vehicles to heavy construction machinery, discover our extensive catalog of high-quality products and professional trading services.
            </p>
          </div>
        </div>
      </section>

      {/* Product Categories Overview */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-slate-800 mb-4">
              Our Product Categories
            </h2>
            <p className="text-xl text-slate-600">
              Explore our comprehensive range of automotive and construction solutions
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {productCategories.map((category) => {
              const IconComponent = categoryIcons[category.id];
              return (
                <Card key={category.id} className="group overflow-hidden hover:shadow-xl transition-all duration-300">
                  <div className="relative h-64 overflow-hidden">
                    <img 
                      src={category.image} 
                      alt={category.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                    <div className="absolute top-4 right-4">
                      <div className="bg-white/20 backdrop-blur-sm rounded-full p-3">
                        <IconComponent className="h-6 w-6 text-white" />
                      </div>
                    </div>
                    <div className="absolute bottom-4 left-4 right-4 text-white">
                      <h3 className="text-xl font-bold mb-2">{category.name}</h3>
                    </div>
                  </div>
                  <CardContent className="p-6">
                    <p className="text-slate-600 mb-4">{category.description}</p>
                    <div className="flex flex-wrap gap-2 mb-6">
                      {category.products.map((product, idx) => (
                        <Badge key={idx} variant="secondary" className="text-xs">
                          {product}
                        </Badge>
                      ))}
                    </div>
                    <Button className="w-full bg-blue-600 hover:bg-blue-700">
                      View Products
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Detailed Product Catalog */}
      <section className="py-16 bg-slate-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-slate-800 mb-4">
              Product Catalog
            </h2>
            <p className="text-xl text-slate-600">
              Browse our current inventory and available products
            </p>
          </div>
          
          <Tabs defaultValue="1" className="w-full">
            <TabsList className="grid w-full grid-cols-4 bg-white shadow-sm mb-8">
              {productCategories.map((category) => {
                const IconComponent = categoryIcons[category.id];
                return (
                  <TabsTrigger 
                    key={category.id} 
                    value={category.id.toString()}
                    className="flex flex-col items-center gap-2 p-4 data-[state=active]:bg-blue-50 data-[state=active]:text-blue-600"
                  >
                    <IconComponent className="h-5 w-5" />
                    <span className="text-xs font-medium">{category.name.split(' ')[0]}</span>
                  </TabsTrigger>
                );
              })}
            </TabsList>

            {productCategories.map((category) => (
              <TabsContent key={category.id} value={category.id.toString()}>
                <Card>
                  <CardContent className="p-8">
                    <div className="mb-8 text-center">
                      <h3 className="text-2xl font-bold text-slate-800 mb-4">
                        {category.name}
                      </h3>
                      <p className="text-slate-600 max-w-2xl mx-auto">
                        {category.description}
                      </p>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {sampleProducts[category.id]?.map((product, index) => (
                        <Card key={index} className="hover:shadow-md transition-shadow">
                          <CardContent className="p-6">
                            <div className="flex justify-between items-start mb-4">
                              <h4 className="font-semibold text-slate-800">{product.name}</h4>
                              <Badge variant="outline" className="text-blue-600 border-blue-600">
                                Available
                              </Badge>
                            </div>
                            <p className="text-sm text-slate-600 mb-4">{product.specs}</p>
                            <div className="flex justify-between items-center">
                              <div className="font-semibold text-slate-800">{product.price}</div>
                              <Button size="sm" variant="outline">
                                Get Quote
                              </Button>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            ))}
          </Tabs>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-slate-800 mb-4">
              Our Trading Services
            </h2>
            <p className="text-xl text-slate-600">
              Comprehensive services to support your business needs
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardContent className="p-8">
                <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Truck className="h-8 w-8 text-blue-600" />
                </div>
                <h3 className="text-xl font-bold text-slate-800 mb-4">Global Shipping</h3>
                <p className="text-slate-600 mb-6">
                  Reliable shipping and logistics solutions to deliver your orders worldwide with full tracking and insurance.
                </p>
                <Button variant="outline">Learn More</Button>
              </CardContent>
            </Card>
            
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardContent className="p-8">
                <div className="bg-emerald-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Phone className="h-8 w-8 text-emerald-600" />
                </div>
                <h3 className="text-xl font-bold text-slate-800 mb-4">Custom Sourcing</h3>
                <p className="text-slate-600 mb-6">
                  Can't find what you're looking for? Our team can source specific vehicles, parts, or equipment to meet your requirements.
                </p>
                <Button variant="outline">Contact Us</Button>
              </CardContent>
            </Card>
            
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardContent className="p-8">
                <div className="bg-amber-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Mail className="h-8 w-8 text-amber-600" />
                </div>
                <h3 className="text-xl font-bold text-slate-800 mb-4">Technical Support</h3>
                <p className="text-slate-600 mb-6">
                  Expert technical advice and support to help you choose the right products for your specific applications.
                </p>
                <Button variant="outline">Get Support</Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-blue-600 to-blue-700 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl lg:text-4xl font-bold mb-6">
            Need a Custom Quote?
          </h2>
          <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
            Get competitive pricing on bulk orders or custom specifications. Our team is ready to help you find the perfect solution.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" variant="secondary" className="text-lg px-8">
              Request Bulk Quote
            </Button>
            <Button size="lg" variant="outline" className="text-lg px-8 border-white text-white hover:bg-white hover:text-blue-600">
              Contact Sales Team
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Products;
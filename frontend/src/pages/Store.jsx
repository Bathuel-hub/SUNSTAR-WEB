import React, { useState, useEffect } from 'react';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { 
  Car, Wrench, Cog, Truck, Phone, Mail, Eye, 
  ImageIcon, Package, Loader2, Star
} from 'lucide-react';
import { useProductCategories, useCompanyInfo } from '../hooks/useApi';
import { contactActions } from '../utils/contactUtils';

const Gallery = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const { data: categories } = useProductCategories();
  const { data: companyInfo } = useCompanyInfo();

  const categoryIcons = {
    1: Car,
    2: Wrench,
    3: Cog,
    4: Truck
  };

  // Sample products with generated images for demonstration
  const sampleProducts = {
    1: [ // New Passenger Motor Vehicles
      {
        id: '1',
        name: 'Toyota Camry 2024',
        description: 'Premium sedan with advanced safety features, hybrid engine option, and luxurious interior.',
        price: '$45,000',
        image_url: 'https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=500&h=300&fit=crop',
        is_featured: true,
        category_name: 'New Passenger Motor Vehicles'
      },
      {
        id: '2', 
        name: 'Honda Accord 2024',
        description: 'Reliable family sedan with excellent fuel efficiency and modern technology.',
        price: '$42,000',
        image_url: 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=500&h=300&fit=crop',
        is_featured: false,
        category_name: 'New Passenger Motor Vehicles'
      },
      {
        id: '3',
        name: 'Nissan Altima 2024', 
        description: 'Sporty sedan with ProPILOT Assist and premium interior comfort.',
        price: '$38,500',
        image_url: 'https://images.unsplash.com/photo-1549399047-d52dbf139018?w=500&h=300&fit=crop',
        is_featured: false,
        category_name: 'New Passenger Motor Vehicles'
      }
    ],
    2: [ // Auto Spare Parts & Components
      {
        id: '4',
        name: 'Premium Brake Pads Set',
        description: 'High-performance ceramic brake pads compatible with most vehicle models.',
        price: '$75',
        image_url: 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=500&h=300&fit=crop',
        is_featured: true,
        category_name: 'Auto Spare Parts & Components'
      },
      {
        id: '5',
        name: 'Engine Oil Filter Kit',
        description: 'Complete oil filter kit with premium filters for engine protection.',
        price: '$25',
        image_url: 'https://images.unsplash.com/photo-1635691033744-a1a2a07ba971?w=500&h=300&fit=crop',
        is_featured: false,
        category_name: 'Auto Spare Parts & Components'
      }
    ],
    3: [ // Heavy Equipment & Machinery Spare Parts
      {
        id: '6',
        name: 'Hydraulic Pump Assembly',
        description: 'Heavy-duty hydraulic pump for excavators and construction equipment.',
        price: 'Contact for Price',
        image_url: 'https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=500&h=300&fit=crop',
        is_featured: true,
        category_name: 'Heavy Equipment & Machinery Spare Parts'
      }
    ],
    4: [ // Construction Equipment & Machinery
      {
        id: '7',
        name: 'CAT 320 Excavator',
        description: '20-ton hydraulic excavator perfect for construction and earthmoving.',
        price: 'Contact for Price',
        image_url: 'https://images.unsplash.com/photo-1717386255773-1e3037c81788?w=500&h=300&fit=crop',
        is_featured: true,
        category_name: 'Construction Equipment & Machinery'
      },
      {
        id: '8',
        name: 'Concrete Mixer Truck',
        description: '8 cubic meter capacity concrete mixer truck for construction projects.',
        price: 'Contact for Price', 
        image_url: 'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=500&h=300&fit=crop',
        is_featured: false,
        category_name: 'Construction Equipment & Machinery'
      }
    ]
  };

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      setLoading(true);
      // Try to get products from admin panel
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/products`);
      let adminProducts = [];
      
      if (response.ok) {
        adminProducts = await response.json();
      }

      // Combine admin products with sample products
      const allProducts = [];
      
      // Add admin products
      adminProducts.forEach(product => {
        const categoryName = getCategoryName(product.category_id);
        allProducts.push({
          ...product,
          category_name: categoryName
        });
      });

      // Add sample products for demonstration
      Object.values(sampleProducts).forEach(categoryProducts => {
        categoryProducts.forEach(product => {
          // Only add sample products if we don't have many admin products
          if (adminProducts.length < 5) {
            allProducts.push(product);
          }
        });
      });

      setProducts(allProducts);
    } catch (error) {
      console.error('Failed to load products:', error);
      // Fall back to sample products
      const allSamples = Object.values(sampleProducts).flat();
      setProducts(allSamples);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryName = (categoryId) => {
    const category = categories?.find(cat => cat.id?.toString() === categoryId?.toString());
    return category?.name || 'Unknown Category';
  };

  const getProductsByCategory = (categoryId) => {
    if (categoryId === 'all') return products;
    return products.filter(product => 
      product.category_id?.toString() === categoryId?.toString() ||
      product.category_name === getCategoryName(categoryId)
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="flex items-center gap-2">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <span className="text-lg text-foreground">Loading gallery...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-card to-background text-foreground py-20 border-b border-border">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <Badge className="mb-6 bg-primary hover:bg-primary/90 text-primary-foreground">
              Product Gallery
            </Badge>
            <h1 className="text-4xl lg:text-5xl font-bold mb-6">
              Browse Our Products
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Explore our extensive catalog of vehicles, parts, and machinery. Each product is carefully selected for quality and reliability.
            </p>
          </div>
        </div>
      </section>

      {/* Gallery Navigation */}
      <section className="py-16 bg-card">
        <div className="container mx-auto px-4">
          <Tabs defaultValue="all" className="w-full">
            <div className="flex flex-col lg:flex-row gap-8">
              {/* Category Tabs */}
              <div className="lg:w-1/4">
                <TabsList className="flex flex-col h-auto w-full bg-muted p-2">
                  <TabsTrigger 
                    value="all"
                    className="w-full justify-start p-4 data-[state=active]:bg-primary data-[state=active]:text-primary-foreground"
                  >
                    <Package className="mr-3 h-5 w-5" />
                    All Products ({products.length})
                  </TabsTrigger>
                  
                  {categories?.map((category, index) => {
                    const IconComponent = categoryIcons[index + 1] || Package;
                    const categoryProducts = getProductsByCategory((index + 1).toString());
                    
                    return (
                      <TabsTrigger
                        key={index}
                        value={(index + 1).toString()}
                        className="w-full justify-start p-4 data-[state=active]:bg-primary data-[state=active]:text-primary-foreground"
                      >
                        <IconComponent className="mr-3 h-5 w-5" />
                        <div className="text-left">
                          <div className="font-medium">{category.name.split(' ')[0]} {category.name.split(' ')[1]}</div>
                          <div className="text-xs opacity-70">({categoryProducts.length} items)</div>
                        </div>
                      </TabsTrigger>
                    );
                  })}
                </TabsList>
              </div>

              {/* Products Display */}
              <div className="lg:w-3/4">
                <TabsContent value="all" className="mt-0">
                  <div className="mb-6">
                    <h2 className="text-2xl font-bold text-foreground mb-2">All Products</h2>
                    <p className="text-muted-foreground">Browse our complete product collection</p>
                  </div>
                  <ProductGrid products={products} companyInfo={companyInfo} />
                </TabsContent>

                {categories?.map((category, index) => (
                  <TabsContent key={index} value={(index + 1).toString()} className="mt-0">
                    <div className="mb-6">
                      <h2 className="text-2xl font-bold text-foreground mb-2">{category.name}</h2>
                      <p className="text-muted-foreground">{category.description}</p>
                    </div>
                    <ProductGrid 
                      products={getProductsByCategory((index + 1).toString())} 
                      companyInfo={companyInfo}
                    />
                  </TabsContent>
                ))}
              </div>
            </div>
          </Tabs>
        </div>
      </section>
    </div>
  );
};

// Product Grid Component
const ProductGrid = ({ products, companyInfo }) => {
  if (products.length === 0) {
    return (
      <div className="text-center py-12">
        <ImageIcon className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
        <h3 className="text-lg font-medium text-foreground mb-2">No products in this category</h3>
        <p className="text-muted-foreground">Check back soon for new additions to our inventory</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} companyInfo={companyInfo} />
      ))}
    </div>
  );
};

// Individual Product Card Component  
const ProductCard = ({ product, companyInfo }) => {
  return (
    <Card className="group overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
      {/* Product Image */}
      <div className="relative h-48 overflow-hidden">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="w-full h-full bg-muted flex items-center justify-center">
            <ImageIcon className="h-12 w-12 text-muted-foreground" />
          </div>
        )}
        
        {/* Overlay on hover */}
        <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
          <Button variant="secondary" size="sm">
            <Eye className="mr-2 h-4 w-4" />
            View Details
          </Button>
        </div>

        {/* Featured Badge */}
        {product.is_featured && (
          <div className="absolute top-3 right-3">
            <Badge className="bg-secondary text-secondary-foreground">
              <Star className="mr-1 h-3 w-3 fill-current" />
              Featured
            </Badge>
          </div>
        )}
      </div>

      {/* Product Details */}
      <CardContent className="p-6">
        <div className="mb-3">
          <h3 className="text-lg font-semibold text-foreground mb-2 line-clamp-1">
            {product.name}
          </h3>
          <p className="text-sm text-muted-foreground line-clamp-2">
            {product.description}
          </p>
        </div>

        <div className="flex items-center justify-between mb-4">
          <div className="text-lg font-bold text-primary">
            {product.price}
          </div>
          <Badge variant="outline" className="text-xs">
            {product.category_name?.split(' ')[0] || 'Product'}
          </Badge>
        </div>

        <div className="flex gap-2">
          <Button 
            className="flex-1 bg-primary hover:bg-primary/90"
            onClick={() => contactActions.requestQuote(
              companyInfo?.contact?.email || 'sunstarintl.ae@gmail.com',
              `${product.category_name} - ${product.name}`
            )}
          >
            <Mail className="mr-2 h-4 w-4" />
            Get Quote
          </Button>
          
          <Button 
            variant="outline" 
            size="icon"
            onClick={() => contactActions.openWhatsApp(
              companyInfo?.contact?.whatsapp || companyInfo?.contact?.phoneUAE || '+971551849702',
              `Hello! I'm interested in the ${product.name}. Could you provide more information?`
            )}
          >
            <Phone className="h-4 w-4" />
          </Button>
        </div>

        {/* Availability Status */}
        <div className="mt-3 pt-3 border-t border-border">
          <div className="flex items-center justify-between text-xs">
            <span className="text-muted-foreground">Status:</span>
            <Badge 
              variant={product.is_available !== false ? "default" : "secondary"}
              className="text-xs"
            >
              {product.is_available !== false ? "Available" : "Out of Stock"}
            </Badge>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default Gallery;
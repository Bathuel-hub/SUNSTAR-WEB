import React, { useState, useEffect } from 'react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { Label } from '../components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Badge } from '../components/ui/badge';
import { 
  Plus, Edit2, Trash2, Save, X, Package, DollarSign, 
  ImageIcon, Loader2, Star, CheckCircle, Camera, Type, 
  FileText, AlertCircle, Eye, Home
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { useProductCategories } from '../hooks/useApi';
import ThemeToggle from '../components/ThemeToggle';

const AdminManager = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const { data: categories } = useProductCategories();
  
  const [formData, setFormData] = useState({
    category_id: '',
    name: '',
    description: '',
    price: '',
    image_url: '',
    is_featured: false,
    is_available: true
  });

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/products`);
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error('Failed to load products:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const method = editingProduct ? 'PUT' : 'POST';
      const url = editingProduct 
        ? `${process.env.REACT_APP_BACKEND_URL}/api/admin/products/${editingProduct.id}`
        : `${process.env.REACT_APP_BACKEND_URL}/api/admin/products`;
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        await loadProducts();
        resetForm();
        alert(editingProduct ? 'Product updated successfully!' : 'Product added successfully!');
      } else {
        alert('Failed to save product');
      }
    } catch (error) {
      console.error('Error saving product:', error);
      alert('Error saving product');
    }
  };

  const handleDelete = async (productId) => {
    if (!window.confirm('Are you sure you want to delete this product?')) return;
    
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/products/${productId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        await loadProducts();
        alert('Product deleted successfully!');
      } else {
        alert('Failed to delete product');
      }
    } catch (error) {
      console.error('Error deleting product:', error);
      alert('Error deleting product');
    }
  };

  const handleEdit = (product) => {
    setEditingProduct(product);
    setFormData({
      category_id: product.category_id,
      name: product.name,
      description: product.description,
      price: product.price,
      image_url: product.image_url || '',
      is_featured: product.is_featured,
      is_available: product.is_available
    });
    setShowAddForm(true);
  };

  const resetForm = () => {
    setFormData({
      category_id: '',
      name: '',
      description: '',
      price: '',
      image_url: '',
      is_featured: false,
      is_available: true
    });
    setEditingProduct(null);
    setShowAddForm(false);
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      // For now, we'll use a placeholder URL
      // In production, you'd upload to a service like Cloudinary or AWS S3
      const imageUrl = URL.createObjectURL(file);
      setFormData(prev => ({ ...prev, image_url: imageUrl }));
    }
  };

  const getCategoryName = (categoryId) => {
    const category = categories?.find(cat => cat.id?.toString() === categoryId?.toString());
    return category?.name || 'Unknown Category';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="flex items-center gap-2">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <span className="text-lg text-foreground">Loading admin panel...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Simple Header Bar */}
      <div className="bg-card border-b border-border p-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-4">
            <Link to="/" className="text-primary hover:text-primary/80 transition-colors">
              <Home className="h-6 w-6" />
            </Link>
            <div>
              <h1 className="text-2xl font-bold text-foreground">🏪 Store Manager</h1>
              <p className="text-sm text-muted-foreground">Add and manage your products</p>
            </div>
          </div>
          <ThemeToggle />
        </div>
      </div>

      <div className="max-w-6xl mx-auto p-6">
        {/* Welcome Card */}
        <Card className="mb-8 border-2 border-primary/20">
          <CardContent className="p-8">
            <div className="text-center">
              <Package className="h-12 w-12 text-primary mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-foreground mb-2">Welcome to Your Store Manager!</h2>
              <p className="text-lg text-muted-foreground mb-6">
                Add new products to show customers what you have in stock
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button 
                  size="lg"
                  onClick={() => setShowAddForm(true)}
                  className="bg-primary hover:bg-primary/90 text-lg px-8"
                >
                  <Plus className="mr-2 h-6 w-6" />
                  Add New Product
                </Button>
                <Link to="/gallery">
                  <Button size="lg" variant="outline" className="text-lg px-8">
                    <Eye className="mr-2 h-6 w-6" />
                    View Gallery
                  </Button>
                </Link>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Add/Edit Form */}
        {showAddForm && (
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                {editingProduct ? 'Edit Product' : 'Add New Product'}
                <Button variant="ghost" size="sm" onClick={resetForm}>
                  <X className="h-4 w-4" />
                </Button>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="category_id">Category</Label>
                    <Select value={formData.category_id} onValueChange={(value) => setFormData(prev => ({ ...prev, category_id: value }))}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select category" />
                      </SelectTrigger>
                      <SelectContent>
                        {categories?.map((category, index) => (
                          <SelectItem key={index} value={(index + 1).toString()}>
                            {category.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div>
                    <Label htmlFor="name">Product Name</Label>
                    <Input
                      id="name"
                      value={formData.name}
                      onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                      placeholder="Enter product name"
                      required
                    />
                  </div>
                </div>

                <div>
                  <Label htmlFor="description">Description</Label>
                  <Textarea
                    id="description"
                    value={formData.description}
                    onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                    placeholder="Enter product description"
                    rows={3}
                    required
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="price">Price</Label>
                    <Input
                      id="price"
                      value={formData.price}
                      onChange={(e) => setFormData(prev => ({ ...prev, price: e.target.value }))}
                      placeholder="e.g., $25,000 or Contact for Price"
                      required
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="image">Product Image</Label>
                    <Input
                      id="image"
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                    />
                  </div>
                </div>

                {formData.image_url && (
                  <div>
                    <Label>Preview</Label>
                    <img 
                      src={formData.image_url} 
                      alt="Product preview" 
                      className="w-32 h-32 object-cover rounded-lg border"
                    />
                  </div>
                )}

                <div className="flex gap-4">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.is_featured}
                      onChange={(e) => setFormData(prev => ({ ...prev, is_featured: e.target.checked }))}
                      className="rounded border-gray-300"
                    />
                    <span className="text-sm text-foreground">Featured Product</span>
                  </label>
                  
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.is_available}
                      onChange={(e) => setFormData(prev => ({ ...prev, is_available: e.target.checked }))}
                      className="rounded border-gray-300"
                    />
                    <span className="text-sm text-foreground">Available</span>
                  </label>
                </div>

                <div className="flex gap-4">
                  <Button type="submit" className="bg-primary hover:bg-primary/90">
                    <Save className="mr-2 h-4 w-4" />
                    {editingProduct ? 'Update Product' : 'Add Product'}
                  </Button>
                  <Button type="button" variant="outline" onClick={resetForm}>
                    Cancel
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        )}

        {/* Products Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product) => (
            <Card key={product.id} className="overflow-hidden hover:shadow-lg transition-shadow">
              {product.image_url ? (
                <div className="h-48 bg-muted">
                  <img 
                    src={product.image_url} 
                    alt={product.name}
                    className="w-full h-full object-cover"
                  />
                </div>
              ) : (
                <div className="h-48 bg-muted flex items-center justify-center">
                  <ImageIcon className="h-12 w-12 text-muted-foreground" />
                </div>
              )}
              
              <CardContent className="p-4">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-semibold text-foreground truncate">{product.name}</h3>
                  {product.is_featured && (
                    <Badge className="bg-secondary text-secondary-foreground">Featured</Badge>
                  )}
                </div>
                
                <p className="text-sm text-muted-foreground mb-2 line-clamp-2">
                  {product.description}
                </p>
                
                <div className="flex items-center gap-2 mb-3">
                  <DollarSign className="h-4 w-4 text-primary" />
                  <span className="font-medium text-foreground">{product.price}</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="text-xs text-muted-foreground">
                    {getCategoryName(product.category_id)}
                  </div>
                  
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleEdit(product)}
                    >
                      <Edit2 className="h-3 w-3" />
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleDelete(product.id)}
                      className="text-red-600 hover:text-red-700"
                    >
                      <Trash2 className="h-3 w-3" />
                    </Button>
                  </div>
                </div>
                
                <div className="mt-2 flex gap-2">
                  <Badge variant={product.is_available ? "default" : "secondary"}>
                    {product.is_available ? 'Available' : 'Unavailable'}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {products.length === 0 && (
          <div className="text-center py-12">
            <Package className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-medium text-foreground mb-2">No products yet</h3>
            <p className="text-muted-foreground mb-4">Start by adding your first product to the catalog</p>
            <Button onClick={() => setShowAddForm(true)} className="bg-primary hover:bg-primary/90">
              <Plus className="mr-2 h-4 w-4" />
              Add Your First Product
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminManager;
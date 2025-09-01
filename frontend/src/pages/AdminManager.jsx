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
  FileText, AlertCircle, Eye, Home, Upload, Cloud
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { useProductCategories } from '../hooks/useApi';
import ThemeToggle from '../components/ThemeToggle';

const AdminManager = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
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

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
      alert('Please select an image file');
      return;
    }

    // Validate file size (5MB)
    if (file.size > 5 * 1024 * 1024) {
      alert('File size must be less than 5MB');
      return;
    }

    try {
      setUploading(true);
      setUploadProgress(0);

      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + Math.random() * 20;
        });
      }, 100);

      const formDataUpload = new FormData();
      formDataUpload.append('file', file);

      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/upload/image`, {
        method: 'POST',
        body: formDataUpload,
      });

      if (response.ok) {
        const result = await response.json();
        const imageUrl = `${process.env.REACT_APP_BACKEND_URL}${result.data.file_url}`;
        
        setFormData(prev => ({ ...prev, image_url: imageUrl }));
        setUploadProgress(100);
        
        // Clear progress after a short delay
        setTimeout(() => {
          setUploading(false);
          setUploadProgress(0);
        }, 500);
      } else {
        throw new Error('Upload failed');
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Failed to upload image. Please try again.');
      setUploading(false);
      setUploadProgress(0);
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
                <Link to="/store">
                  <Button size="lg" variant="outline" className="text-lg px-8">
                    <Eye className="mr-2 h-6 w-6" />
                    View Store
                  </Button>
                </Link>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Simple Add/Edit Form */}
        {showAddForm && (
          <Card className="mb-8 border-2 border-primary/30">
            <CardHeader className="bg-primary/5">
              <CardTitle className="flex items-center justify-between text-xl">
                <div className="flex items-center gap-3">
                  {editingProduct ? 
                    <Edit2 className="h-6 w-6 text-primary" /> : 
                    <Plus className="h-6 w-6 text-primary" />
                  }
                  {editingProduct ? 'Edit Your Product' : 'Add New Product'}
                </div>
                <Button variant="ghost" size="lg" onClick={resetForm}>
                  <X className="h-5 w-5" />
                </Button>
              </CardTitle>
            </CardHeader>
            <CardContent className="p-8">
              <form onSubmit={handleSubmit} className="space-y-8">
                {/* Step 1: Product Type */}
                <div className="bg-muted/50 rounded-lg p-6">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="bg-primary text-primary-foreground rounded-full w-8 h-8 flex items-center justify-center font-bold">1</div>
                    <h3 className="text-lg font-semibold">What type of product is this?</h3>
                  </div>
                  <Select value={formData.category_id} onValueChange={(value) => setFormData(prev => ({ ...prev, category_id: value }))}>
                    <SelectTrigger className="h-12 text-base">
                      <SelectValue placeholder="Choose the product type..." />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="1">🚗 Cars & Vehicles</SelectItem>
                      <SelectItem value="2">🔧 Car Parts & Components</SelectItem>
                      <SelectItem value="3">⚙️ Heavy Machinery Parts</SelectItem>
                      <SelectItem value="4">🚜 Construction Equipment</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Step 2: Product Name */}
                <div className="bg-muted/50 rounded-lg p-6">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="bg-primary text-primary-foreground rounded-full w-8 h-8 flex items-center justify-center font-bold">2</div>
                    <h3 className="text-lg font-semibold">What is the product name?</h3>
                  </div>
                  <Input
                    id="name"
                    value={formData.name}
                    onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                    placeholder="Example: Toyota Camry 2024, Brake Pads, etc."
                    className="h-12 text-base"
                    required
                  />
                  <p className="text-sm text-muted-foreground mt-2">📝 Write the full product name clearly</p>
                </div>

                {/* Step 3: Description */}
                <div className="bg-muted/50 rounded-lg p-6">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="bg-primary text-primary-foreground rounded-full w-8 h-8 flex items-center justify-center font-bold">3</div>
                    <h3 className="text-lg font-semibold">Describe your product</h3>
                  </div>
                  <Textarea
                    id="description"
                    value={formData.description}
                    onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                    placeholder="Example: Premium sedan with excellent fuel economy, leather seats, backup camera, etc."
                    rows={4}
                    className="text-base"
                    required
                  />
                  <p className="text-sm text-muted-foreground mt-2">📄 Tell customers what makes this product special</p>
                </div>

                {/* Step 4: Price */}
                <div className="bg-muted/50 rounded-lg p-6">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="bg-primary text-primary-foreground rounded-full w-8 h-8 flex items-center justify-center font-bold">4</div>
                    <h3 className="text-lg font-semibold">What is the price?</h3>
                  </div>
                  <Input
                    id="price"
                    value={formData.price}
                    onChange={(e) => setFormData(prev => ({ ...prev, price: e.target.value }))}
                    placeholder="Example: $25,000 or Contact for Price"
                    className="h-12 text-base"
                    required
                  />
                  <p className="text-sm text-muted-foreground mt-2">💰 Write the price or "Contact for Price" if you prefer</p>
                </div>

                {/* Step 5: Photo - MANDATORY */}
                <div className="bg-muted/50 rounded-lg p-6 border-2 border-primary/20">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="bg-primary text-primary-foreground rounded-full w-8 h-8 flex items-center justify-center font-bold">5</div>
                    <h3 className="text-lg font-semibold">Add a photo *REQUIRED*</h3>
                    <Badge className="bg-red-100 text-red-800 text-xs">MANDATORY</Badge>
                  </div>
                  
                  {!formData.image_url && (
                    <div className="space-y-4">
                      <div className="relative">
                        <Input
                          id="image"
                          type="file"
                          accept="image/*"
                          onChange={handleImageUpload}
                          className="h-12 text-base cursor-pointer"
                          disabled={uploading}
                          required
                        />
                        {uploading && (
                          <div className="absolute inset-0 bg-background/80 flex items-center justify-center rounded-md">
                            <div className="flex items-center gap-2">
                              <Loader2 className="h-4 w-4 animate-spin text-primary" />
                              <span className="text-sm font-medium">Uploading...</span>
                            </div>
                          </div>
                        )}
                      </div>
                      
                      {uploading && (
                        <div className="space-y-2">
                          <div className="flex items-center justify-between text-sm">
                            <span className="text-foreground">Upload Progress</span>
                            <span className="text-primary font-bold">{Math.round(uploadProgress)}%</span>
                          </div>
                          <div className="relative h-2 bg-muted rounded-full overflow-hidden">
                            <div 
                              className="absolute top-0 left-0 h-full bg-gradient-to-r from-primary to-secondary transition-all duration-300 ease-out"
                              style={{ width: `${uploadProgress}%` }}
                            />
                            <div className="absolute top-0 left-0 h-full w-full bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer" />
                          </div>
                          <div className="flex items-center gap-2 text-sm text-muted-foreground">
                            <Cloud className="h-4 w-4 animate-bounce" />
                            <span>Uploading to server...</span>
                          </div>
                        </div>
                      )}
                      
                      <div className="flex items-center gap-2 text-sm text-red-600 font-medium">
                        <AlertCircle className="h-4 w-4" />
                        <span>📸 Product photo is required before saving</span>
                      </div>
                    </div>
                  )}
                  
                  {formData.image_url && (
                    <div className="space-y-4">
                      <div className="flex items-center gap-2 text-sm text-green-600 font-medium mb-4">
                        <CheckCircle className="h-4 w-4" />
                        <span>✅ Image uploaded successfully!</span>
                      </div>
                      
                      <div className="relative group">
                        <img 
                          src={formData.image_url} 
                          alt="Product preview" 
                          className="w-full max-w-md h-48 object-cover rounded-lg border-2 border-border shadow-md"
                        />
                        <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-200 rounded-lg flex items-center justify-center">
                          <Button
                            type="button"
                            variant="destructive"
                            size="sm"
                            onClick={() => setFormData(prev => ({ ...prev, image_url: '' }))}
                            className="bg-red-600 hover:bg-red-700"
                          >
                            <Trash2 className="h-4 w-4 mr-2" />
                            Change Image
                          </Button>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Step 6: Special Settings */}
                <div className="bg-muted/50 rounded-lg p-6">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="bg-primary text-primary-foreground rounded-full w-8 h-8 flex items-center justify-center font-bold">6</div>
                    <h3 className="text-lg font-semibold">Special settings (optional)</h3>
                  </div>
                  <div className="space-y-4">
                    <label className="flex items-center gap-3 cursor-pointer p-3 rounded-lg border border-border hover:bg-muted/50 transition-colors">
                      <input
                        type="checkbox"
                        checked={formData.is_featured}
                        onChange={(e) => setFormData(prev => ({ ...prev, is_featured: e.target.checked }))}
                        className="w-5 h-5 rounded border-gray-300"
                      />
                      <div>
                        <div className="flex items-center gap-2 font-medium text-foreground">
                          <Star className="h-4 w-4 text-secondary" />
                          Featured Product
                        </div>
                        <p className="text-sm text-muted-foreground">⭐ Make this product stand out to customers</p>
                      </div>
                    </label>
                    
                    <label className="flex items-center gap-3 cursor-pointer p-3 rounded-lg border border-border hover:bg-muted/50 transition-colors">
                      <input
                        type="checkbox"
                        checked={formData.is_available}
                        onChange={(e) => setFormData(prev => ({ ...prev, is_available: e.target.checked }))}
                        className="w-5 h-5 rounded border-gray-300"
                      />
                      <div>
                        <div className="flex items-center gap-2 font-medium text-foreground">
                          <CheckCircle className="h-4 w-4 text-green-500" />
                          Available for Sale
                        </div>
                        <p className="text-sm text-muted-foreground">✅ Customers can contact you about this product</p>
                      </div>
                    </label>
                  </div>
                </div>

                {/* Submit Buttons */}
                <div className="flex flex-col sm:flex-row gap-4 pt-6 border-t border-border">
                  <Button 
                    type="submit" 
                    size="lg"
                    className="bg-primary hover:bg-primary/90 text-lg px-8"
                    disabled={!formData.name || !formData.description || !formData.price || !formData.category_id || !formData.image_url || uploading}
                  >
                    {uploading ? (
                      <>
                        <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                        Uploading Image...
                      </>
                    ) : (
                      <>
                        <Save className="mr-2 h-5 w-5" />
                        {editingProduct ? '✏️ Update Product' : '➕ Add Product'}
                      </>
                    )}
                  </Button>
                  <Button type="button" variant="outline" size="lg" onClick={resetForm} className="text-lg px-8" disabled={uploading}>
                    ❌ Cancel
                  </Button>
                  
                  {(!formData.image_url && !uploading) && (
                    <div className="flex items-center gap-2 text-sm text-red-600">
                      <AlertCircle className="h-4 w-4" />
                      <span>Image upload is required to save product</span>
                    </div>
                  )}
                </div>
              </form>
            </CardContent>
          </Card>
        )}

        {/* Your Products */}
        {products.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold text-foreground mb-6 flex items-center gap-2">
              📦 Your Products ({products.length})
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {products.map((product) => (
                <Card key={product.id} className="overflow-hidden border-2 hover:border-primary/30 transition-all">
                  <div className="flex">
                    {/* Product Image */}
                    <div className="w-1/3 h-32">
                      {product.image_url ? (
                        <img 
                          src={product.image_url} 
                          alt={product.name}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="w-full h-full bg-muted flex items-center justify-center">
                          <ImageIcon className="h-8 w-8 text-muted-foreground" />
                        </div>
                      )}
                    </div>
                    
                    {/* Product Info */}
                    <CardContent className="flex-1 p-4">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="font-bold text-foreground text-lg">{product.name}</h3>
                        <div className="flex gap-1">
                          {product.is_featured && (
                            <Badge className="bg-secondary text-secondary-foreground text-xs">
                              ⭐ Featured
                            </Badge>
                          )}
                        </div>
                      </div>
                      
                      <p className="text-sm text-muted-foreground mb-3 line-clamp-2">
                        {product.description}
                      </p>
                      
                      <div className="flex items-center justify-between mb-3">
                        <div className="font-bold text-primary text-lg">
                          {product.price}
                        </div>
                        <Badge variant={product.is_available ? "default" : "secondary"}>
                          {product.is_available ? '✅ Available' : '❌ Sold Out'}
                        </Badge>
                      </div>
                      
                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleEdit(product)}
                          className="flex-1"
                        >
                          <Edit2 className="mr-2 h-4 w-4" />
                          Edit
                        </Button>
                        <Button
                          size="sm" 
                          variant="outline"
                          onClick={() => handleDelete(product.id)}
                          className="text-red-600 hover:text-red-700 hover:border-red-300"
                        >
                          <Trash2 className="mr-2 h-4 w-4" />
                          Delete
                        </Button>
                      </div>
                    </CardContent>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {products.length === 0 && !showAddForm && (
          <Card className="border-2 border-dashed border-primary/30 bg-primary/5">
            <CardContent className="p-12 text-center">
              <Package className="h-20 w-20 text-primary mx-auto mb-6" />
              <h3 className="text-2xl font-bold text-foreground mb-3">No products added yet</h3>
              <p className="text-lg text-muted-foreground mb-6 max-w-md mx-auto">
                Start building your product catalog! Add your first product to show customers what you have available.
              </p>
              <Button 
                size="lg"
                onClick={() => setShowAddForm(true)} 
                className="bg-primary hover:bg-primary/90 text-lg px-8"
              >
                <Plus className="mr-2 h-6 w-6" />
                Add Your First Product
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default AdminManager;
import React from 'react';
import { Card, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { 
  Shield, Globe, Package, Truck, Award, Clock, 
  CheckCircle, Star, Users, HeadphonesIcon,
  MapPin, FileText, Zap
} from 'lucide-react';
import { whyChooseUs, companyInfo, testimonials } from '../mock';

const WhyChooseUs = () => {
  const advantages = [
    {
      icon: Shield,
      title: 'RAKEZ Licensed & Regulated',
      description: 'Fully licensed by Ras Al Khaimah Economic Zone with transparent business operations and legal compliance.',
      details: ['License No: 5034384', 'Full regulatory compliance', 'Transparent business practices']
    },
    {
      icon: Globe,
      title: 'Global Export Network',
      description: 'Established shipping partnerships and logistics networks covering major international markets.',
      details: ['25+ countries served', 'Major shipping lines partnership', 'Full tracking & insurance']
    },
    {
      icon: Package,
      title: 'Comprehensive Product Range',
      description: 'One-stop solution for all automotive and construction equipment needs with extensive inventory.',
      details: ['Passenger vehicles', 'Auto spare parts', 'Heavy machinery', 'Construction equipment']
    },
    {
      icon: Truck,
      title: 'Reliable Supply Chain',
      description: 'Trusted supplier relationships and efficient logistics ensure consistent availability and fast delivery.',
      details: ['Direct manufacturer relationships', 'Strategic inventory management', 'Express shipping options']
    }
  ];

  const certifications = [
    { title: 'RAKEZ Authorized', icon: Award, description: 'Official trading license from UAE authorities' },
    { title: 'ISO Standards', icon: CheckCircle, description: 'Quality management systems compliance' },
    { title: '24/7 Support', icon: HeadphonesIcon, description: 'Round-the-clock customer service' },
    { title: 'Fast Processing', icon: Zap, description: 'Quick order processing and dispatch' }
  ];

  const stats = [
    { number: '500+', label: 'Vehicles Traded', icon: Package },
    { number: '1000+', label: 'Parts Delivered', icon: Truck },
    { number: '25+', label: 'Countries Served', icon: Globe },
    { number: '99%', label: 'Client Satisfaction', icon: Star }
  ];

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-slate-900 to-slate-800 text-white py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <Badge className="mb-6 bg-blue-600 hover:bg-blue-700 text-white">
              Your Trusted Trading Partner
            </Badge>
            <h1 className="text-4xl lg:text-5xl font-bold mb-6">
              Why Choose Sun Star International?
            </h1>
            <p className="text-xl text-slate-300 max-w-3xl mx-auto">
              Discover what makes us the preferred choice for automotive and construction equipment trading across the Middle East and beyond.
            </p>
          </div>
        </div>
      </section>

      {/* Key Statistics */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center group">
                <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-blue-600 group-hover:text-white transition-colors">
                  <stat.icon className="h-8 w-8 text-blue-600 group-hover:text-white" />
                </div>
                <div className="text-3xl font-bold text-slate-800 mb-2">{stat.number}</div>
                <div className="text-slate-600 font-medium">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Main Advantages */}
      <section className="py-16 bg-slate-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-slate-800 mb-4">
              Our Competitive Advantages
            </h2>
            <p className="text-xl text-slate-600 max-w-3xl mx-auto">
              We combine legal compliance, global reach, and operational excellence to deliver unmatched value to our clients.
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {advantages.map((advantage, index) => (
              <Card key={index} className="group hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                <CardContent className="p-8">
                  <div className="flex items-start gap-4">
                    <div className="bg-blue-100 p-3 rounded-lg group-hover:bg-blue-600 transition-colors">
                      <advantage.icon className="h-8 w-8 text-blue-600 group-hover:text-white" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-slate-800 mb-3">
                        {advantage.title}
                      </h3>
                      <p className="text-slate-600 mb-4">
                        {advantage.description}
                      </p>
                      <ul className="space-y-2">
                        {advantage.details.map((detail, idx) => (
                          <li key={idx} className="flex items-center gap-2 text-sm text-slate-600">
                            <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0" />
                            {detail}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Certifications & Quality */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-slate-800 mb-4">
              Certifications & Quality Assurance
            </h2>
            <p className="text-xl text-slate-600">
              Our commitment to excellence is backed by official certifications and quality standards
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {certifications.map((cert, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                <CardContent className="p-6">
                  <div className="bg-emerald-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <cert.icon className="h-8 w-8 text-emerald-600" />
                  </div>
                  <h3 className="font-bold text-slate-800 mb-2">{cert.title}</h3>
                  <p className="text-sm text-slate-600">{cert.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Process & Timeline */}
      <section className="py-16 bg-slate-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-slate-800 mb-4">
              Our Streamlined Process
            </h2>
            <p className="text-xl text-slate-600">
              From inquiry to delivery - experience our efficient trading process
            </p>
          </div>
          
          <div className="max-w-4xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              {[
                { step: '01', title: 'Inquiry', desc: 'Share your requirements via phone, email, or contact form', icon: FileText },
                { step: '02', title: 'Quote', desc: 'Receive competitive pricing and detailed specifications within 24 hours', icon: Clock },
                { step: '03', title: 'Order', desc: 'Confirm your order with our secure payment and documentation process', icon: CheckCircle },
                { step: '04', title: 'Delivery', desc: 'Track your shipment from our facility to your destination worldwide', icon: Truck }
              ].map((process, index) => (
                <div key={index} className="text-center relative">
                  {index < 3 && (
                    <div className="hidden md:block absolute top-8 left-full w-full h-0.5 bg-blue-200 -translate-x-1/2 z-0" />
                  )}
                  <div className="relative z-10">
                    <div className="bg-blue-600 text-white w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 font-bold text-lg">
                      {process.step}
                    </div>
                    <div className="bg-blue-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 -mt-8">
                      <process.icon className="h-6 w-6 text-blue-600" />
                    </div>
                    <h3 className="font-bold text-slate-800 mb-2">{process.title}</h3>
                    <p className="text-sm text-slate-600">{process.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-slate-800 mb-4">
              Client Success Stories
            </h2>
            <p className="text-xl text-slate-600">
              See what our satisfied clients say about working with us
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {testimonials.map((testimonial) => (
              <Card key={testimonial.id} className="hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-center gap-2 mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="h-4 w-4 text-yellow-400 fill-current" />
                    ))}
                  </div>
                  <p className="text-slate-600 mb-6 italic">"{testimonial.text}"</p>
                  <div>
                    <div className="font-semibold text-slate-800">{testimonial.name}</div>
                    <div className="text-sm text-slate-600">{testimonial.company}</div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-blue-600 to-blue-700 text-white">
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl lg:text-4xl font-bold mb-6">
              Ready to Experience the Sun Star Difference?
            </h2>
            <p className="text-xl mb-8 opacity-90">
              Join hundreds of satisfied clients who trust us for their automotive and construction equipment needs.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" variant="secondary" className="text-lg px-8">
                Start Your Order
              </Button>
              <Button size="lg" variant="outline" className="text-lg px-8 border-white text-white hover:bg-white hover:text-blue-600">
                Schedule Consultation
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default WhyChooseUs;
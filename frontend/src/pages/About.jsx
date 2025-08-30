import React from 'react';
import { Card, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Shield, Target, Award, Users, Globe2, Truck, CheckCircle } from 'lucide-react';
import { useCompanyInfo } from '../hooks/useApi';

const About = () => {
  const { data: companyInfo } = useCompanyInfo();

  const values = [
    {
      icon: Shield,
      title: 'Trust',
      description: 'Building lasting relationships through transparency and reliability in every transaction.'
    },
    {
      icon: Target,
      title: 'Reliability',
      description: 'Consistent quality and dependable service that our clients can count on.'
    },
    {
      icon: Award,
      title: 'Speed',
      description: 'Quick response times and efficient delivery to meet your business needs.'
    }
  ];

  const achievements = [
    { metric: '500+', label: 'Vehicles Traded' },
    { metric: '1000+', label: 'Parts Delivered' },
    { metric: '50+', label: 'Heavy Machinery Units' },
    { metric: '25+', label: 'Countries Served' }
  ];

  const licenses = [
    'New Passenger Motor Vehicles Trading',
    'Heavy Equipment & Machinery Spare Parts Trading', 
    'Auto Spare Parts & Components Trading',
    'Construction Equipment & Machinery Trading'
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-card to-background text-foreground py-20 border-b border-border">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <Badge className="mb-6 bg-primary hover:bg-primary/90 text-primary-foreground">
              RAKEZ Licensed • Established 2025
            </Badge>
            <h1 className="text-4xl lg:text-5xl font-bold mb-6">
              About Sun Star International
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              A professionally licensed trading company specializing in automotive and construction equipment solutions across the Middle East and global markets.
            </p>
          </div>
        </div>
      </section>

      {/* Company Overview */}
      <section className="py-16 bg-card">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-foreground mb-6">
                Licensed Excellence in Trading
              </h2>
              <p className="text-lg text-muted-foreground mb-6">
                Sun Star International FZ-LLC is a fully licensed trading company operating from the prestigious Ras Al Khaimah Economic Zone (RAKEZ) in the United Arab Emirates. We specialize in connecting global markets with high-quality automotive vehicles, spare parts, and heavy construction equipment.
              </p>
              <p className="text-lg text-muted-foreground mb-8">
                Our mission is to bridge the gap between manufacturers and end-users by providing reliable, cost-effective trading solutions that meet the diverse needs of our international clientele.
              </p>
              
              <div className="grid grid-cols-2 gap-6">
                {achievements.map((achievement, index) => (
                  <div key={index} className="text-center">
                    <div className="text-3xl font-bold text-primary mb-2">
                      {achievement.metric}
                    </div>
                    <div className="text-sm text-muted-foreground font-medium">
                      {achievement.label}
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div>
              <Card className="bg-muted border-0 shadow-lg">
                <CardContent className="p-8">
                  <div className="text-center mb-6">
                    <Shield className="h-16 w-16 text-primary mx-auto mb-4" />
                    <h3 className="text-xl font-bold text-foreground mb-2">
                      RAKEZ Licensed Company
                    </h3>
                    <Badge variant="outline" className="text-primary border-primary">
                      License No: {companyInfo.licenseNo}
                    </Badge>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="text-center">
                      <div className="font-semibold text-slate-800">Manager</div>
                      <div className="text-slate-600">{companyInfo.manager}</div>
                    </div>
                    
                    <div className="text-center">
                      <div className="font-semibold text-slate-800">License Period</div>
                      <div className="text-slate-600">
                        {companyInfo.license.issueDate} to {companyInfo.license.expiryDate}
                      </div>
                    </div>
                    
                    <div className="text-center pt-4">
                      <div className="font-semibold text-slate-800 mb-3">Authorized Activities</div>
                      <div className="space-y-2">
                        {licenses.map((license, index) => (
                          <div key={index} className="flex items-center gap-2 text-sm text-slate-600">
                            <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0" />
                            <span>{license}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Mission & Vision */}
      <section className="py-16 bg-muted">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-foreground mb-4">
              Our Mission & Values
            </h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Driving excellence through principled business practices and unwavering commitment to quality.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {values.map((value, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                <CardContent className="p-8">
                  <div className="bg-primary/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                    <value.icon className="h-8 w-8 text-primary" />
                  </div>
                  <h3 className="text-xl font-bold text-foreground mb-4">
                    {value.title}
                  </h3>
                  <p className="text-muted-foreground">
                    {value.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Location & Operations */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-slate-800 mb-6">
                Strategic Location in UAE
              </h2>
              <p className="text-lg text-slate-600 mb-6">
                Located in the Al Hulaila Industrial Zone within Ras Al Khaimah Economic Zone, our strategic position provides us with excellent access to global shipping routes and trade networks.
              </p>
              
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <Globe2 className="h-6 w-6 text-blue-600 mt-1 flex-shrink-0" />
                  <div>
                    <div className="font-semibold text-slate-800">Global Trade Access</div>
                    <div className="text-slate-600">Direct access to major shipping lanes and international markets</div>
                  </div>
                </div>
                
                <div className="flex items-start gap-3">
                  <Truck className="h-6 w-6 text-blue-600 mt-1 flex-shrink-0" />
                  <div>
                    <div className="font-semibold text-slate-800">Efficient Logistics</div>
                    <div className="text-slate-600">State-of-the-art facilities for storage and distribution</div>
                  </div>
                </div>
                
                <div className="flex items-start gap-3">
                  <Users className="h-6 w-6 text-blue-600 mt-1 flex-shrink-0" />
                  <div>
                    <div className="font-semibold text-slate-800">Professional Team</div>
                    <div className="text-slate-600">Experienced professionals managing all aspects of trading operations</div>
                  </div>
                </div>
              </div>
            </div>
            
            <div>
              <Card className="overflow-hidden">
                <div className="bg-gradient-to-br from-blue-600 to-blue-700 text-white p-8">
                  <h3 className="text-xl font-bold mb-6">Our Address</h3>
                  <div className="space-y-3 text-blue-100">
                    <div>{companyInfo.address.building}</div>
                    <div>{companyInfo.address.zone}</div>
                    <div>{companyInfo.address.city}</div>
                    <div>{companyInfo.address.country}</div>
                  </div>
                </div>
                <CardContent className="p-8 bg-slate-50">
                  <div className="text-center">
                    <div className="text-sm text-slate-600 mb-4">
                      Operating under RAKEZ jurisdiction since August 2025
                    </div>
                    <Badge className="bg-green-100 text-green-700">
                      Fully Licensed & Compliant
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;
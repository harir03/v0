import { InterfaceSpec, ComponentSpec } from '@/types/builder'

/**
 * Advanced Template System
 * Professional templates for SaaS, e-commerce, portfolios, and more
 */
export class TemplateLibrary {
  /**
   * Get all available templates
   */
  getTemplates(): TemplateCategory[] {
    return [
      {
        id: 'saas',
        name: 'SaaS & Software',
        description: 'Modern SaaS landing pages and app interfaces',
        templates: this.getSaaSTemplates()
      },
      {
        id: 'ecommerce',
        name: 'E-commerce',
        description: 'Product showcases and online store layouts',
        templates: this.getEcommerceTemplates()
      },
      {
        id: 'portfolio',
        name: 'Portfolio & Agency',
        description: 'Creative portfolios and agency websites',
        templates: this.getPortfolioTemplates()
      },
      {
        id: 'business',
        name: 'Business & Corporate',
        description: 'Professional business and corporate sites',
        templates: this.getBusinessTemplates()
      },
      {
        id: 'startup',
        name: 'Startup & Tech',
        description: 'Modern startup and technology company sites',
        templates: this.getStartupTemplates()
      }
    ]
  }

  /**
   * Get template by ID
   */
  getTemplate(templateId: string): Template | null {
    const allTemplates = this.getTemplates().flatMap(cat => cat.templates)
    return allTemplates.find(t => t.id === templateId) || null
  }

  /**
   * Generate interface spec from template
   */
  generateSpecFromTemplate(templateId: string, customizations?: TemplateCustomizations): InterfaceSpec {
    const template = this.getTemplate(templateId)
    if (!template) {
      throw new Error(`Template ${templateId} not found`)
    }

    return {
      id: `${templateId}-${Date.now()}`,
      name: customizations?.name || template.name,
      type: 'page',
      components: this.customizeComponents(template.components, customizations),
      theme: customizations?.theme || template.defaultTheme,
      metadata: {
        description: template.description,
        tags: template.tags,
        version: '1.0.0'
      }
    }
  }

  // SaaS Templates
  private getSaaSTemplates(): Template[] {
    return [
      {
        id: 'saas-modern',
        name: 'Modern SaaS Platform',
        description: 'Clean, professional SaaS landing page with feature highlights',
        tags: ['saas', 'software', 'b2b'],
        preview: '/templates/saas-modern.png',
        components: [
          this.createHeroComponent({
            title: 'The All-in-One Platform for Modern Teams',
            subtitle: 'Streamline your workflow, boost productivity, and scale your business with our comprehensive SaaS solution.',
            ctaText: 'Start Free Trial',
            features: ['14-day free trial', 'No credit card required', 'Cancel anytime']
          }),
          this.createFeaturesComponent({
            title: 'Everything you need to succeed',
            subtitle: 'Powerful features designed for modern businesses',
            features: [
              {
                title: 'Real-time Collaboration',
                description: 'Work together seamlessly with your team across any device, anywhere in the world.',
                icon: 'users'
              },
              {
                title: 'Advanced Analytics',
                description: 'Get deep insights into your business with comprehensive reporting and analytics.',
                icon: 'chart'
              },
              {
                title: 'Enterprise Security',
                description: 'Bank-level security with SOC 2 compliance and end-to-end encryption.',
                icon: 'shield'
              }
            ]
          }),
          this.createPricingComponent({
            title: 'Simple, Transparent Pricing',
            plans: [
              {
                name: 'Starter',
                price: '$29',
                period: 'month',
                features: ['Up to 5 users', 'Basic analytics', 'Email support'],
                highlighted: false
              },
              {
                name: 'Professional',
                price: '$99',
                period: 'month',
                features: ['Up to 25 users', 'Advanced analytics', 'Priority support', 'Custom integrations'],
                highlighted: true
              },
              {
                name: 'Enterprise',
                price: 'Custom',
                period: '',
                features: ['Unlimited users', 'Custom features', 'Dedicated support', 'On-premise deployment'],
                highlighted: false
              }
            ]
          }),
          this.createCTAComponent({
            title: 'Ready to transform your business?',
            subtitle: 'Join thousands of companies already using our platform',
            ctaText: 'Get Started Today'
          })
        ],
        defaultTheme: {
          primaryColor: '#2563eb',
          secondaryColor: '#7c3aed',
          accentColor: '#06b6d4',
          backgroundColor: '#ffffff',
          textColor: '#1f2937',
          fontFamily: 'Inter'
        }
      },
      {
        id: 'saas-dashboard',
        name: 'SaaS Dashboard Preview',
        description: 'Showcase your SaaS product with an interactive dashboard preview',
        tags: ['saas', 'dashboard', 'analytics'],
        preview: '/templates/saas-dashboard.png',
        components: [
          this.createHeroComponent({
            title: 'Analytics That Drive Results',
            subtitle: 'Transform your data into actionable insights with our powerful analytics platform.',
            ctaText: 'View Demo',
            variant: 'dashboard'
          }),
          this.createDashboardComponent(),
          this.createFeaturesComponent({
            title: 'Powerful Analytics Features',
            layout: 'grid',
            features: [
              {
                title: 'Real-time Data',
                description: 'Monitor your metrics as they happen',
                icon: 'activity'
              },
              {
                title: 'Custom Dashboards',
                description: 'Build dashboards tailored to your needs',
                icon: 'layout'
              },
              {
                title: 'Team Collaboration',
                description: 'Share insights across your organization',
                icon: 'share'
              },
              {
                title: 'API Integration',
                description: 'Connect with your existing tools',
                icon: 'link'
              }
            ]
          })
        ],
        defaultTheme: {
          primaryColor: '#059669',
          secondaryColor: '#3b82f6',
          accentColor: '#f59e0b',
          backgroundColor: '#ffffff',
          textColor: '#111827',
          fontFamily: 'Inter'
        }
      }
    ]
  }

  // E-commerce Templates
  private getEcommerceTemplates(): Template[] {
    return [
      {
        id: 'ecommerce-fashion',
        name: 'Fashion Store',
        description: 'Elegant e-commerce site for fashion and lifestyle brands',
        tags: ['ecommerce', 'fashion', 'retail'],
        preview: '/templates/ecommerce-fashion.png',
        components: [
          this.createHeroComponent({
            title: 'New Collection',
            subtitle: 'Discover the latest trends in sustainable fashion',
            ctaText: 'Shop Now',
            backgroundImage: true,
            variant: 'image-overlay'
          }),
          this.createProductGridComponent(),
          this.createFeaturesComponent({
            title: 'Why Choose Us',
            features: [
              {
                title: 'Sustainable Materials',
                description: 'Ethically sourced, eco-friendly fabrics',
                icon: 'leaf'
              },
              {
                title: 'Free Shipping',
                description: 'Free delivery on orders over $100',
                icon: 'truck'
              },
              {
                title: '30-Day Returns',
                description: 'Easy returns and exchanges',
                icon: 'refresh'
              }
            ]
          })
        ],
        defaultTheme: {
          primaryColor: '#1f2937',
          secondaryColor: '#f59e0b',
          accentColor: '#ef4444',
          backgroundColor: '#ffffff',
          textColor: '#374151',
          fontFamily: 'Playfair Display'
        }
      }
    ]
  }

  // Portfolio Templates
  private getPortfolioTemplates(): Template[] {
    return [
      {
        id: 'portfolio-creative',
        name: 'Creative Portfolio',
        description: 'Showcase your creative work with this modern portfolio design',
        tags: ['portfolio', 'creative', 'designer'],
        preview: '/templates/portfolio-creative.png',
        components: [
          this.createHeroComponent({
            title: 'Creative Designer',
            subtitle: 'Crafting beautiful experiences through thoughtful design',
            ctaText: 'View Work',
            variant: 'minimal'
          }),
          this.createPortfolioGridComponent(),
          this.createAboutComponent(),
          this.createContactComponent()
        ],
        defaultTheme: {
          primaryColor: '#7c3aed',
          secondaryColor: '#f59e0b',
          accentColor: '#06b6d4',
          backgroundColor: '#ffffff',
          textColor: '#1f2937',
          fontFamily: 'Inter'
        }
      }
    ]
  }

  // Business Templates
  private getBusinessTemplates(): Template[] {
    return [
      {
        id: 'business-consulting',
        name: 'Business Consulting',
        description: 'Professional website for consulting and service businesses',
        tags: ['business', 'consulting', 'professional'],
        preview: '/templates/business-consulting.png',
        components: [
          this.createHeroComponent({
            title: 'Transform Your Business',
            subtitle: 'Expert consulting services to help you achieve sustainable growth and operational excellence.',
            ctaText: 'Schedule Consultation'
          }),
          this.createServicesComponent(),
          this.createTestimonialsComponent(),
          this.createCTAComponent({
            title: 'Ready to take your business to the next level?',
            subtitle: 'Let\'s discuss how we can help you achieve your goals',
            ctaText: 'Contact Us Today'
          })
        ],
        defaultTheme: {
          primaryColor: '#1e40af',
          secondaryColor: '#059669',
          accentColor: '#dc2626',
          backgroundColor: '#ffffff',
          textColor: '#1f2937',
          fontFamily: 'Inter'
        }
      }
    ]
  }

  // Startup Templates
  private getStartupTemplates(): Template[] {
    return [
      {
        id: 'startup-tech',
        name: 'Tech Startup',
        description: 'Modern landing page for technology startups and innovations',
        tags: ['startup', 'tech', 'innovation'],
        preview: '/templates/startup-tech.png',
        components: [
          this.createHeroComponent({
            title: 'The Future of Technology',
            subtitle: 'Revolutionary solutions that transform how businesses operate in the digital age.',
            ctaText: 'Join Waitlist',
            variant: 'gradient'
          }),
          this.createFeaturesComponent({
            title: 'Built for Tomorrow',
            features: [
              {
                title: 'AI-Powered',
                description: 'Leverage artificial intelligence for smarter decisions',
                icon: 'brain'
              },
              {
                title: 'Scalable',
                description: 'Grows with your business from startup to enterprise',
                icon: 'trending-up'
              },
              {
                title: 'Secure',
                description: 'Enterprise-grade security built from the ground up',
                icon: 'lock'
              }
            ]
          }),
          this.createCTAComponent({
            title: 'Be part of the revolution',
            subtitle: 'Get early access and help shape the future',
            ctaText: 'Get Early Access'
          })
        ],
        defaultTheme: {
          primaryColor: '#6366f1',
          secondaryColor: '#8b5cf6',
          accentColor: '#06b6d4',
          backgroundColor: '#0f172a',
          textColor: '#f8fafc',
          fontFamily: 'Inter'
        }
      }
    ]
  }

  // Helper methods to create specific components
  private createHeroComponent(props: any): ComponentSpec {
    return {
      id: `hero-${Date.now()}`,
      type: 'hero',
      props
    }
  }

  private createFeaturesComponent(props: any): ComponentSpec {
    return {
      id: `features-${Date.now()}`,
      type: 'features',
      props
    }
  }

  private createPricingComponent(props: any): ComponentSpec {
    return {
      id: `pricing-${Date.now()}`,
      type: 'pricing',
      props
    }
  }

  private createCTAComponent(props: any): ComponentSpec {
    return {
      id: `cta-${Date.now()}`,
      type: 'cta',
      props
    }
  }

  private createDashboardComponent(): ComponentSpec {
    return {
      id: `dashboard-${Date.now()}`,
      type: 'dashboard',
      props: {
        title: 'Live Analytics Dashboard',
        metrics: [
          { label: 'Revenue', value: '$47,329', change: '+12%' },
          { label: 'Users', value: '2,847', change: '+8%' },
          { label: 'Conversion', value: '3.24%', change: '+0.4%' }
        ]
      }
    }
  }

  private createProductGridComponent(): ComponentSpec {
    return {
      id: `products-${Date.now()}`,
      type: 'product-grid',
      props: {
        title: 'Featured Products',
        products: [
          { name: 'Product 1', price: '$99', image: '/product1.jpg' },
          { name: 'Product 2', price: '$149', image: '/product2.jpg' },
          { name: 'Product 3', price: '$199', image: '/product3.jpg' }
        ]
      }
    }
  }

  private createPortfolioGridComponent(): ComponentSpec {
    return {
      id: `portfolio-${Date.now()}`,
      type: 'portfolio-grid',
      props: {
        title: 'Selected Work',
        projects: [
          { title: 'Project 1', category: 'Web Design', image: '/project1.jpg' },
          { title: 'Project 2', category: 'Branding', image: '/project2.jpg' },
          { title: 'Project 3', category: 'Mobile App', image: '/project3.jpg' }
        ]
      }
    }
  }

  private createAboutComponent(): ComponentSpec {
    return {
      id: `about-${Date.now()}`,
      type: 'about',
      props: {
        title: 'About Me',
        description: 'I\'m a passionate designer with over 5 years of experience creating beautiful, functional designs.',
        image: '/about.jpg'
      }
    }
  }

  private createContactComponent(): ComponentSpec {
    return {
      id: `contact-${Date.now()}`,
      type: 'contact',
      props: {
        title: 'Let\'s Work Together',
        subtitle: 'Ready to start your project?',
        email: 'hello@example.com'
      }
    }
  }

  private createServicesComponent(): ComponentSpec {
    return {
      id: `services-${Date.now()}`,
      type: 'services',
      props: {
        title: 'Our Services',
        services: [
          {
            title: 'Strategy Consulting',
            description: 'Develop winning strategies for sustainable growth',
            icon: 'target'
          },
          {
            title: 'Process Optimization',
            description: 'Streamline operations for maximum efficiency',
            icon: 'settings'
          },
          {
            title: 'Change Management',
            description: 'Navigate organizational transformation successfully',
            icon: 'arrow-right'
          }
        ]
      }
    }
  }

  private createTestimonialsComponent(): ComponentSpec {
    return {
      id: `testimonials-${Date.now()}`,
      type: 'testimonials',
      props: {
        title: 'What Our Clients Say',
        testimonials: [
          {
            quote: 'Their expertise transformed our business operations completely.',
            author: 'John Smith',
            company: 'Tech Corp',
            avatar: '/avatar1.jpg'
          }
        ]
      }
    }
  }

  private customizeComponents(components: ComponentSpec[], customizations?: TemplateCustomizations): ComponentSpec[] {
    if (!customizations) return components

    return components.map(component => ({
      ...component,
      props: {
        ...component.props,
        ...customizations.componentOverrides?.[component.type]
      }
    }))
  }
}

// Type definitions
export interface TemplateCategory {
  id: string
  name: string
  description: string
  templates: Template[]
}

export interface Template {
  id: string
  name: string
  description: string
  tags: string[]
  preview: string
  components: ComponentSpec[]
  defaultTheme: any
}

export interface TemplateCustomizations {
  name?: string
  theme?: any
  componentOverrides?: Record<string, any>
}
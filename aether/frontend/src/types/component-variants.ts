export interface ComponentVariant {
  id: string
  name: string
  description: string
  preview: string // Preview image or description
  props: Record<string, any>
  styling?: ComponentVariantStyling
}

export interface ComponentVariantStyling {
  background?: string
  textColor?: string
  accentColor?: string
  layout?: 'left' | 'center' | 'right' | 'grid' | 'flex'
  size?: 'sm' | 'md' | 'lg' | 'xl'
  spacing?: 'tight' | 'normal' | 'loose'
  borderRadius?: 'none' | 'sm' | 'md' | 'lg' | 'full'
}

export interface ComponentVariantLibrary {
  [componentType: string]: ComponentVariant[]
}

// Component Variants Library
export const COMPONENT_VARIANTS: ComponentVariantLibrary = {
  hero: [
    {
      id: 'hero-centered',
      name: 'Centered Hero',
      description: 'Clean, centered layout with large headline',
      preview: 'Centered text with prominent CTA button',
      props: {
        layout: 'center',
        titleSize: 'text-6xl',
        subtitleSize: 'text-xl',
        showBackgroundImage: false
      },
      styling: {
        background: 'gradient-to-br from-blue-50 to-indigo-100',
        textColor: 'text-gray-900',
        layout: 'center',
        size: 'lg',
        spacing: 'normal'
      }
    },
    {
      id: 'hero-split',
      name: 'Split Layout Hero',
      description: 'Two-column layout with image on right',
      preview: 'Text on left, visual content on right',
      props: {
        layout: 'split',
        titleSize: 'text-5xl',
        subtitleSize: 'text-lg',
        showBackgroundImage: true,
        imagePosition: 'right'
      },
      styling: {
        background: 'bg-white',
        textColor: 'text-gray-900',
        layout: 'left',
        size: 'lg',
        spacing: 'loose'
      }
    },
    {
      id: 'hero-minimal',
      name: 'Minimal Hero',
      description: 'Clean, minimal design with subtle accents',
      preview: 'Simple, elegant layout with minimal elements',
      props: {
        layout: 'center',
        titleSize: 'text-4xl',
        subtitleSize: 'text-base',
        showBackgroundImage: false,
        minimalist: true
      },
      styling: {
        background: 'bg-gray-50',
        textColor: 'text-gray-800',
        layout: 'center',
        size: 'md',
        spacing: 'tight'
      }
    },
    {
      id: 'hero-gradient',
      name: 'Gradient Hero',
      description: 'Bold gradient background with dynamic effects',
      preview: 'Vibrant gradient with animated elements',
      props: {
        layout: 'center',
        titleSize: 'text-6xl',
        subtitleSize: 'text-xl',
        showBackgroundImage: false,
        gradient: true
      },
      styling: {
        background: 'gradient-to-r from-purple-600 via-blue-600 to-indigo-600',
        textColor: 'text-white',
        layout: 'center',
        size: 'xl',
        spacing: 'loose'
      }
    }
  ],
  navbar: [
    {
      id: 'navbar-centered',
      name: 'Centered Navigation',
      description: 'Logo and menu items centered',
      preview: 'Centered logo with navigation items',
      props: {
        layout: 'center',
        showLogo: true,
        ctaButton: true,
        transparent: false
      },
      styling: {
        background: 'bg-white border-b',
        textColor: 'text-gray-900',
        layout: 'center',
        size: 'md',
        spacing: 'normal'
      }
    },
    {
      id: 'navbar-spread',
      name: 'Spread Navigation',
      description: 'Logo on left, menu items on right',
      preview: 'Logo left, navigation right with CTA',
      props: {
        layout: 'spread',
        showLogo: true,
        ctaButton: true,
        transparent: false
      },
      styling: {
        background: 'bg-white border-b',
        textColor: 'text-gray-900',
        layout: 'flex',
        size: 'md',
        spacing: 'normal'
      }
    },
    {
      id: 'navbar-transparent',
      name: 'Transparent Navigation',
      description: 'Transparent background overlay',
      preview: 'Transparent overlay navigation',
      props: {
        layout: 'spread',
        showLogo: true,
        ctaButton: true,
        transparent: true
      },
      styling: {
        background: 'bg-white/80 backdrop-blur-md',
        textColor: 'text-gray-900',
        layout: 'flex',
        size: 'md',
        spacing: 'normal'
      }
    },
    {
      id: 'navbar-minimal',
      name: 'Minimal Navigation',
      description: 'Clean, minimal design',
      preview: 'Simple navigation without borders',
      props: {
        layout: 'spread',
        showLogo: true,
        ctaButton: false,
        transparent: false,
        minimal: true
      },
      styling: {
        background: 'bg-white',
        textColor: 'text-gray-900',
        layout: 'flex',
        size: 'sm',
        spacing: 'tight'
      }
    }
  ],
  features: [
    {
      id: 'features-grid-3',
      name: '3-Column Grid',
      description: 'Three features in a row with icons',
      preview: 'Icon-based features in 3 columns',
      props: {
        columns: 3,
        showIcons: true,
        iconStyle: 'outline',
        alignment: 'center'
      },
      styling: {
        background: 'bg-white',
        textColor: 'text-gray-900',
        layout: 'grid',
        size: 'md',
        spacing: 'normal'
      }
    },
    {
      id: 'features-grid-4',
      name: '4-Column Grid',
      description: 'Four features with compact layout',
      preview: 'Compact 4-column feature grid',
      props: {
        columns: 4,
        showIcons: true,
        iconStyle: 'filled',
        alignment: 'center'
      },
      styling: {
        background: 'bg-gray-50',
        textColor: 'text-gray-900',
        layout: 'grid',
        size: 'sm',
        spacing: 'tight'
      }
    },
    {
      id: 'features-alternating',
      name: 'Alternating Layout',
      description: 'Features with alternating image/text',
      preview: 'Text and images in alternating rows',
      props: {
        columns: 1,
        showIcons: false,
        showImages: true,
        alternating: true,
        alignment: 'left'
      },
      styling: {
        background: 'bg-white',
        textColor: 'text-gray-900',
        layout: 'flex',
        size: 'lg',
        spacing: 'loose'
      }
    },
    {
      id: 'features-cards',
      name: 'Card Layout',
      description: 'Features in elevated cards',
      preview: 'Feature cards with shadows and borders',
      props: {
        columns: 3,
        showIcons: true,
        iconStyle: 'gradient',
        cardStyle: true,
        alignment: 'center'
      },
      styling: {
        background: 'bg-gray-50',
        textColor: 'text-gray-900',
        layout: 'grid',
        size: 'md',
        spacing: 'normal',
        borderRadius: 'lg'
      }
    }
  ],
  pricing: [
    {
      id: 'pricing-simple',
      name: 'Simple Pricing',
      description: 'Clean 3-tier pricing layout',
      preview: 'Three pricing tiers with features',
      props: {
        tiers: 3,
        highlightMiddle: true,
        showFeatures: true,
        billingToggle: false
      },
      styling: {
        background: 'bg-white',
        textColor: 'text-gray-900',
        layout: 'grid',
        size: 'md',
        spacing: 'normal'
      }
    },
    {
      id: 'pricing-cards',
      name: 'Card Pricing',
      description: 'Pricing tiers in elevated cards',
      preview: 'Pricing cards with shadows and highlights',
      props: {
        tiers: 3,
        highlightMiddle: true,
        showFeatures: true,
        billingToggle: true,
        cardStyle: true
      },
      styling: {
        background: 'bg-gray-50',
        textColor: 'text-gray-900',
        layout: 'grid',
        size: 'md',
        spacing: 'normal',
        borderRadius: 'lg'
      }
    },
    {
      id: 'pricing-comparison',
      name: 'Comparison Table',
      description: 'Detailed feature comparison table',
      preview: 'Feature comparison with checkmarks',
      props: {
        tiers: 3,
        highlightMiddle: true,
        showFeatures: true,
        billingToggle: true,
        tableStyle: true
      },
      styling: {
        background: 'bg-white',
        textColor: 'text-gray-900',
        layout: 'grid',
        size: 'lg',
        spacing: 'normal'
      }
    }
  ],
  cta: [
    {
      id: 'cta-centered',
      name: 'Centered CTA',
      description: 'Centered call-to-action section',
      preview: 'Centered headline with prominent button',
      props: {
        layout: 'center',
        showSubtext: true,
        buttonStyle: 'primary',
        backgroundStyle: 'gradient'
      },
      styling: {
        background: 'gradient-to-r from-blue-600 to-indigo-600',
        textColor: 'text-white',
        layout: 'center',
        size: 'lg',
        spacing: 'loose'
      }
    },
    {
      id: 'cta-split',
      name: 'Split CTA',
      description: 'Text on left, button on right',
      preview: 'Split layout with action on the side',
      props: {
        layout: 'split',
        showSubtext: true,
        buttonStyle: 'primary',
        backgroundStyle: 'solid'
      },
      styling: {
        background: 'bg-gray-900',
        textColor: 'text-white',
        layout: 'flex',
        size: 'md',
        spacing: 'normal'
      }
    },
    {
      id: 'cta-minimal',
      name: 'Minimal CTA',
      description: 'Clean, minimal call-to-action',
      preview: 'Simple layout with subtle styling',
      props: {
        layout: 'center',
        showSubtext: false,
        buttonStyle: 'outline',
        backgroundStyle: 'none'
      },
      styling: {
        background: 'bg-white border-t',
        textColor: 'text-gray-900',
        layout: 'center',
        size: 'sm',
        spacing: 'tight'
      }
    }
  ]
}
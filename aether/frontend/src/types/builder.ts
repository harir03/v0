// Interface Specification DSL Types
export interface InterfaceSpec {
  id: string
  name: string
  type: 'page' | 'component'
  components: ComponentSpec[]
  theme: ThemeSpec
  metadata?: {
    description?: string
    tags?: string[]
    version?: string
  }
}

export interface ComponentSpec {
  id: string
  type: ComponentType
  props: Record<string, any>
  children?: ComponentSpec[]
  styling?: ComponentStyling
}

export type ComponentType = 
  | 'hero'
  | 'features'
  | 'pricing' 
  | 'testimonials'
  | 'cta'
  | 'navbar'
  | 'footer'
  | 'card'
  | 'button'
  | 'text'
  | 'image'
  | 'container'
  | 'grid'
  | 'flex'
  | 'gallery'
  | 'carousel'
  | 'form'
  | 'dashboard'
  | 'product-grid'
  | 'portfolio-grid'
  | 'about'
  | 'contact'
  | 'services'

export interface ComponentStyling {
  spacing?: {
    padding?: string
    margin?: string
  }
  colors?: {
    background?: string
    text?: string
    border?: string
  }
  typography?: {
    fontSize?: string
    fontWeight?: string
    lineHeight?: string
  }
  layout?: {
    width?: string
    height?: string
    display?: string
  }
  animations?: {
    type?: string
    duration?: string
    easing?: string
  }
  responsive?: {
    mobile?: string
    tablet?: string
    desktop?: string
  }
}

export interface ThemeSpec {
  primaryColor: string
  secondaryColor?: string
  accentColor?: string
  backgroundColor: string
  textColor: string
  fontFamily: string
  borderRadius?: string
  spacing?: {
    xs: string
    sm: string
    md: string
    lg: string
    xl: string
  }
  shadows?: string | {
    sm: string
    md: string
    lg: string
  }
}

// Code Generation Types
export interface GeneratedCode {
  typescript: string
  css?: string
  dependencies: string[]
  imports: string[]
  additionalFiles?: Record<string, string> // For frameworks like Angular that need separate files
}

export interface CodeGenerationOptions {
  framework: 'next' | 'react' | 'vue' | 'svelte' | 'angular'
  styling: 'tailwind' | 'css-modules' | 'styled-components'
  typescript: boolean
  accessibility: boolean
  responsive: boolean
  version?: string // Framework version (e.g., 'vue-3', 'angular-17', 'svelte-4')
}

// Template Types
export interface Template {
  id: string
  name: string
  description: string
  category: 'landing' | 'saas' | 'ecommerce' | 'blog' | 'portfolio'
  preview: string
  spec: InterfaceSpec
  tags: string[]
}

// Verification Types
export interface VerificationResult {
  passed: boolean
  errors: VerificationError[]
  warnings: VerificationWarning[]
  performance?: PerformanceMetrics
  accessibility?: AccessibilityReport
}

export interface VerificationError {
  type: 'typescript' | 'eslint' | 'build'
  message: string
  file: string
  line?: number
  column?: number
}

export interface VerificationWarning {
  type: 'performance' | 'accessibility' | 'best-practice'
  message: string
  severity: 'low' | 'medium' | 'high'
}

export interface PerformanceMetrics {
  lcp: number // Largest Contentful Paint
  cls: number // Cumulative Layout Shift  
  fid: number // First Input Delay
  ttfb: number // Time to First Byte
}

export interface AccessibilityReport {
  violations: AccessibilityViolation[]
  score: number
  passes: number
  incomplete: number
}

export interface AccessibilityViolation {
  id: string
  impact: 'minor' | 'moderate' | 'serious' | 'critical'
  description: string
  help: string
  helpUrl: string
  tags: string[]
}
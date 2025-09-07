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
}

export interface ThemeSpec {
  primaryColor: string
  secondaryColor?: string
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
  shadows?: {
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
}

export interface CodeGenerationOptions {
  framework: 'next' | 'react' | 'vue' | 'svelte'
  styling: 'tailwind' | 'css-modules' | 'styled-components'
  typescript: boolean
  accessibility: boolean
  responsive: boolean
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
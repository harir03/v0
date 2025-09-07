import { InterfaceSpec, ComponentSpec, GeneratedCode, CodeGenerationOptions } from '@/types/builder'

/**
 * Abstract base class for framework-specific code generators
 */
export abstract class FrameworkCodeGenerator {
  protected options: CodeGenerationOptions

  constructor(options: CodeGenerationOptions) {
    this.options = options
  }

  /**
   * Generate complete page code from interface specification
   */
  abstract generatePage(spec: InterfaceSpec): GeneratedCode

  /**
   * Generate individual component code
   */
  abstract generateComponent(component: ComponentSpec, theme: any): string

  /**
   * Generate framework-specific imports
   */
  abstract generateImports(spec: InterfaceSpec): string[]

  /**
   * Generate framework-specific dependencies
   */
  abstract getDependencies(spec: InterfaceSpec): string[]

  /**
   * Generate component props interface (TypeScript)
   */
  abstract generatePropsInterface(component: ComponentSpec): string

  /**
   * Generate framework-specific event handlers
   */
  abstract generateEventHandlers(component: ComponentSpec): string

  /**
   * Generate framework-specific lifecycle hooks
   */
  abstract generateLifecycleHooks(component: ComponentSpec): string

  /**
   * Common utilities for all frameworks
   */
  protected generateTailwindClasses(component: ComponentSpec, theme: any): string {
    const baseClasses = []
    
    if (component.styling?.spacing?.padding) {
      baseClasses.push(`p-${component.styling.spacing.padding}`)
    }
    if (component.styling?.spacing?.margin) {
      baseClasses.push(`m-${component.styling.spacing.margin}`)
    }
    if (component.styling?.colors?.background) {
      baseClasses.push(`bg-${component.styling.colors.background}`)
    }
    if (component.styling?.colors?.text) {
      baseClasses.push(`text-${component.styling.colors.text}`)
    }
    
    // Apply theme colors
    if (theme?.primaryColor) {
      baseClasses.push('hover:bg-primary/10')
    }
    
    return baseClasses.join(' ')
  }

  protected generateAccessibilityAttributes(component: ComponentSpec): Record<string, string> {
    const attrs: Record<string, string> = {}
    
    if (component.props?.ariaLabel) {
      attrs['aria-label'] = component.props.ariaLabel
    }
    if (component.props?.role) {
      attrs['role'] = component.props.role
    }
    if (component.type === 'button') {
      attrs['type'] = component.props?.type || 'button'
    }
    
    return attrs
  }

  protected generateResponsiveClasses(component: ComponentSpec): string[] {
    const classes = []
    
    if (component.styling?.responsive?.mobile) {
      classes.push(`sm:${component.styling.responsive.mobile}`)
    }
    if (component.styling?.responsive?.tablet) {
      classes.push(`md:${component.styling.responsive.tablet}`)
    }
    if (component.styling?.responsive?.desktop) {
      classes.push(`lg:${component.styling.responsive.desktop}`)
    }
    
    return classes
  }
}

/**
 * Framework-agnostic component abstraction
 */
export interface FrameworkComponent {
  name: string
  props: Record<string, any>
  children?: FrameworkComponent[]
  events?: Record<string, string>
  slots?: Record<string, string> // For Vue/Angular
  bindings?: Record<string, string> // For data binding
}

/**
 * Framework-specific configuration
 */
export interface FrameworkConfig {
  name: string
  version: string
  fileExtension: string
  templateSyntax: 'jsx' | 'template' | 'html'
  stateManagement: 'hooks' | 'composition' | 'reactive' | 'rxjs'
  stylingApproach: 'classes' | 'scoped' | 'modules'
  buildTool: 'vite' | 'webpack' | 'rollup' | 'angular-cli'
}
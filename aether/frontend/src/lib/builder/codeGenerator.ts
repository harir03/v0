import { InterfaceSpec, ComponentSpec, GeneratedCode, CodeGenerationOptions } from '@/types/builder'
import { FrameworkFactory } from './frameworks/factory'
import { FrameworkCodeGenerator } from './frameworks/base'

/**
 * Core code generation engine with multi-framework support
 */
export class CodeGenerator {
  private options: CodeGenerationOptions
  private frameworkGenerator: FrameworkCodeGenerator

  constructor(options: CodeGenerationOptions = {
    framework: 'next',
    styling: 'tailwind',
    typescript: true,
    accessibility: true,
    responsive: true
  }) {
    this.options = options
    this.frameworkGenerator = FrameworkFactory.createGenerator(options)
  }

  /**
   * Generate complete page code from interface specification
   */
  generatePage(spec: InterfaceSpec): GeneratedCode {
    return this.frameworkGenerator.generatePage(spec)
  }

  /**
   * Generate individual component code
   */
  generateComponent(component: ComponentSpec, theme: any): string {
    return this.frameworkGenerator.generateComponent(component, theme)
  }

  /**
   * Get available frameworks
   */
  getAvailableFrameworks() {
    return FrameworkFactory.getAvailableFrameworks()
  }

  /**
   * Get project structure for current framework
   */
  getProjectStructure() {
    return FrameworkFactory.getProjectStructure(this.options.framework)
  }

  /**
   * Switch framework and recreate generator
   */
  switchFramework(framework: CodeGenerationOptions['framework']) {
    this.options.framework = framework
    this.frameworkGenerator = FrameworkFactory.createGenerator(this.options)
  }

  // Legacy methods for backwards compatibility
  generateImports(spec: InterfaceSpec): string[] {
    return this.frameworkGenerator.generateImports(spec)
  }

  getDependencies(spec: InterfaceSpec): string[] {
    return this.frameworkGenerator.getDependencies(spec)
  }

  generateComponents(components: ComponentSpec[]): string[] {
    return components.map(comp => this.generateComponent(comp, {}))
  }

  generateStyles(spec: InterfaceSpec): string {
    // This is a simplified implementation for backwards compatibility
    return this.frameworkGenerator.generatePage(spec).css || ''
  }

  generatePageCode(spec: InterfaceSpec, imports: string[], components: string[]): string {
    return this.frameworkGenerator.generatePage(spec).typescript
  }

  generateHeroComponent(component: ComponentSpec, theme: any): string {
    return this.frameworkGenerator.generateComponent(component, theme)
  }

  generateFeaturesComponent(component: ComponentSpec, theme: any): string {
    return this.frameworkGenerator.generateComponent(component, theme)
  }

  generatePricingComponent(component: ComponentSpec, theme: any): string {
    return this.frameworkGenerator.generateComponent(component, theme)
  }

  generateCTAComponent(component: ComponentSpec, theme: any): string {
    return this.frameworkGenerator.generateComponent(component, theme)
  }

  generateGenericComponent(component: ComponentSpec, theme: any): string {
    return this.frameworkGenerator.generateComponent(component, theme)
  }
}
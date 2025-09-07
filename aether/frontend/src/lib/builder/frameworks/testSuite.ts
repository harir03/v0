import { CodeGenerator } from '../codeGenerator'
import { FrameworkFactory } from './factory'
import { InterfaceSpec, ComponentSpec, CodeGenerationOptions } from '@/types/builder'

/**
 * Comprehensive test suite for multi-framework code generation
 */
export class MultiFrameworkTestSuite {
  
  /**
   * Run all tests for Phase 3A implementation
   */
  static async runAllTests(): Promise<TestResult[]> {
    const results: TestResult[] = []
    
    // Test each framework twice as requested
    const frameworks: CodeGenerationOptions['framework'][] = ['react', 'next', 'vue', 'svelte', 'angular']
    
    for (const framework of frameworks) {
      console.log(`🔄 Testing ${framework} (First run)...`)
      const firstRun = await this.testFramework(framework, 1)
      results.push(firstRun)
      
      console.log(`🔄 Testing ${framework} (Second run)...`)
      const secondRun = await this.testFramework(framework, 2)
      results.push(secondRun)
    }
    
    // Test framework switching
    const switchingTest = await this.testFrameworkSwitching()
    results.push(switchingTest)
    
    // Test component generation for each framework
    const componentTests = await this.testComponentGeneration()
    results.push(...componentTests)
    
    return results
  }
  
  /**
   * Test individual framework code generation
   */
  static async testFramework(framework: CodeGenerationOptions['framework'], runNumber: number): Promise<TestResult> {
    const testName = `${framework}-generation-run-${runNumber}`
    const startTime = Date.now()
    
    try {
      const options: CodeGenerationOptions = {
        framework,
        styling: 'tailwind',
        typescript: true,
        accessibility: true,
        responsive: true
      }
      
      const generator = new CodeGenerator(options)
      const testSpec = this.createTestInterfaceSpec()
      
      // Test page generation
      const generatedCode = generator.generatePage(testSpec)
      
      // Verify generated code
      this.verifyGeneratedCode(generatedCode, framework)
      
      // Test dependencies
      const dependencies = generator.getDependencies(testSpec)
      this.verifyDependencies(dependencies, framework)
      
      // Test imports
      const imports = generator.generateImports(testSpec)
      this.verifyImports(imports, framework)
      
      // Test individual components
      for (const component of testSpec.components) {
        const componentCode = generator.generateComponent(component, testSpec.theme)
        this.verifyComponentCode(componentCode, component.type, framework)
      }
      
      const endTime = Date.now()
      
      return {
        testName,
        framework,
        runNumber,
        success: true,
        duration: endTime - startTime,
        details: `Successfully generated ${framework} code with ${dependencies.length} dependencies`,
        generatedLines: this.countLines(generatedCode.typescript),
        codeSize: generatedCode.typescript.length
      }
      
    } catch (error) {
      const endTime = Date.now()
      return {
        testName,
        framework,
        runNumber,
        success: false,
        duration: endTime - startTime,
        error: error instanceof Error ? error.message : 'Unknown error',
        details: `Failed to generate ${framework} code`
      }
    }
  }
  
  /**
   * Test framework switching functionality
   */
  static async testFrameworkSwitching(): Promise<TestResult> {
    const testName = 'framework-switching'
    const startTime = Date.now()
    
    try {
      const generator = new CodeGenerator({
        framework: 'react',
        styling: 'tailwind',
        typescript: true,
        accessibility: true,
        responsive: true
      })
      
      const testSpec = this.createTestInterfaceSpec()
      const frameworks: CodeGenerationOptions['framework'][] = ['react', 'vue', 'svelte', 'angular', 'next']
      
      for (const framework of frameworks) {
        generator.switchFramework(framework)
        const code = generator.generatePage(testSpec)
        this.verifyGeneratedCode(code, framework)
      }
      
      const endTime = Date.now()
      
      return {
        testName,
        framework: 'all',
        runNumber: 1,
        success: true,
        duration: endTime - startTime,
        details: `Successfully switched between ${frameworks.length} frameworks`
      }
      
    } catch (error) {
      const endTime = Date.now()
      return {
        testName,
        framework: 'all',
        runNumber: 1,
        success: false,
        duration: endTime - startTime,
        error: error instanceof Error ? error.message : 'Unknown error',
        details: 'Failed to switch frameworks'
      }
    }
  }
  
  /**
   * Test component generation for all frameworks
   */
  static async testComponentGeneration(): Promise<TestResult[]> {
    const results: TestResult[] = []
    const componentTypes: ComponentSpec['type'][] = ['hero', 'features', 'pricing', 'cta', 'button']
    const frameworks: CodeGenerationOptions['framework'][] = ['react', 'vue', 'svelte', 'angular']
    
    for (const framework of frameworks) {
      for (const componentType of componentTypes) {
        const testName = `${framework}-${componentType}-component`
        const startTime = Date.now()
        
        try {
          const generator = new CodeGenerator({
            framework,
            styling: 'tailwind',
            typescript: true,
            accessibility: true,
            responsive: true
          })
          
          const component = this.createTestComponent(componentType)
          const componentCode = generator.generateComponent(component, this.createTestTheme())
          
          this.verifyComponentCode(componentCode, componentType, framework)
          
          const endTime = Date.now()
          
          results.push({
            testName,
            framework,
            runNumber: 1,
            success: true,
            duration: endTime - startTime,
            details: `Generated ${componentType} component for ${framework}`,
            generatedLines: this.countLines(componentCode),
            codeSize: componentCode.length
          })
          
        } catch (error) {
          const endTime = Date.now()
          results.push({
            testName,
            framework,
            runNumber: 1,
            success: false,
            duration: endTime - startTime,
            error: error instanceof Error ? error.message : 'Unknown error',
            details: `Failed to generate ${componentType} component for ${framework}`
          })
        }
      }
    }
    
    return results
  }
  
  /**
   * Verify generated code quality and structure
   */
  static verifyGeneratedCode(code: any, framework: CodeGenerationOptions['framework']): void {
    if (!code.typescript || code.typescript.length === 0) {
      throw new Error(`No TypeScript code generated for ${framework}`)
    }
    
    if (!code.dependencies || code.dependencies.length === 0) {
      throw new Error(`No dependencies specified for ${framework}`)
    }
    
    if (!code.imports || code.imports.length === 0) {
      throw new Error(`No imports specified for ${framework}`)
    }
    
    // Framework-specific validations
    switch (framework) {
      case 'vue':
        if (!code.typescript.includes('<template>') || !code.typescript.includes('<script')) {
          throw new Error('Vue code missing template or script sections')
        }
        break
      case 'svelte':
        if (!code.typescript.includes('<script') || !code.typescript.includes('<style>')) {
          throw new Error('Svelte code missing script or style sections')
        }
        break
      case 'angular':
        if (!code.typescript.includes('@Component') || !code.typescript.includes('export class')) {
          throw new Error('Angular code missing component decorator or class')
        }
        break
      case 'react':
      case 'next':
        if (!code.typescript.includes('export default function') && !code.typescript.includes('const ')) {
          throw new Error('React/Next code missing component export')
        }
        break
    }
  }
  
  /**
   * Verify dependencies for framework
   */
  static verifyDependencies(dependencies: string[], framework: CodeGenerationOptions['framework']): void {
    const frameworkDeps: Record<string, string[]> = {
      react: ['react', 'react-dom'],
      next: ['next', 'react', 'react-dom'],
      vue: ['vue'],
      svelte: ['svelte'],
      angular: ['@angular/core']
    }
    
    const requiredDeps = frameworkDeps[framework] || []
    for (const dep of requiredDeps) {
      if (!dependencies.some(d => d.includes(dep))) {
        throw new Error(`Missing required dependency: ${dep} for ${framework}`)
      }
    }
  }
  
  /**
   * Verify imports for framework
   */
  static verifyImports(imports: string[], framework: CodeGenerationOptions['framework']): void {
    if (imports.length === 0) {
      throw new Error(`No imports generated for ${framework}`)
    }
    
    // Framework-specific import validations
    switch (framework) {
      case 'react':
      case 'next':
        if (!imports.some(imp => imp.includes('React'))) {
          throw new Error('React imports missing React import')
        }
        break
      case 'vue':
        if (!imports.some(imp => imp.includes('vue'))) {
          throw new Error('Vue imports missing vue import')
        }
        break
      case 'svelte':
        if (!imports.some(imp => imp.includes('svelte'))) {
          throw new Error('Svelte imports missing svelte import')
        }
        break
      case 'angular':
        if (!imports.some(imp => imp.includes('@angular'))) {
          throw new Error('Angular imports missing @angular import')
        }
        break
    }
  }
  
  /**
   * Verify component code
   */
  static verifyComponentCode(code: string, componentType: string, framework: CodeGenerationOptions['framework']): void {
    if (!code || code.length === 0) {
      throw new Error(`No code generated for ${componentType} component in ${framework}`)
    }
    
    // Check for component-specific content
    switch (componentType) {
      case 'hero':
        if (!code.includes('hero') && !code.includes('Hero')) {
          throw new Error(`Hero component code doesn't contain hero-related content`)
        }
        break
      case 'button':
        if (!code.includes('button') && !code.includes('Button')) {
          throw new Error(`Button component code doesn't contain button-related content`)
        }
        break
    }
  }
  
  /**
   * Create test interface specification
   */
  static createTestInterfaceSpec(): InterfaceSpec {
    return {
      id: 'test-page',
      name: 'TestPage',
      type: 'page',
      components: [
        this.createTestComponent('hero'),
        this.createTestComponent('features'),
        this.createTestComponent('pricing')
      ],
      theme: this.createTestTheme()
    }
  }
  
  /**
   * Create test component
   */
  static createTestComponent(type: ComponentSpec['type']): ComponentSpec {
    return {
      id: `test-${type}`,
      type,
      props: {
        title: `Test ${type} Title`,
        description: `Test ${type} Description`,
        ctaText: 'Test CTA'
      },
      styling: {
        colors: {
          background: 'blue-50',
          text: 'gray-900'
        },
        spacing: {
          padding: '6'
        }
      }
    }
  }
  
  /**
   * Create test theme
   */
  static createTestTheme() {
    return {
      primaryColor: '#3b82f6',
      secondaryColor: '#8b5cf6',
      backgroundColor: '#ffffff',
      textColor: '#1f2937',
      fontFamily: 'Inter'
    }
  }
  
  /**
   * Count lines in code
   */
  static countLines(code: string): number {
    return code.split('\n').length
  }
  
  /**
   * Generate test report
   */
  static generateTestReport(results: TestResult[]): string {
    const totalTests = results.length
    const successfulTests = results.filter(r => r.success).length
    const failedTests = results.filter(r => !r.success)
    
    let report = `
🧪 Phase 3A Multi-Framework Test Report
========================================

Total Tests: ${totalTests}
Successful: ${successfulTests}
Failed: ${failedTests.length}
Success Rate: ${((successfulTests / totalTests) * 100).toFixed(1)}%

Framework Results:
`
    
    const frameworkResults = ['react', 'next', 'vue', 'svelte', 'angular'].map(framework => {
      const frameworkTests = results.filter(r => r.framework === framework)
      const success = frameworkTests.filter(r => r.success).length
      const total = frameworkTests.length
      return `  ${framework}: ${success}/${total} passed`
    }).join('\n')
    
    report += frameworkResults
    
    if (failedTests.length > 0) {
      report += '\n\nFailed Tests:\n'
      failedTests.forEach(test => {
        report += `  ❌ ${test.testName}: ${test.error}\n`
      })
    }
    
    report += '\n\nPerformance Metrics:\n'
    const avgDuration = results.reduce((sum, r) => sum + r.duration, 0) / results.length
    report += `  Average test duration: ${avgDuration.toFixed(0)}ms\n`
    
    const totalCodeSize = results.reduce((sum, r) => sum + (r.codeSize || 0), 0)
    report += `  Total generated code size: ${(totalCodeSize / 1024).toFixed(1)}KB\n`
    
    return report
  }
}

export interface TestResult {
  testName: string
  framework: CodeGenerationOptions['framework'] | 'all'
  runNumber: number
  success: boolean
  duration: number
  error?: string
  details: string
  generatedLines?: number
  codeSize?: number
}
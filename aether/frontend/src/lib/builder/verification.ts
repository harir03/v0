import { InterfaceSpec, VerificationResult, VerificationError, VerificationWarning } from '@/types/builder'

/**
 * Verification system for generated code quality and compliance
 */
export class CodeVerifier {
  /**
   * Verify interface specification and generated code
   */
  async verify(spec: InterfaceSpec, generatedCode: string): Promise<VerificationResult> {
    const errors: VerificationError[] = []
    const warnings: VerificationWarning[] = []

    // TypeScript verification
    const tsErrors = this.verifyTypeScript(generatedCode)
    errors.push(...tsErrors)

    // ESLint verification
    const eslintWarnings = this.verifyESLint(generatedCode)
    warnings.push(...eslintWarnings)

    // Accessibility verification
    const a11yWarnings = this.verifyAccessibility(spec)
    warnings.push(...a11yWarnings)

    // Performance verification
    const perfWarnings = this.verifyPerformance(spec)
    warnings.push(...perfWarnings)

    // Responsive design verification
    const responsiveWarnings = this.verifyResponsive(spec)
    warnings.push(...responsiveWarnings)

    return {
      passed: errors.length === 0,
      errors,
      warnings,
      performance: this.calculatePerformanceMetrics(spec),
      accessibility: this.calculateAccessibilityScore(spec)
    }
  }

  private verifyTypeScript(code: string): VerificationError[] {
    const errors: VerificationError[] = []

    // Basic TypeScript checks
    if (!code.includes('export default')) {
      errors.push({
        type: 'typescript',
        message: 'Component must have a default export',
        file: 'generated.tsx',
        line: 1
      })
    }

    // Check for proper React import
    if (!code.includes('import React') && !code.includes('import { ')) {
      errors.push({
        type: 'typescript',
        message: 'Missing React import',
        file: 'generated.tsx',
        line: 1
      })
    }

    return errors
  }

  private verifyESLint(code: string): VerificationWarning[] {
    const warnings: VerificationWarning[] = []

    // Check for unused variables
    const unusedVarRegex = /const\s+(\w+)\s*=/g
    let match
    while ((match = unusedVarRegex.exec(code)) !== null) {
      const variable = match[1]
      if (!code.includes(variable, match.index + match[0].length)) {
        warnings.push({
          type: 'best-practice',
          message: `Unused variable: ${variable}`,
          severity: 'low'
        })
      }
    }

    // Check for console.log statements
    if (code.includes('console.log')) {
      warnings.push({
        type: 'best-practice',
        message: 'Remove console.log statements from production code',
        severity: 'medium'
      })
    }

    return warnings
  }

  private verifyAccessibility(spec: InterfaceSpec): VerificationWarning[] {
    const warnings: VerificationWarning[] = []

    spec.components.forEach(component => {
      switch (component.type) {
        case 'hero':
          if (!component.props.title) {
            warnings.push({
              type: 'accessibility',
              message: `Hero component ${component.id} missing title for screen readers`,
              severity: 'high'
            })
          }
          break

        case 'button':
          if (!component.props.ariaLabel && !component.props.children) {
            warnings.push({
              type: 'accessibility',
              message: `Button component ${component.id} needs aria-label or text content`,
              severity: 'high'
            })
          }
          break

        case 'image':
          if (!component.props.alt) {
            warnings.push({
              type: 'accessibility',
              message: `Image component ${component.id} missing alt text`,
              severity: 'high'
            })
          }
          break
      }
    })

    // Check color contrast
    if (spec.theme.backgroundColor && spec.theme.textColor) {
      const contrast = this.calculateColorContrast(spec.theme.backgroundColor, spec.theme.textColor)
      if (contrast < 4.5) {
        warnings.push({
          type: 'accessibility',
          message: 'Text color contrast ratio is below WCAG AA standards (4.5:1)',
          severity: 'high'
        })
      }
    }

    return warnings
  }

  private verifyPerformance(spec: InterfaceSpec): VerificationWarning[] {
    const warnings: VerificationWarning[] = []

    // Check for too many components
    if (spec.components.length > 20) {
      warnings.push({
        type: 'performance',
        message: 'Consider splitting large pages into smaller components for better performance',
        severity: 'medium'
      })
    }

    // Check for heavy animations
    const hasHeavyAnimations = spec.components.some(component => 
      component.props.animation === 'complex' || component.props.particles
    )
    
    if (hasHeavyAnimations) {
      warnings.push({
        type: 'performance',
        message: 'Heavy animations may impact performance on slower devices',
        severity: 'medium'
      })
    }

    return warnings
  }

  private verifyResponsive(spec: InterfaceSpec): VerificationWarning[] {
    const warnings: VerificationWarning[] = []

    spec.components.forEach(component => {
      // Check for responsive grid classes
      if (component.type === 'features' && !this.hasResponsiveClasses(component)) {
        warnings.push({
          type: 'best-practice',
          message: `Features component ${component.id} should include responsive grid classes`,
          severity: 'medium'
        })
      }

      // Check for mobile-friendly text sizes
      if (component.type === 'hero' && component.props.fontSize && parseInt(component.props.fontSize) > 48) {
        warnings.push({
          type: 'best-practice',
          message: `Hero text size may be too large for mobile devices`,
          severity: 'low'
        })
      }
    })

    return warnings
  }

  private hasResponsiveClasses(component: any): boolean {
    const code = JSON.stringify(component)
    return /md:|lg:|xl:|sm:/.test(code)
  }

  private calculateColorContrast(bg: string, text: string): number {
    // Simplified contrast calculation
    // In a real implementation, you'd use proper color contrast algorithms
    const bgLuminance = this.getLuminance(bg)
    const textLuminance = this.getLuminance(text)
    
    const lighter = Math.max(bgLuminance, textLuminance)
    const darker = Math.min(bgLuminance, textLuminance)
    
    return (lighter + 0.05) / (darker + 0.05)
  }

  private getLuminance(color: string): number {
    // Simplified luminance calculation
    const hex = color.replace('#', '')
    const r = parseInt(hex.slice(0, 2), 16) / 255
    const g = parseInt(hex.slice(2, 4), 16) / 255
    const b = parseInt(hex.slice(4, 6), 16) / 255
    
    return 0.2126 * r + 0.7152 * g + 0.0722 * b
  }

  private calculatePerformanceMetrics(spec: InterfaceSpec) {
    // Estimate performance metrics based on spec complexity
    const componentCount = spec.components.length
    const hasAnimations = spec.components.some(c => c.props.animation)
    
    return {
      lcp: 1200 + (componentCount * 100), // Estimated LCP in ms
      cls: hasAnimations ? 0.1 : 0.05, // Estimated CLS
      fid: 50 + (componentCount * 5), // Estimated FID in ms
      ttfb: 200 // Estimated TTFB in ms
    }
  }

  private calculateAccessibilityScore(spec: InterfaceSpec) {
    let violations = 0
    let totalChecks = 0

    spec.components.forEach(component => {
      totalChecks += 3 // Basic checks per component

      // Check for missing alt text on images
      if (component.type === 'image' && !component.props.alt) {
        violations++
      }

      // Check for missing labels on buttons
      if (component.type === 'button' && !component.props.ariaLabel && !component.props.children) {
        violations++
      }

      // Check for heading hierarchy
      if (component.type === 'text' && component.props.level > 3) {
        violations++
      }
    })

    // Check color contrast
    totalChecks++
    if (spec.theme.backgroundColor && spec.theme.textColor) {
      const contrast = this.calculateColorContrast(spec.theme.backgroundColor, spec.theme.textColor)
      if (contrast < 4.5) {
        violations++
      }
    }

    const score = Math.max(0, Math.round((1 - violations / totalChecks) * 100))
    
    return {
      violations: [],
      score,
      passes: totalChecks - violations,
      incomplete: 0
    }
  }
}

/**
 * Performance optimization utilities
 */
export class PerformanceOptimizer {
  /**
   * Optimize generated code for performance
   */
  static optimizeCode(code: string): string {
    let optimized = code

    // Add React.memo for components without props dependencies
    if (!optimized.includes('React.memo') && !optimized.includes('useState') && !optimized.includes('useEffect')) {
      optimized = optimized.replace(
        /export default function (\w+)/,
        'const $1 = React.memo(function $1'
      ).replace(/}$/, '})\n\nexport default $1')
    }

    // Add loading="lazy" to images
    optimized = optimized.replace(
      /<img\s+([^>]+)>/g,
      '<img loading="lazy" $1>'
    )

    // Add prefetch hints for critical resources
    if (optimized.includes('framer-motion')) {
      optimized = `// @ts-ignore
import dynamic from 'next/dynamic'

const MotionDiv = dynamic(() => import('framer-motion').then(mod => mod.motion.div), {
  loading: () => <div className="animate-pulse" />
})

${optimized}`
    }

    return optimized
  }

  /**
   * Generate lighthouse performance budget
   */
  static generatePerformanceBudget(spec: InterfaceSpec) {
    const componentCount = spec.components.length
    const hasAnimations = spec.components.some(c => c.props.animation)
    
    return {
      resourceSizes: [
        { resourceType: 'script', budget: 300000 }, // 300KB
        { resourceType: 'stylesheet', budget: 50000 }, // 50KB
        { resourceType: 'image', budget: 200000 }, // 200KB per image
      ],
      resourceCounts: [
        { resourceType: 'script', budget: 10 },
        { resourceType: 'stylesheet', budget: 5 },
        { resourceType: 'third-party', budget: 5 }
      ],
      timings: [
        { metric: 'first-contentful-paint', budget: 2000 },
        { metric: 'largest-contentful-paint', budget: 2500 },
        { metric: 'cumulative-layout-shift', budget: 0.1 },
        { metric: 'total-blocking-time', budget: 300 }
      ]
    }
  }
}
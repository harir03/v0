import { InterfaceSpec, ComponentSpec, GeneratedCode } from '@/types/builder'
import { FrameworkCodeGenerator } from './base'

/**
 * Angular code generator (Angular 17 with standalone components)
 */
export class AngularCodeGenerator extends FrameworkCodeGenerator {
  
  generatePage(spec: InterfaceSpec): GeneratedCode {
    const imports = this.generateImports(spec)
    const componentClass = this.generateComponentClass(spec)
    const template = this.generateTemplate(spec)
    const styles = this.generateStyles(spec)

    const angularCode = `${imports.join('\n')}\n\n${componentClass}`

    return {
      typescript: angularCode,
      css: styles,
      dependencies: this.getDependencies(spec),
      imports: imports,
      additionalFiles: {
        'component.html': template,
        'component.css': styles
      }
    }
  }

  generateComponent(component: ComponentSpec, theme: any): string {
    switch (component.type) {
      case 'hero':
        return this.generateHeroComponent(component, theme)
      case 'features':
        return this.generateFeaturesComponent(component, theme)
      case 'pricing':
        return this.generatePricingComponent(component, theme)
      case 'cta':
        return this.generateCTAComponent(component, theme)
      case 'button':
        return this.generateButtonComponent(component, theme)
      default:
        return this.generateGenericComponent(component, theme)
    }
  }

  generateImports(spec: InterfaceSpec): string[] {
    const imports = [
      "import { Component, OnInit, OnDestroy, ChangeDetectionStrategy } from '@angular/core'",
      "import { CommonModule } from '@angular/common'",
      "import { RouterModule } from '@angular/router'"
    ]

    // Add framework-specific imports
    if (this.hasAnimations(spec)) {
      imports.push("import { trigger, transition, style, animate } from '@angular/animations'")
    }

    if (this.hasReactiveForms(spec)) {
      imports.push("import { ReactiveFormsModule, FormBuilder, FormGroup } from '@angular/forms'")
    }

    return imports
  }

  getDependencies(spec: InterfaceSpec): string[] {
    const deps = [
      '@angular/core@^17.0.0',
      '@angular/common@^17.0.0',
      '@angular/platform-browser@^17.0.0',
      '@angular/router@^17.0.0',
      '@angular/cli@^17.0.0',
      'typescript@^5.2.0'
    ]

    if (this.options.styling === 'tailwind') {
      deps.push('tailwindcss@^3.3.0', 'autoprefixer@^10.4.0', 'postcss@^8.4.0')
    }

    if (this.hasAnimations(spec)) {
      deps.push('@angular/animations@^17.0.0')
    }

    if (this.hasReactiveForms(spec)) {
      deps.push('@angular/forms@^17.0.0')
    }

    return deps
  }

  generatePropsInterface(component: ComponentSpec): string {
    if (!this.options.typescript) return ''

    const props = Object.keys(component.props || {})
    if (props.length === 0) return ''

    const propsInterface = props.map(prop => {
      const value = component.props[prop]
      const type = typeof value === 'string' ? 'string' : 
                   typeof value === 'number' ? 'number' :
                   typeof value === 'boolean' ? 'boolean' : 'any'
      return `  @Input() ${prop}!: ${type};`
    }).join('\n')

    return `// Component Inputs\n${propsInterface}`
  }

  generateEventHandlers(component: ComponentSpec): string {
    const events = component.props?.events || {}
    const handlers = Object.keys(events).map(event => {
      return `  handle${this.capitalizeFirst(event)}(): void {\n    // ${events[event]}\n  }`
    })

    return handlers.join('\n\n')
  }

  generateLifecycleHooks(component: ComponentSpec): string {
    let hooks = ''

    if (component.props?.onMount) {
      hooks += `  ngOnInit(): void {\n    // ${component.props.onMount}\n  }\n\n`
    }

    hooks += `  ngOnDestroy(): void {\n    // Cleanup\n  }\n\n`

    return hooks
  }

  private generateComponentClass(spec: InterfaceSpec): string {
    const animations = this.hasAnimations(spec) ? this.generateAnimations(spec) : ''
    
    return `@Component({
  selector: 'app-${spec.name.toLowerCase()}',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './${spec.name.toLowerCase()}.component.html',
  styleUrls: ['./${spec.name.toLowerCase()}.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush${animations ? ',\n  animations: [' + animations + ']' : ''}
})
export class ${this.capitalizeFirst(spec.name)}Component implements OnInit, OnDestroy {
  
  // Component properties
  isLoaded = false;
  currentTheme = 'default';

  // Mock data for demo
  features = [
    { id: 1, title: 'Fast', description: 'Lightning fast performance', icon: 'speed' },
    { id: 2, title: 'Reliable', description: 'Rock solid reliability', icon: 'shield' },
    { id: 3, title: 'Scalable', description: 'Scales with your needs', icon: 'trending_up' }
  ];

  pricingPlans = [
    { id: 1, name: 'Starter', price: 9, ctaText: 'Start Free Trial' },
    { id: 2, name: 'Pro', price: 29, ctaText: 'Go Pro' },
    { id: 3, name: 'Enterprise', price: 99, ctaText: 'Contact Sales' }
  ];

  constructor() {}

  ngOnInit(): void {
    this.isLoaded = true;
  }

  ngOnDestroy(): void {
    // Cleanup
  }

  // Component methods
  ${this.generatePageMethods(spec)}
}`
  }

  private generateTemplate(spec: InterfaceSpec): string {
    const componentTemplates = spec.components.map(comp => 
      this.generateComponentTemplate(comp, spec.theme)
    ).join('\n')

    return `<div class="min-h-screen bg-background text-foreground">
  ${componentTemplates}
</div>`
  }

  private generateStyles(spec: InterfaceSpec): string {
    if (this.options.styling === 'tailwind') {
      return `/* Tailwind CSS */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom component styles */
.hero-gradient {
  background: linear-gradient(135deg, ${spec.theme.primaryColor || '#3b82f6'} 0%, ${spec.theme.secondaryColor || '#8b5cf6'} 100%);
}

/* Angular-specific animations */
.fade-in {
  animation: fadeIn 0.6s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Host element styles */
:host {
  display: block;
  width: 100%;
}`
    }

    return `/* Component-specific styles */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Global transitions */
* {
  transition: all 0.2s ease;
}

/* Host element styles */
:host {
  display: block;
  width: 100%;
}`
  }

  private generateComponentTemplate(component: ComponentSpec, theme: any): string {
    const classes = this.generateTailwindClasses(component, theme)
    const responsiveClasses = this.generateResponsiveClasses(component).join(' ')
    const allClasses = [classes, responsiveClasses].filter(Boolean).join(' ')

    switch (component.type) {
      case 'hero':
        return `<section class="${allClasses} py-20 px-4" [class.fade-in]="isLoaded">
  <div class="max-w-7xl mx-auto text-center">
    <h1 class="text-5xl font-bold mb-6 gradient-text">
      ${component.props?.title || 'Welcome to Angular App'}
    </h1>
    <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
      ${component.props?.description || 'Build amazing applications with Angular'}
    </p>
    <button 
      class="bg-primary text-white px-8 py-3 rounded-lg hover:bg-primary/90 transition-colors" 
      (click)="handleCTAClick()"
    >
      ${component.props?.ctaText || 'Get Started'}
    </button>
  </div>
</section>`

      case 'features':
        return `<section class="${allClasses} py-16 px-4">
  <div class="max-w-7xl mx-auto">
    <h2 class="text-3xl font-bold text-center mb-12">
      ${component.props?.title || 'Features'}
    </h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div *ngFor="let feature of features; trackBy: trackByFeatureId" 
           class="text-center p-6 rounded-lg border hover:shadow-lg transition-shadow">
        <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mx-auto mb-4">
          <mat-icon class="text-primary">{{ feature.icon }}</mat-icon>
        </div>
        <h3 class="text-xl font-semibold mb-2">{{ feature.title }}</h3>
        <p class="text-gray-600">{{ feature.description }}</p>
      </div>
    </div>
  </div>
</section>`

      case 'pricing':
        return `<section class="${allClasses} py-16 px-4">
  <div class="max-w-7xl mx-auto">
    <h2 class="text-3xl font-bold text-center mb-12">
      ${component.props?.title || 'Pricing'}
    </h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div *ngFor="let plan of pricingPlans; trackBy: trackByPlanId" 
           class="border rounded-lg p-8 text-center hover:shadow-lg transition-shadow">
        <h3 class="text-2xl font-bold mb-4">{{ plan.name }}</h3>
        <div class="text-4xl font-bold mb-6">
          <span class="text-sm font-normal">$</span>{{ plan.price }}
          <span class="text-base font-normal text-gray-600">/month</span>
        </div>
        <button 
          class="w-full bg-primary text-white py-3 rounded-lg hover:bg-primary/90 transition-colors"
          (click)="handlePlanSelect(plan)"
        >
          {{ plan.ctaText }}
        </button>
      </div>
    </div>
  </div>
</section>`

      case 'button':
        return `<button 
  class="${allClasses} px-6 py-2 rounded-lg transition-colors"
  (click)="handleClick()"
  [disabled]="${component.props?.disabled || false}"
>
  ${component.props?.text || 'Button'}
</button>`

      default:
        return `<div class="${allClasses}">
  <!-- ${component.type} component -->
  ${component.children?.map(child => this.generateComponentTemplate(child, theme)).join('\n  ') || ''}
</div>`
    }
  }

  private generateAnimations(spec: InterfaceSpec): string {
    return `
    trigger('fadeIn', [
      transition(':enter', [
        style({ opacity: 0, transform: 'translateY(20px)' }),
        animate('0.6s ease-in-out', style({ opacity: 1, transform: 'translateY(0)' }))
      ])
    ])`
  }

  private generateHeroComponent(component: ComponentSpec, theme: any): string {
    return this.generateComponentTemplate(component, theme)
  }

  private generateFeaturesComponent(component: ComponentSpec, theme: any): string {
    return this.generateComponentTemplate(component, theme)
  }

  private generatePricingComponent(component: ComponentSpec, theme: any): string {
    return this.generateComponentTemplate(component, theme)
  }

  private generateCTAComponent(component: ComponentSpec, theme: any): string {
    return this.generateComponentTemplate(component, theme)
  }

  private generateButtonComponent(component: ComponentSpec, theme: any): string {
    return this.generateComponentTemplate(component, theme)
  }

  private generateGenericComponent(component: ComponentSpec, theme: any): string {
    return this.generateComponentTemplate(component, theme)
  }

  private generatePageMethods(spec: InterfaceSpec): string {
    return `// Page methods
  handleCTAClick(): void {
    console.log('CTA clicked');
  }

  handleClick(): void {
    console.log('Button clicked');
  }

  handlePlanSelect(plan: any): void {
    console.log('Plan selected:', plan);
  }

  // Track by functions for ngFor
  trackByFeatureId(index: number, feature: any): number {
    return feature.id;
  }

  trackByPlanId(index: number, plan: any): number {
    return plan.id;
  }`
  }

  private hasAnimations(spec: InterfaceSpec): boolean {
    return spec.components.some(comp => 
      comp.props?.animations || 
      comp.styling?.animations
    )
  }

  private hasReactiveForms(spec: InterfaceSpec): boolean {
    return spec.components.some(comp => comp.type === 'form')
  }

  private capitalizeFirst(str: string): string {
    return str.charAt(0).toUpperCase() + str.slice(1)
  }
}
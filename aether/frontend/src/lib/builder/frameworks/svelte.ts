import { InterfaceSpec, ComponentSpec, GeneratedCode } from '@/types/builder'
import { FrameworkCodeGenerator } from './base'

/**
 * Svelte code generator (Svelte 4 with SvelteKit)
 */
export class SvelteCodeGenerator extends FrameworkCodeGenerator {
  
  generatePage(spec: InterfaceSpec): GeneratedCode {
    const imports = this.generateImports(spec)
    const script = this.generateScript(spec, imports)
    const template = this.generateTemplate(spec)
    const styles = this.generateStyles(spec)

    const svelteCode = `${script}\n\n${template}\n\n${styles}`

    return {
      typescript: svelteCode,
      css: styles,
      dependencies: this.getDependencies(spec),
      imports: imports
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
      "import { onMount, tick } from 'svelte'",
      "import { writable } from 'svelte/store'"
    ]

    // Add framework-specific imports
    if (this.hasAnimations(spec)) {
      imports.push("import { gsap } from 'gsap'")
    }

    return imports
  }

  getDependencies(spec: InterfaceSpec): string[] {
    const deps = [
      'svelte@^4.2.0',
      '@sveltejs/kit@^1.27.0',
      '@sveltejs/adapter-auto@^2.1.0',
      'vite@^4.4.0'
    ]

    if (this.options.typescript) {
      deps.push('typescript@^5.0.0', 'svelte-check@^3.5.0', '@sveltejs/vite-plugin-svelte@^2.5.0')
    }

    if (this.options.styling === 'tailwind') {
      deps.push('tailwindcss@^3.3.0', 'autoprefixer@^10.4.0', 'postcss@^8.4.0')
    }

    if (this.hasAnimations(spec)) {
      deps.push('gsap@^3.12.0')
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
      return `  export let ${prop}: ${type}`
    }).join('\n')

    return `// Component Props\n${propsInterface}`
  }

  generateEventHandlers(component: ComponentSpec): string {
    const events = component.props?.events || {}
    const handlers = Object.keys(events).map(event => {
      return `function handle${this.capitalizeFirst(event)}() {\n  // ${events[event]}\n}`
    })

    return handlers.join('\n\n')
  }

  generateLifecycleHooks(component: ComponentSpec): string {
    let hooks = ''

    if (component.props?.onMount) {
      hooks += `onMount(() => {\n  // ${component.props.onMount}\n})\n\n`
    }

    return hooks
  }

  private generateScript(spec: InterfaceSpec, imports: string[]): string {
    const scriptLang = this.options.typescript ? ' lang="ts"' : ''
    
    return `<script${scriptLang}>
${imports.join('\n')}

// Component state
let isLoaded = false

// Stores
const currentTheme = writable('default')

// Lifecycle
onMount(() => {
  isLoaded = true
})

// Component methods
${this.generatePageMethods(spec)}

// Mock data for demo
let features = [
  { id: 1, title: 'Fast', description: 'Lightning fast performance', icon: 'zap' },
  { id: 2, title: 'Reliable', description: 'Rock solid reliability', icon: 'shield' },
  { id: 3, title: 'Scalable', description: 'Scales with your needs', icon: 'trending-up' }
]

let pricingPlans = [
  { id: 1, name: 'Starter', price: 9, ctaText: 'Start Free Trial' },
  { id: 2, name: 'Pro', price: 29, ctaText: 'Go Pro' },
  { id: 3, name: 'Enterprise', price: 99, ctaText: 'Contact Sales' }
]
</script>`
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
      return `<style>
  /* Tailwind CSS */
  @tailwind base;
  @tailwind components;
  @tailwind utilities;

  /* Custom component styles */
  .hero-gradient {
    background: linear-gradient(135deg, ${spec.theme.primaryColor || '#3b82f6'} 0%, ${spec.theme.secondaryColor || '#8b5cf6'} 100%);
  }

  /* Svelte-specific animations */
  .fade-in {
    animation: fadeIn 0.6s ease-in-out;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }
</style>`
    }

    return `<style>
  /* Component-specific styles */
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
  }

  /* Global transitions */
  * {
    transition: all 0.2s ease;
  }
</style>`
  }

  private generateComponentTemplate(component: ComponentSpec, theme: any): string {
    const classes = this.generateTailwindClasses(component, theme)
    const responsiveClasses = this.generateResponsiveClasses(component).join(' ')
    const allClasses = [classes, responsiveClasses].filter(Boolean).join(' ')

    switch (component.type) {
      case 'hero':
        return `<section class="${allClasses} py-20 px-4" class:fade-in={isLoaded}>
  <div class="max-w-7xl mx-auto text-center">
    <h1 class="text-5xl font-bold mb-6 gradient-text">
      ${component.props?.title || 'Welcome to Svelte App'}
    </h1>
    <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
      ${component.props?.description || 'Build amazing applications with Svelte'}
    </p>
    <button 
      class="bg-primary text-white px-8 py-3 rounded-lg hover:bg-primary/90 transition-colors" 
      on:click={handleCTAClick}
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
      {#each features as feature (feature.id)}
        <div class="text-center p-6 rounded-lg border hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mx-auto mb-4">
            <iconify-icon icon="lucide:{feature.icon}" class="w-6 h-6 text-primary"></iconify-icon>
          </div>
          <h3 class="text-xl font-semibold mb-2">{feature.title}</h3>
          <p class="text-gray-600">{feature.description}</p>
        </div>
      {/each}
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
      {#each pricingPlans as plan (plan.id)}
        <div class="border rounded-lg p-8 text-center hover:shadow-lg transition-shadow">
          <h3 class="text-2xl font-bold mb-4">{plan.name}</h3>
          <div class="text-4xl font-bold mb-6">
            <span class="text-sm font-normal">$</span>{plan.price}
            <span class="text-base font-normal text-gray-600">/month</span>
          </div>
          <button 
            class="w-full bg-primary text-white py-3 rounded-lg hover:bg-primary/90 transition-colors"
            on:click={() => handlePlanSelect(plan)}
          >
            {plan.ctaText}
          </button>
        </div>
      {/each}
    </div>
  </div>
</section>`

      case 'button':
        return `<button 
  class="${allClasses} px-6 py-2 rounded-lg transition-colors"
  on:click={handleClick}
  disabled={${component.props?.disabled || false}}
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
function handleCTAClick() {
  console.log('CTA clicked')
}

function handleClick() {
  console.log('Button clicked')
}

function handlePlanSelect(plan) {
  console.log('Plan selected:', plan)
}`
  }

  private hasAnimations(spec: InterfaceSpec): boolean {
    return spec.components.some(comp => 
      comp.props?.animations || 
      comp.styling?.animations
    )
  }

  private capitalizeFirst(str: string): string {
    return str.charAt(0).toUpperCase() + str.slice(1)
  }
}
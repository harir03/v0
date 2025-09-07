import { CodeGenerationOptions } from '@/types/builder'
import { FrameworkCodeGenerator } from './base'
import { VueCodeGenerator } from './vue'
import { SvelteCodeGenerator } from './svelte'
import { AngularCodeGenerator } from './angular'
import { ReactCodeGenerator } from './react'

/**
 * Factory for creating framework-specific code generators
 */
export class FrameworkFactory {
  
  static createGenerator(options: CodeGenerationOptions): FrameworkCodeGenerator {
    switch (options.framework) {
      case 'vue':
        return new VueCodeGenerator(options)
      case 'svelte':
        return new SvelteCodeGenerator(options)
      case 'angular':
        return new AngularCodeGenerator(options)
      case 'react':
      case 'next':
        return new ReactCodeGenerator(options)
      default:
        throw new Error(`Unsupported framework: ${options.framework}`)
    }
  }

  /**
   * Get available frameworks with their configurations
   */
  static getAvailableFrameworks(): FrameworkInfo[] {
    return [
      {
        name: 'React',
        key: 'react',
        version: '18.x',
        description: 'Popular JavaScript library for building user interfaces',
        icon: '⚛️',
        features: ['Hooks', 'JSX', 'Virtual DOM', 'Component-based'],
        buildTool: 'Vite',
        styling: ['Tailwind CSS', 'CSS Modules', 'Styled Components']
      },
      {
        name: 'Next.js',
        key: 'next',
        version: '14.x',
        description: 'React framework with SSR, routing, and optimizations',
        icon: '▲',
        features: ['SSR/SSG', 'App Router', 'Image Optimization', 'API Routes'],
        buildTool: 'Next.js',
        styling: ['Tailwind CSS', 'CSS Modules', 'Styled Components']
      },
      {
        name: 'Vue.js',
        key: 'vue',
        version: '3.x',
        description: 'Progressive framework with Composition API',
        icon: '🟢',
        features: ['Composition API', 'Reactivity', 'SFC', 'Templates'],
        buildTool: 'Vite',
        styling: ['Tailwind CSS', 'Scoped CSS', 'CSS Modules']
      },
      {
        name: 'Svelte',
        key: 'svelte',
        version: '4.x',
        description: 'Compile-time framework with no virtual DOM',
        icon: '🔥',
        features: ['No Runtime', 'Reactive', 'Small Bundle', 'Simple Syntax'],
        buildTool: 'Vite',
        styling: ['Tailwind CSS', 'Scoped CSS', 'CSS-in-JS']
      },
      {
        name: 'Angular',
        key: 'angular',
        version: '17.x',
        description: 'Full-featured framework with TypeScript by default',
        icon: '🅰️',
        features: ['TypeScript', 'Dependency Injection', 'RxJS', 'CLI'],
        buildTool: 'Angular CLI',
        styling: ['Tailwind CSS', 'Angular Material', 'CSS Modules']
      }
    ]
  }

  /**
   * Get framework-specific project structure templates
   */
  static getProjectStructure(framework: string): ProjectStructure {
    const structures: Record<string, ProjectStructure> = {
      react: {
        files: [
          'src/components/App.tsx',
          'src/components/Button.tsx',
          'src/styles/globals.css',
          'src/main.tsx',
          'index.html',
          'package.json',
          'vite.config.ts',
          'tsconfig.json'
        ],
        scripts: {
          dev: 'vite',
          build: 'vite build',
          preview: 'vite preview'
        }
      },
      next: {
        files: [
          'src/app/page.tsx',
          'src/app/layout.tsx',
          'src/components/Button.tsx',
          'src/app/globals.css',
          'package.json',
          'next.config.js',
          'tsconfig.json'
        ],
        scripts: {
          dev: 'next dev',
          build: 'next build',
          start: 'next start'
        }
      },
      vue: {
        files: [
          'src/App.vue',
          'src/components/Button.vue',
          'src/style.css',
          'src/main.ts',
          'index.html',
          'package.json',
          'vite.config.ts',
          'tsconfig.json'
        ],
        scripts: {
          dev: 'vite',
          build: 'vite build',
          preview: 'vite preview'
        }
      },
      svelte: {
        files: [
          'src/App.svelte',
          'src/lib/Button.svelte',
          'src/app.css',
          'src/main.ts',
          'src/app.html',
          'package.json',
          'vite.config.ts',
          'tsconfig.json'
        ],
        scripts: {
          dev: 'vite dev',
          build: 'vite build',
          preview: 'vite preview'
        }
      },
      angular: {
        files: [
          'src/app/app.component.ts',
          'src/app/app.component.html',
          'src/app/app.component.css',
          'src/app/button/button.component.ts',
          'src/styles.css',
          'src/main.ts',
          'angular.json',
          'package.json',
          'tsconfig.json'
        ],
        scripts: {
          dev: 'ng serve',
          build: 'ng build',
          test: 'ng test'
        }
      }
    }

    return structures[framework] || structures.react
  }
}

export interface FrameworkInfo {
  name: string
  key: string
  version: string
  description: string
  icon: string
  features: string[]
  buildTool: string
  styling: string[]
}

export interface ProjectStructure {
  files: string[]
  scripts: Record<string, string>
}
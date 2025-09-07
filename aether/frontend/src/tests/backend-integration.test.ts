// Phase 3B: Backend Integration Tests

import { BackendCodeGenerator } from '../lib/backend-generator'
import { BackendTemplateLibrary } from '../lib/backend-templates'
import { BackendSpec, BackendFramework } from '../types/backend'

describe('Phase 3B - Backend Integration Tests', () => {
  describe('Backend Templates', () => {
    test('should load all backend templates', () => {
      const templates = BackendTemplateLibrary.getTemplates()
      expect(templates).toBeDefined()
      expect(templates.length).toBeGreaterThan(0)
      
      // Verify required properties
      templates.forEach(template => {
        expect(template.id).toBeDefined()
        expect(template.name).toBeDefined()
        expect(template.framework).toBeDefined()
        expect(template.spec).toBeDefined()
      })
    })

    test('should find templates by framework', () => {
      const expressTemplates = BackendTemplateLibrary.getTemplatesByFramework('express')
      const fastapiTemplates = BackendTemplateLibrary.getTemplatesByFramework('fastapi')
      
      expect(expressTemplates.length).toBeGreaterThan(0)
      expect(fastapiTemplates.length).toBeGreaterThan(0)
      
      expressTemplates.forEach(template => {
        expect(template.framework).toBe('express')
      })
    })

    test('should find templates by feature', () => {
      const authTemplates = BackendTemplateLibrary.getTemplatesByFeature('authentication')
      const crudTemplates = BackendTemplateLibrary.getTemplatesByFeature('crud-api')
      
      expect(authTemplates.length).toBeGreaterThan(0)
      expect(crudTemplates.length).toBeGreaterThan(0)
    })

    test('should find template by ID', () => {
      const template = BackendTemplateLibrary.getTemplateById('crud-api')
      expect(template).toBeDefined()
      expect(template?.id).toBe('crud-api')
      expect(template?.name).toBe('CRUD API')
    })
  })

  describe('Backend Code Generator - Express', () => {
    let generator: BackendCodeGenerator
    let crudTemplate: BackendSpec

    beforeEach(() => {
      const template = BackendTemplateLibrary.getTemplateById('crud-api')
      if (!template) throw new Error('CRUD template not found')
      
      crudTemplate = template.spec
      generator = new BackendCodeGenerator('express', crudTemplate)
    })

    test('should generate Express backend successfully', () => {
      const result = generator.generate()
      
      expect(result).toBeDefined()
      expect(result.framework).toBe('express')
      expect(result.files).toBeDefined()
      expect(result.dependencies).toBeDefined()
      expect(result.scripts).toBeDefined()
    })

    test('should generate required Express files', () => {
      const result = generator.generate()
      
      // Check for essential files
      expect(result.files['src/app.ts']).toBeDefined()
      expect(result.files['src/server.ts']).toBeDefined()
      expect(result.files['package.json']).toBeDefined()
      expect(result.files['tsconfig.json']).toBeDefined()
      expect(result.files['Dockerfile']).toBeDefined()
      
      // Check for middleware files
      expect(result.files['src/middleware/auth.ts']).toBeDefined()
      expect(result.files['src/middleware/validation.ts']).toBeDefined()
      expect(result.files['src/middleware/error.ts']).toBeDefined()
      
      // Check for database config
      expect(result.files['src/config/database.ts']).toBeDefined()
    })

    test('should generate model files based on spec', () => {
      const result = generator.generate()
      
      crudTemplate.database.models.forEach(model => {
        const modelFile = `src/models/${model.name.toLowerCase()}.ts`
        expect(result.files[modelFile]).toBeDefined()
        expect(result.files[modelFile]).toContain(`interface ${model.name}`)
        expect(result.files[modelFile]).toContain(`Create${model.name}`)
        expect(result.files[modelFile]).toContain(`Update${model.name}`)
      })
    })

    test('should generate correct dependencies', () => {
      const result = generator.generate()
      
      const depNames = result.dependencies.map(dep => dep.name)
      expect(depNames).toContain('express')
      expect(depNames).toContain('cors')
      expect(depNames).toContain('helmet')
      expect(depNames).toContain('jsonwebtoken')
      expect(depNames).toContain('typescript')
    })

    test('should generate valid package.json', () => {
      const result = generator.generate()
      const packageJson = JSON.parse(result.files['package.json'])
      
      expect(packageJson.name).toBeDefined()
      expect(packageJson.version).toBeDefined()
      expect(packageJson.scripts).toBeDefined()
      expect(packageJson.dependencies).toBeDefined()
      expect(packageJson.devDependencies).toBeDefined()
      
      // Check for essential scripts
      expect(packageJson.scripts.start).toBeDefined()
      expect(packageJson.scripts.dev).toBeDefined()
      expect(packageJson.scripts.build).toBeDefined()
    })

    test('should generate valid TypeScript config', () => {
      const result = generator.generate()
      const tsConfig = JSON.parse(result.files['tsconfig.json'])
      
      expect(tsConfig.compilerOptions).toBeDefined()
      expect(tsConfig.compilerOptions.target).toBeDefined()
      expect(tsConfig.compilerOptions.module).toBeDefined()
      expect(tsConfig.compilerOptions.outDir).toBe('./dist')
      expect(tsConfig.compilerOptions.rootDir).toBe('./src')
    })
  })

  describe('Backend Code Generator - FastAPI', () => {
    let generator: BackendCodeGenerator
    let blogTemplate: BackendSpec

    beforeEach(() => {
      const template = BackendTemplateLibrary.getTemplateById('blog-api')
      if (!template) throw new Error('Blog template not found')
      
      blogTemplate = template.spec
      generator = new BackendCodeGenerator('fastapi', blogTemplate)
    })

    test('should generate FastAPI backend successfully', () => {
      const result = generator.generate()
      
      expect(result).toBeDefined()
      expect(result.framework).toBe('fastapi')
      expect(result.files).toBeDefined()
      expect(result.dependencies).toBeDefined()
    })

    test('should generate required FastAPI files', () => {
      const result = generator.generate()
      
      // Check for essential files
      expect(result.files['main.py']).toBeDefined()
      expect(result.files['requirements.txt']).toBeDefined()
      expect(result.files['database.py']).toBeDefined()
      expect(result.files['schemas.py']).toBeDefined()
      expect(result.files['auth.py']).toBeDefined()
      
      // Check for model and router directories
      expect(result.files['models/__init__.py']).toBeDefined()
      expect(result.files['routers/__init__.py']).toBeDefined()
    })

    test('should generate correct Python dependencies', () => {
      const result = generator.generate()
      
      const depNames = result.dependencies.map(dep => dep.name)
      expect(depNames).toContain('fastapi')
      expect(depNames).toContain('uvicorn')
      expect(depNames).toContain('sqlalchemy')
      expect(depNames).toContain('pydantic')
    })
  })

  describe('Database Integration', () => {
    test('should handle PostgreSQL configuration', () => {
      const template = BackendTemplateLibrary.getTemplateById('crud-api')
      if (!template) throw new Error('Template not found')
      
      expect(template.spec.database.type).toBe('postgresql')
      
      const generator = new BackendCodeGenerator('express', template.spec)
      const result = generator.generate()
      
      expect(result.files['src/config/database.ts']).toContain('Pool')
      expect(result.files['src/config/database.ts']).toContain('postgresql')
    })

    test('should handle MongoDB configuration', () => {
      const template = BackendTemplateLibrary.getTemplateById('blog-api')
      if (!template) throw new Error('Template not found')
      
      expect(template.spec.database.type).toBe('mongodb')
      
      const generator = new BackendCodeGenerator('fastapi', template.spec)
      const result = generator.generate()
      
      expect(result.files['database.py']).toContain('mongodb')
    })
  })

  describe('Authentication Integration', () => {
    test('should generate JWT authentication for Express', () => {
      const template = BackendTemplateLibrary.getTemplateById('auth-api')
      if (!template) throw new Error('Auth template not found')
      
      const generator = new BackendCodeGenerator('express', template.spec)
      const result = generator.generate()
      
      expect(result.files['src/middleware/auth.ts']).toContain('jwt')
      expect(result.files['src/middleware/auth.ts']).toContain('verify')
      expect(result.files['src/middleware/auth.ts']).toContain('Bearer')
    })

    test('should include authentication endpoints', () => {
      const template = BackendTemplateLibrary.getTemplateById('auth-api')
      if (!template) throw new Error('Auth template not found')
      
      const authEndpoints = template.spec.api.endpoints.filter(
        endpoint => endpoint.path.includes('/auth/')
      )
      
      expect(authEndpoints.length).toBeGreaterThan(0)
      
      const loginEndpoint = authEndpoints.find(
        endpoint => endpoint.path === '/auth/login'
      )
      expect(loginEndpoint).toBeDefined()
      expect(loginEndpoint?.method).toBe('POST')
    })
  })

  describe('API Endpoint Generation', () => {
    test('should generate REST endpoints from spec', () => {
      const template = BackendTemplateLibrary.getTemplateById('crud-api')
      if (!template) throw new Error('Template not found')
      
      const { endpoints } = template.spec.api
      expect(endpoints.length).toBeGreaterThan(0)
      
      // Check for CRUD operations
      const getMethods = endpoints.filter(e => e.method === 'GET')
      const postMethods = endpoints.filter(e => e.method === 'POST')
      const putMethods = endpoints.filter(e => e.method === 'PUT')
      const deleteMethods = endpoints.filter(e => e.method === 'DELETE')
      
      expect(getMethods.length).toBeGreaterThan(0)
      expect(postMethods.length).toBeGreaterThan(0)
      expect(putMethods.length).toBeGreaterThan(0)
      expect(deleteMethods.length).toBeGreaterThan(0)
    })

    test('should generate controller files for endpoints', () => {
      const template = BackendTemplateLibrary.getTemplateById('crud-api')
      if (!template) throw new Error('Template not found')
      
      const generator = new BackendCodeGenerator('express', template.spec)
      const result = generator.generate()
      
      // Check that controller files are generated
      const controllerFiles = Object.keys(result.files).filter(
        filename => filename.includes('controllers/')
      )
      expect(controllerFiles.length).toBeGreaterThan(0)
    })
  })

  describe('Deployment Configuration', () => {
    test('should generate Dockerfile for Express', () => {
      const template = BackendTemplateLibrary.getTemplateById('crud-api')
      if (!template) throw new Error('Template not found')
      
      const generator = new BackendCodeGenerator('express', template.spec)
      const result = generator.generate()
      
      expect(result.files['Dockerfile']).toBeDefined()
      expect(result.files['Dockerfile']).toContain('FROM node:')
      expect(result.files['Dockerfile']).toContain('WORKDIR /app')
      expect(result.files['Dockerfile']).toContain('EXPOSE')
    })

    test('should generate docker-compose configuration', () => {
      const template = BackendTemplateLibrary.getTemplateById('crud-api')
      if (!template) throw new Error('Template not found')
      
      const generator = new BackendCodeGenerator('express', template.spec)
      const result = generator.generate()
      
      expect(result.files['docker-compose.yml']).toBeDefined()
      expect(result.files['docker-compose.yml']).toContain('version:')
      expect(result.files['docker-compose.yml']).toContain('services:')
      expect(result.files['docker-compose.yml']).toContain('app:')
      expect(result.files['docker-compose.yml']).toContain('db:')
    })

    test('should generate environment configuration', () => {
      const template = BackendTemplateLibrary.getTemplateById('crud-api')
      if (!template) throw new Error('Template not found')
      
      const generator = new BackendCodeGenerator('express', template.spec)
      const result = generator.generate()
      
      expect(result.files['.env.example']).toBeDefined()
      expect(result.files['.env.example']).toContain('DB_HOST')
      expect(result.files['.env.example']).toContain('JWT_SECRET')
      expect(result.files['.env.example']).toContain('NODE_ENV')
    })
  })

  describe('Error Handling and Validation', () => {
    test('should throw error for unsupported framework', () => {
      const template = BackendTemplateLibrary.getTemplateById('crud-api')
      if (!template) throw new Error('Template not found')
      
      expect(() => {
        new BackendCodeGenerator('unsupported' as BackendFramework, template.spec)
      }).not.toThrow() // Constructor doesn't validate, generate() does
      
      const generator = new BackendCodeGenerator('unsupported' as BackendFramework, template.spec)
      expect(() => {
        generator.generate()
      }).toThrow()
    })

    test('should handle missing template gracefully', () => {
      const template = BackendTemplateLibrary.getTemplateById('non-existent')
      expect(template).toBeUndefined()
    })

    test('should validate backend spec structure', () => {
      const template = BackendTemplateLibrary.getTemplateById('crud-api')
      if (!template) throw new Error('Template not found')
      
      const spec = template.spec
      
      // Validate required properties
      expect(spec.id).toBeDefined()
      expect(spec.name).toBeDefined()
      expect(spec.framework).toBeDefined()
      expect(spec.database).toBeDefined()
      expect(spec.api).toBeDefined()
      expect(spec.auth).toBeDefined()
      expect(spec.deployment).toBeDefined()
      expect(spec.version).toBeDefined()
      
      // Validate database spec
      expect(spec.database.type).toBeDefined()
      expect(spec.database.name).toBeDefined()
      expect(spec.database.models).toBeDefined()
      expect(Array.isArray(spec.database.models)).toBe(true)
      
      // Validate API spec
      expect(spec.api.basePath).toBeDefined()
      expect(spec.api.version).toBeDefined()
      expect(spec.api.endpoints).toBeDefined()
      expect(Array.isArray(spec.api.endpoints)).toBe(true)
    })
  })

  describe('Integration Testing', () => {
    test('should generate complete backend from template to deployment', () => {
      const template = BackendTemplateLibrary.getTemplateById('crud-api')
      if (!template) throw new Error('Template not found')
      
      // Step 1: Load template
      expect(template).toBeDefined()
      expect(template.spec).toBeDefined()
      
      // Step 2: Generate backend code
      const generator = new BackendCodeGenerator('express', template.spec)
      const result = generator.generate()
      
      expect(result).toBeDefined()
      expect(result.framework).toBe('express')
      
      // Step 3: Verify all required components
      expect(result.files).toBeDefined()
      expect(result.dependencies).toBeDefined()
      expect(result.scripts).toBeDefined()
      expect(result.documentation).toBeDefined()
      
      // Step 4: Verify deployment readiness
      expect(result.dockerFile).toBeDefined()
      expect(result.files['docker-compose.yml']).toBeDefined()
      expect(result.files['.env.example']).toBeDefined()
      
      console.log('✅ Backend integration test completed successfully')
      console.log(`✅ Generated ${Object.keys(result.files).length} files`)
      console.log(`✅ Included ${result.dependencies.length} dependencies`)
    })
  })
})

// Export test utilities for external testing
export const BackendTestUtils = {
  getTestTemplate: (id: string) => BackendTemplateLibrary.getTemplateById(id),
  generateTestBackend: (framework: BackendFramework, templateId: string) => {
    const template = BackendTemplateLibrary.getTemplateById(templateId)
    if (!template) throw new Error(`Template ${templateId} not found`)
    
    const generator = new BackendCodeGenerator(framework, template.spec)
    return generator.generate()
  },
  validateGeneratedCode: (code: any) => {
    expect(code).toBeDefined()
    expect(code.framework).toBeDefined()
    expect(code.files).toBeDefined()
    expect(code.dependencies).toBeDefined()
    return true
  }
}
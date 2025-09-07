// Phase 3B: Backend Templates Library

import { BackendSpec, BackendTemplate, ModelSpec, EndpointSpec } from '../types/backend'

export class BackendTemplateLibrary {
  static getTemplates(): BackendTemplate[] {
    return [
      this.createCRUDAPITemplate(),
      this.createAuthAPITemplate(),
      this.createECommerceAPITemplate(),
      this.createBlogAPITemplate(),
      this.createSaaSAPITemplate(),
      this.createChatAPITemplate(),
      this.createFileUploadAPITemplate(),
      this.createAnalyticsAPITemplate()
    ]
  }

  static createCRUDAPITemplate(): BackendTemplate {
    const userModel: ModelSpec = {
      name: 'User',
      tableName: 'users',
      fields: [
        { name: 'id', type: 'uuid', required: true },
        { name: 'email', type: 'email', required: true, unique: true },
        { name: 'name', type: 'string', required: true },
        { name: 'avatar', type: 'url', required: false },
        { name: 'isActive', type: 'boolean', required: true, default: true }
      ],
      relationships: [],
      indexes: [
        { name: 'idx_user_email', fields: ['email'], unique: true }
      ],
      validations: [
        { field: 'email', rules: [{ type: 'email', message: 'Invalid email format' }] }
      ]
    }

    const postModel: ModelSpec = {
      name: 'Post',
      tableName: 'posts',
      fields: [
        { name: 'id', type: 'uuid', required: true },
        { name: 'title', type: 'string', required: true },
        { name: 'content', type: 'text', required: true },
        { name: 'published', type: 'boolean', required: true, default: false },
        { name: 'authorId', type: 'reference', required: true }
      ],
      relationships: [
        { type: 'one-to-many', target: 'User', foreignKey: 'authorId' }
      ],
      indexes: [
        { name: 'idx_post_author', fields: ['authorId'] },
        { name: 'idx_post_published', fields: ['published'] }
      ],
      validations: [
        { field: 'title', rules: [{ type: 'min', value: 3, message: 'Title too short' }] }
      ]
    }

    const endpoints: EndpointSpec[] = [
      // User endpoints
      {
        path: '/users',
        method: 'GET',
        handler: 'getUsers',
        params: [
          { name: 'page', type: 'number', required: false, description: 'Page number' },
          { name: 'limit', type: 'number', required: false, description: 'Items per page' }
        ],
        response: { statusCode: 200, schema: { users: 'User[]', total: 'number' } },
        auth: true,
        description: 'Get paginated list of users'
      },
      {
        path: '/users/:id',
        method: 'GET',
        handler: 'getUserById',
        params: [
          { name: 'id', type: 'uuid', required: true, description: 'User ID' }
        ],
        response: { statusCode: 200, schema: { user: 'User' } },
        auth: true,
        description: 'Get user by ID'
      },
      {
        path: '/users',
        method: 'POST',
        handler: 'createUser',
        body: {
          type: 'json',
          schema: {
            email: { name: 'email', type: 'email', required: true },
            name: { name: 'name', type: 'string', required: true },
            avatar: { name: 'avatar', type: 'url', required: false }
          },
          required: ['email', 'name']
        },
        response: { statusCode: 201, schema: { user: 'User' } },
        auth: false,
        description: 'Create new user'
      },
      {
        path: '/users/:id',
        method: 'PUT',
        handler: 'updateUser',
        params: [
          { name: 'id', type: 'uuid', required: true, description: 'User ID' }
        ],
        body: {
          type: 'json',
          schema: {
            name: { name: 'name', type: 'string', required: false },
            avatar: { name: 'avatar', type: 'url', required: false }
          }
        },
        response: { statusCode: 200, schema: { user: 'User' } },
        auth: true,
        description: 'Update user'
      },
      {
        path: '/users/:id',
        method: 'DELETE',
        handler: 'deleteUser',
        params: [
          { name: 'id', type: 'uuid', required: true, description: 'User ID' }
        ],
        response: { statusCode: 200, schema: { message: 'string' } },
        auth: true,
        description: 'Delete user'
      },
      // Post endpoints
      {
        path: '/posts',
        method: 'GET',
        handler: 'getPosts',
        params: [
          { name: 'published', type: 'boolean', required: false, description: 'Filter by published status' }
        ],
        response: { statusCode: 200, schema: { posts: 'Post[]' } },
        auth: false,
        description: 'Get all posts'
      },
      {
        path: '/posts',
        method: 'POST',
        handler: 'createPost',
        body: {
          type: 'json',
          schema: {
            title: { name: 'title', type: 'string', required: true },
            content: { name: 'content', type: 'text', required: true },
            published: { name: 'published', type: 'boolean', required: false }
          },
          required: ['title', 'content']
        },
        response: { statusCode: 201, schema: { post: 'Post' } },
        auth: true,
        description: 'Create new post'
      }
    ]

    const spec: BackendSpec = {
      id: 'crud-api-template',
      name: 'CRUD API',
      framework: 'express',
      database: {
        type: 'postgresql',
        name: 'crud_api_db',
        connection: {
          host: 'localhost',
          port: 5432,
          username: 'postgres',
          password: 'password',
          database: 'crud_api_db'
        },
        models: [userModel, postModel]
      },
      api: {
        basePath: '/api',
        version: 'v1',
        endpoints,
        middleware: [
          { name: 'cors', type: 'cors', order: 1 },
          { name: 'auth', type: 'auth', order: 2 },
          { name: 'validation', type: 'validation', order: 3 }
        ],
        documentation: {
          title: 'CRUD API',
          description: 'Basic CRUD operations for users and posts',
          version: '1.0.0',
          servers: [
            { url: 'http://localhost:8000', description: 'Development server', environment: 'development' }
          ]
        }
      },
      auth: {
        type: 'jwt',
        provider: 'local',
        config: {
          secretKey: 'your-secret-key',
          expirationTime: '24h',
          refreshToken: true
        }
      },
      deployment: {
        platform: 'railway',
        config: {
          buildCommand: 'npm run build',
          nodeVersion: '18'
        },
        environment: [
          {
            name: 'production',
            variables: {
              NODE_ENV: 'production',
              PORT: '8000'
            },
            secrets: ['DATABASE_URL', 'JWT_SECRET']
          }
        ],
        ci: {
          provider: 'github',
          workflow: {
            name: 'Deploy to Railway',
            triggers: ['push'],
            jobs: [
              {
                name: 'deploy',
                steps: [
                  { name: 'Checkout', action: 'actions/checkout@v3' },
                  { name: 'Deploy', action: 'railway-deploy@v1' }
                ]
              }
            ]
          }
        }
      },
      version: '1.0.0'
    }

    return {
      id: 'crud-api',
      name: 'CRUD API',
      description: 'Complete CRUD API with user management and posts',
      framework: 'express',
      features: ['crud-api', 'authentication', 'authorization'],
      spec,
      preview: '/api/docs',
      tags: ['crud', 'api', 'users', 'posts', 'basic']
    }
  }

  static createAuthAPITemplate(): BackendTemplate {
    const userModel: ModelSpec = {
      name: 'User',
      tableName: 'users',
      fields: [
        { name: 'id', type: 'uuid', required: true },
        { name: 'email', type: 'email', required: true, unique: true },
        { name: 'password', type: 'string', required: true },
        { name: 'firstName', type: 'string', required: true },
        { name: 'lastName', type: 'string', required: true },
        { name: 'avatar', type: 'url', required: false },
        { name: 'isEmailVerified', type: 'boolean', required: true, default: false },
        { name: 'lastLogin', type: 'datetime', required: false },
        { name: 'role', type: 'string', required: true, default: 'user' }
      ],
      relationships: [],
      indexes: [
        { name: 'idx_user_email', fields: ['email'], unique: true },
        { name: 'idx_user_role', fields: ['role'] }
      ],
      validations: [
        { field: 'email', rules: [{ type: 'email', message: 'Invalid email format' }] },
        { field: 'password', rules: [{ type: 'min', value: 8, message: 'Password too short' }] }
      ]
    }

    const endpoints: EndpointSpec[] = [
      {
        path: '/auth/register',
        method: 'POST',
        handler: 'register',
        body: {
          type: 'json',
          schema: {
            email: { name: 'email', type: 'email', required: true },
            password: { name: 'password', type: 'string', required: true },
            firstName: { name: 'firstName', type: 'string', required: true },
            lastName: { name: 'lastName', type: 'string', required: true }
          },
          required: ['email', 'password', 'firstName', 'lastName']
        },
        response: { statusCode: 201, schema: { user: 'User', token: 'string' } },
        auth: false,
        description: 'Register new user'
      },
      {
        path: '/auth/login',
        method: 'POST',
        handler: 'login',
        body: {
          type: 'json',
          schema: {
            email: { name: 'email', type: 'email', required: true },
            password: { name: 'password', type: 'string', required: true }
          },
          required: ['email', 'password']
        },
        response: { statusCode: 200, schema: { user: 'User', token: 'string' } },
        auth: false,
        description: 'Login user'
      },
      {
        path: '/auth/logout',
        method: 'POST',
        handler: 'logout',
        response: { statusCode: 200, schema: { message: 'string' } },
        auth: true,
        description: 'Logout user'
      },
      {
        path: '/auth/me',
        method: 'GET',
        handler: 'getCurrentUser',
        response: { statusCode: 200, schema: { user: 'User' } },
        auth: true,
        description: 'Get current user'
      },
      {
        path: '/auth/refresh',
        method: 'POST',
        handler: 'refreshToken',
        response: { statusCode: 200, schema: { token: 'string' } },
        auth: true,
        description: 'Refresh access token'
      },
      {
        path: '/auth/forgot-password',
        method: 'POST',
        handler: 'forgotPassword',
        body: {
          type: 'json',
          schema: {
            email: { name: 'email', type: 'email', required: true }
          },
          required: ['email']
        },
        response: { statusCode: 200, schema: { message: 'string' } },
        auth: false,
        description: 'Send password reset email'
      },
      {
        path: '/auth/reset-password',
        method: 'POST',
        handler: 'resetPassword',
        body: {
          type: 'json',
          schema: {
            token: { name: 'token', type: 'string', required: true },
            password: { name: 'password', type: 'string', required: true }
          },
          required: ['token', 'password']
        },
        response: { statusCode: 200, schema: { message: 'string' } },
        auth: false,
        description: 'Reset password with token'
      }
    ]

    const spec: BackendSpec = {
      id: 'auth-api-template',
      name: 'Authentication API',
      framework: 'express',
      database: {
        type: 'postgresql',
        name: 'auth_api_db',
        connection: {
          host: 'localhost',
          port: 5432,
          username: 'postgres',
          password: 'password',
          database: 'auth_api_db'
        },
        models: [userModel]
      },
      api: {
        basePath: '/api',
        version: 'v1',
        endpoints,
        middleware: [
          { name: 'cors', type: 'cors', order: 1 },
          { name: 'ratelimit', type: 'ratelimit', order: 2 },
          { name: 'auth', type: 'auth', order: 3 }
        ],
        documentation: {
          title: 'Authentication API',
          description: 'Complete authentication system with JWT',
          version: '1.0.0',
          servers: [
            { url: 'http://localhost:8000', description: 'Development server', environment: 'development' }
          ]
        }
      },
      auth: {
        type: 'jwt',
        provider: 'local',
        config: {
          secretKey: 'your-secret-key',
          expirationTime: '15m',
          refreshToken: true,
          twoFactor: false,
          passwordPolicy: {
            minLength: 8,
            requireUppercase: true,
            requireLowercase: true,
            requireNumbers: true,
            requireSpecialChars: true
          }
        },
        roles: [
          { name: 'user', description: 'Regular user', permissions: ['read:profile', 'update:profile'] },
          { name: 'admin', description: 'Administrator', permissions: ['*'] }
        ]
      },
      deployment: {
        platform: 'vercel',
        config: {
          buildCommand: 'npm run build',
          nodeVersion: '18'
        },
        environment: [
          {
            name: 'production',
            variables: {
              NODE_ENV: 'production'
            },
            secrets: ['DATABASE_URL', 'JWT_SECRET', 'EMAIL_SERVICE_KEY']
          }
        ],
        ci: {
          provider: 'github',
          workflow: {
            name: 'Deploy to Vercel',
            triggers: ['push'],
            jobs: [
              {
                name: 'deploy',
                steps: [
                  { name: 'Checkout', action: 'actions/checkout@v3' },
                  { name: 'Deploy', action: 'vercel-action@v1' }
                ]
              }
            ]
          }
        }
      },
      version: '1.0.0'
    }

    return {
      id: 'auth-api',
      name: 'Authentication API',
      description: 'Complete authentication system with JWT, password reset, and role-based access',
      framework: 'express',
      features: ['authentication', 'authorization', 'email', 'logging'],
      spec,
      preview: '/api/auth/docs',
      tags: ['auth', 'jwt', 'security', 'users', 'rbac']
    }
  }

  static createECommerceAPITemplate(): BackendTemplate {
    const productModel: ModelSpec = {
      name: 'Product',
      tableName: 'products',
      fields: [
        { name: 'id', type: 'uuid', required: true },
        { name: 'name', type: 'string', required: true },
        { name: 'description', type: 'text', required: true },
        { name: 'price', type: 'number', required: true },
        { name: 'salePrice', type: 'number', required: false },
        { name: 'sku', type: 'string', required: true, unique: true },
        { name: 'category', type: 'string', required: true },
        { name: 'brand', type: 'string', required: false },
        { name: 'images', type: 'array', required: true },
        { name: 'inventory', type: 'number', required: true, default: 0 },
        { name: 'isActive', type: 'boolean', required: true, default: true }
      ],
      relationships: [],
      indexes: [
        { name: 'idx_product_sku', fields: ['sku'], unique: true },
        { name: 'idx_product_category', fields: ['category'] },
        { name: 'idx_product_active', fields: ['isActive'] }
      ],
      validations: [
        { field: 'price', rules: [{ type: 'min', value: 0, message: 'Price must be positive' }] }
      ]
    }

    const orderModel: ModelSpec = {
      name: 'Order',
      tableName: 'orders',
      fields: [
        { name: 'id', type: 'uuid', required: true },
        { name: 'userId', type: 'reference', required: true },
        { name: 'status', type: 'string', required: true, default: 'pending' },
        { name: 'items', type: 'json', required: true },
        { name: 'total', type: 'number', required: true },
        { name: 'shippingAddress', type: 'json', required: true },
        { name: 'paymentMethod', type: 'string', required: true },
        { name: 'paymentStatus', type: 'string', required: true, default: 'pending' }
      ],
      relationships: [
        { type: 'one-to-many', target: 'User', foreignKey: 'userId' }
      ],
      indexes: [
        { name: 'idx_order_user', fields: ['userId'] },
        { name: 'idx_order_status', fields: ['status'] }
      ],
      validations: []
    }

    const spec: BackendSpec = {
      id: 'ecommerce-api-template',
      name: 'E-Commerce API',
      framework: 'express',
      database: {
        type: 'postgresql',
        name: 'ecommerce_db',
        connection: {
          host: 'localhost',
          port: 5432,
          username: 'postgres',
          password: 'password',
          database: 'ecommerce_db'
        },
        models: [productModel, orderModel]
      },
      api: {
        basePath: '/api',
        version: 'v1',
        endpoints: [
          {
            path: '/products',
            method: 'GET',
            handler: 'getProducts',
            params: [
              { name: 'category', type: 'string', required: false, description: 'Filter by category' },
              { name: 'brand', type: 'string', required: false, description: 'Filter by brand' },
              { name: 'minPrice', type: 'number', required: false, description: 'Minimum price' },
              { name: 'maxPrice', type: 'number', required: false, description: 'Maximum price' }
            ],
            response: { statusCode: 200, schema: { products: 'Product[]', total: 'number' } },
            auth: false,
            description: 'Get products with filters'
          },
          {
            path: '/orders',
            method: 'POST',
            handler: 'createOrder',
            body: {
              type: 'json',
              schema: {
                items: { name: 'items', type: 'array', required: true },
                shippingAddress: { name: 'shippingAddress', type: 'json', required: true },
                paymentMethod: { name: 'paymentMethod', type: 'string', required: true }
              },
              required: ['items', 'shippingAddress', 'paymentMethod']
            },
            response: { statusCode: 201, schema: { order: 'Order' } },
            auth: true,
            description: 'Create new order'
          }
        ],
        middleware: [
          { name: 'cors', type: 'cors', order: 1 },
          { name: 'auth', type: 'auth', order: 2 }
        ],
        documentation: {
          title: 'E-Commerce API',
          description: 'Complete e-commerce backend with products and orders',
          version: '1.0.0',
          servers: [
            { url: 'http://localhost:8000', description: 'Development server', environment: 'development' }
          ]
        }
      },
      auth: {
        type: 'jwt',
        provider: 'local',
        config: {
          secretKey: 'your-secret-key',
          expirationTime: '24h'
        }
      },
      deployment: {
        platform: 'aws',
        config: {
          buildCommand: 'npm run build',
          nodeVersion: '18'
        },
        environment: [
          {
            name: 'production',
            variables: {
              NODE_ENV: 'production'
            },
            secrets: ['DATABASE_URL', 'JWT_SECRET', 'STRIPE_SECRET_KEY']
          }
        ],
        ci: {
          provider: 'github',
          workflow: {
            name: 'Deploy to AWS',
            triggers: ['push'],
            jobs: [
              {
                name: 'deploy',
                steps: [
                  { name: 'Checkout', action: 'actions/checkout@v3' },
                  { name: 'Deploy', action: 'aws-deploy@v1' }
                ]
              }
            ]
          }
        }
      },
      version: '1.0.0'
    }

    return {
      id: 'ecommerce-api',
      name: 'E-Commerce API',
      description: 'Complete e-commerce backend with products, orders, and payments',
      framework: 'express',
      features: ['crud-api', 'authentication', 'payment', 'file-upload'],
      spec,
      preview: '/api/products',
      tags: ['ecommerce', 'products', 'orders', 'payments', 'stripe']
    }
  }

  static createBlogAPITemplate(): BackendTemplate {
    // Implementation for blog API template
    const spec: BackendSpec = {
      id: 'blog-api-template',
      name: 'Blog API',
      framework: 'fastapi',
      database: { type: 'mongodb', name: 'blog_db', connection: {}, models: [] },
      api: { basePath: '/api', version: 'v1', endpoints: [], middleware: [], documentation: { title: 'Blog API', description: 'Blog management system', version: '1.0.0', servers: [] } },
      auth: { type: 'jwt', provider: 'local', config: {} },
      deployment: { platform: 'railway', config: {}, environment: [], ci: { provider: 'github', workflow: { name: 'Deploy', triggers: [], jobs: [] } } },
      version: '1.0.0'
    }

    return {
      id: 'blog-api',
      name: 'Blog API',
      description: 'Complete blog system with posts, comments, and categories',
      framework: 'fastapi',
      features: ['crud-api', 'authentication', 'file-upload'],
      spec,
      preview: '/api/posts',
      tags: ['blog', 'cms', 'posts', 'comments']
    }
  }

  static createSaaSAPITemplate(): BackendTemplate {
    // Implementation for SaaS API template
    const spec: BackendSpec = {
      id: 'saas-api-template',
      name: 'SaaS API',
      framework: 'nestjs',
      database: { type: 'postgresql', name: 'saas_db', connection: {}, models: [] },
      api: { basePath: '/api', version: 'v1', endpoints: [], middleware: [], documentation: { title: 'SaaS API', description: 'SaaS platform backend', version: '1.0.0', servers: [] } },
      auth: { type: 'oauth2', provider: 'auth0', config: {} },
      deployment: { platform: 'vercel', config: {}, environment: [], ci: { provider: 'github', workflow: { name: 'Deploy', triggers: [], jobs: [] } } },
      version: '1.0.0'
    }

    return {
      id: 'saas-api',
      name: 'SaaS API',
      description: 'Multi-tenant SaaS platform with subscriptions and billing',
      framework: 'nestjs',
      features: ['authentication', 'authorization', 'payment', 'analytics', 'monitoring'],
      spec,
      preview: '/api/dashboard',
      tags: ['saas', 'multi-tenant', 'subscriptions', 'billing']
    }
  }

  static createChatAPITemplate(): BackendTemplate {
    // Implementation for chat API template
    const spec: BackendSpec = {
      id: 'chat-api-template',
      name: 'Chat API',
      framework: 'express',
      database: { type: 'mongodb', name: 'chat_db', connection: {}, models: [] },
      api: { basePath: '/api', version: 'v1', endpoints: [], middleware: [], documentation: { title: 'Chat API', description: 'Real-time chat system', version: '1.0.0', servers: [] } },
      auth: { type: 'jwt', provider: 'local', config: {} },
      deployment: { platform: 'railway', config: {}, environment: [], ci: { provider: 'github', workflow: { name: 'Deploy', triggers: [], jobs: [] } } },
      version: '1.0.0'
    }

    return {
      id: 'chat-api',
      name: 'Chat API',
      description: 'Real-time chat system with rooms and direct messaging',
      framework: 'express',
      features: ['authentication', 'notifications', 'file-upload'],
      spec,
      preview: '/api/chat',
      tags: ['chat', 'realtime', 'websockets', 'messaging']
    }
  }

  static createFileUploadAPITemplate(): BackendTemplate {
    // Implementation for file upload API template
    const spec: BackendSpec = {
      id: 'file-upload-api-template',
      name: 'File Upload API',
      framework: 'express',
      database: { type: 'postgresql', name: 'files_db', connection: {}, models: [] },
      api: { basePath: '/api', version: 'v1', endpoints: [], middleware: [], documentation: { title: 'File Upload API', description: 'File management system', version: '1.0.0', servers: [] } },
      auth: { type: 'jwt', provider: 'local', config: {} },
      deployment: { platform: 'aws', config: {}, environment: [], ci: { provider: 'github', workflow: { name: 'Deploy', triggers: [], jobs: [] } } },
      version: '1.0.0'
    }

    return {
      id: 'file-upload-api',
      name: 'File Upload API',
      description: 'Secure file upload and management system with cloud storage',
      framework: 'express',
      features: ['authentication', 'file-upload', 'logging'],
      spec,
      preview: '/api/files',
      tags: ['files', 'upload', 's3', 'storage']
    }
  }

  static createAnalyticsAPITemplate(): BackendTemplate {
    // Implementation for analytics API template
    const spec: BackendSpec = {
      id: 'analytics-api-template',
      name: 'Analytics API',
      framework: 'fastapi',
      database: { type: 'postgresql', name: 'analytics_db', connection: {}, models: [] },
      api: { basePath: '/api', version: 'v1', endpoints: [], middleware: [], documentation: { title: 'Analytics API', description: 'Analytics and reporting system', version: '1.0.0', servers: [] } },
      auth: { type: 'apikey', provider: 'local', config: {} },
      deployment: { platform: 'gcp', config: {}, environment: [], ci: { provider: 'github', workflow: { name: 'Deploy', triggers: [], jobs: [] } } },
      version: '1.0.0'
    }

    return {
      id: 'analytics-api',
      name: 'Analytics API',
      description: 'Real-time analytics and reporting system with dashboards',
      framework: 'fastapi',
      features: ['analytics', 'monitoring', 'logging'],
      spec,
      preview: '/api/analytics',
      tags: ['analytics', 'reporting', 'metrics', 'dashboard']
    }
  }

  static getTemplateById(id: string): BackendTemplate | undefined {
    return this.getTemplates().find(template => template.id === id)
  }

  static getTemplatesByFramework(framework: string): BackendTemplate[] {
    return this.getTemplates().filter(template => template.framework === framework)
  }

  static getTemplatesByFeature(feature: string): BackendTemplate[] {
    return this.getTemplates().filter(template => template.features.includes(feature as any))
  }
}
// Phase 3B: Backend Code Generators

import { 
  BackendSpec, 
  BackendGeneratedCode, 
  ModelSpec, 
  EndpointSpec, 
  BackendFramework,
  DatabaseType,
  AuthType
} from '../types/backend'

export class BackendCodeGenerator {
  private framework: BackendFramework
  private spec: BackendSpec

  constructor(framework: BackendFramework, spec: BackendSpec) {
    this.framework = framework
    this.spec = spec
  }

  generate(): BackendGeneratedCode {
    switch (this.framework) {
      case 'express':
        return this.generateExpress()
      case 'fastapi':
        return this.generateFastAPI()
      case 'nestjs':
        return this.generateNestJS()
      default:
        throw new Error(`Framework ${this.framework} not supported`)
    }
  }

  private generateExpress(): BackendGeneratedCode {
    const files: Record<string, string> = {}
    
    // Main app file
    files['src/app.ts'] = this.generateExpressApp()
    files['src/server.ts'] = this.generateExpressServer()
    
    // Database models
    this.spec.database.models.forEach(model => {
      files[`src/models/${model.name.toLowerCase()}.ts`] = this.generateExpressModel(model)
    })
    
    // API routes
    files['src/routes/index.ts'] = this.generateExpressRoutes()
    this.spec.api.endpoints.forEach(endpoint => {
      const controllerName = this.getControllerName(endpoint.path)
      files[`src/controllers/${controllerName}.ts`] = this.generateExpressController(endpoint)
    })
    
    // Middleware
    files['src/middleware/auth.ts'] = this.generateExpressAuthMiddleware()
    files['src/middleware/validation.ts'] = this.generateExpressValidationMiddleware()
    files['src/middleware/error.ts'] = this.generateExpressErrorMiddleware()
    
    // Database configuration
    files['src/config/database.ts'] = this.generateExpressDatabaseConfig()
    
    // Environment configuration
    files['.env.example'] = this.generateEnvExample()
    files['package.json'] = this.generateExpressPackageJson()
    files['tsconfig.json'] = this.generateTsConfig()
    
    // Docker and deployment
    files['Dockerfile'] = this.generateExpressDockerfile()
    files['docker-compose.yml'] = this.generateDockerCompose()
    
    return {
      framework: 'express',
      files,
      dependencies: this.getExpressDependencies(),
      scripts: this.getExpressScripts(),
      configuration: [],
      dockerFile: files['Dockerfile'],
      documentation: this.generateExpressDocumentation()
    }
  }

  private generateExpressApp(): string {
    return `import express from 'express'
import cors from 'cors'
import helmet from 'helmet'
import morgan from 'morgan'
import compression from 'compression'
import rateLimit from 'express-rate-limit'
import { errorHandler } from './middleware/error'
import { authMiddleware } from './middleware/auth'
import routes from './routes'
import { connectDatabase } from './config/database'

const app = express()

// Security middleware
app.use(helmet())
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}))

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
})
app.use('/api', limiter)

// General middleware
app.use(compression())
app.use(morgan('combined'))
app.use(express.json({ limit: '10mb' }))
app.use(express.urlencoded({ extended: true, limit: '10mb' }))

// Database connection
connectDatabase()

// Authentication middleware
app.use('/api', authMiddleware)

// Routes
app.use('/api', routes)

// Health check
app.get('/health', (req, res) => {
  res.status(200).json({ 
    status: 'OK', 
    timestamp: new Date().toISOString(),
    service: '${this.spec.name}',
    version: '${this.spec.version}'
  })
})

// Error handling
app.use(errorHandler)

export default app`
  }

  private generateExpressServer(): string {
    return `import app from './app'

const PORT = process.env.PORT || 8000

app.listen(PORT, () => {
  console.log(\`🚀 Server running on port \${PORT}\`)
  console.log(\`📚 API Documentation: http://localhost:\${PORT}/api/docs\`)
  console.log(\`🔍 Health Check: http://localhost:\${PORT}/health\`)
})`
  }

  private generateExpressModel(model: ModelSpec): string {
    const fields = model.fields.map(field => {
      const fieldType = this.mapFieldTypeToTypeScript(field.type)
      const optional = field.required ? '' : '?'
      return `  ${field.name}${optional}: ${fieldType}`
    }).join('\n')

    return `export interface ${model.name} {
${fields}
  createdAt?: Date
  updatedAt?: Date
}

export interface Create${model.name} extends Omit<${model.name}, 'id' | 'createdAt' | 'updatedAt'> {}
export interface Update${model.name} extends Partial<Create${model.name}> {}

// Database operations for ${model.name}
export class ${model.name}Repository {
  // Implement database operations here based on your chosen ORM
  // For example, using Prisma, TypeORM, or Mongoose
  
  static async findAll(): Promise<${model.name}[]> {
    // Implementation depends on your database choice
    throw new Error('Implementation required')
  }
  
  static async findById(id: string): Promise<${model.name} | null> {
    // Implementation depends on your database choice
    throw new Error('Implementation required')
  }
  
  static async create(data: Create${model.name}): Promise<${model.name}> {
    // Implementation depends on your database choice
    throw new Error('Implementation required')
  }
  
  static async update(id: string, data: Update${model.name}): Promise<${model.name} | null> {
    // Implementation depends on your database choice
    throw new Error('Implementation required')
  }
  
  static async delete(id: string): Promise<boolean> {
    // Implementation depends on your database choice
    throw new Error('Implementation required')
  }
}`
  }

  private generateExpressRoutes(): string {
    const routes = this.spec.api.endpoints.map(endpoint => {
      const method = endpoint.method.toLowerCase()
      const controllerName = this.getControllerName(endpoint.path)
      const actionName = this.getActionName(endpoint.method, endpoint.path)
      return `router.${method}('${endpoint.path}', ${controllerName}.${actionName})`
    }).join('\n')

    return `import { Router } from 'express'
${this.spec.api.endpoints.map(endpoint => {
  const controllerName = this.getControllerName(endpoint.path)
  return `import * as ${controllerName} from '../controllers/${controllerName}'`
}).filter((value, index, self) => self.indexOf(value) === index).join('\n')}

const router = Router()

${routes}

export default router`
  }

  private generateExpressController(endpoint: EndpointSpec): string {
    const actionName = this.getActionName(endpoint.method, endpoint.path)
    const controllerName = this.getControllerName(endpoint.path)
    
    return `import { Request, Response, NextFunction } from 'express'

export const ${actionName} = async (req: Request, res: Response, next: NextFunction) => {
  try {
    // TODO: Implement ${endpoint.method} ${endpoint.path}
    ${this.generateControllerLogic(endpoint)}
  } catch (error) {
    next(error)
  }
}`
  }

  private generateControllerLogic(endpoint: EndpointSpec): string {
    switch (endpoint.method) {
      case 'GET':
        return `// Fetch data logic
    const data = await SomeRepository.findAll()
    res.status(200).json({ data, success: true })`
      case 'POST':
        return `// Create logic
    const { body } = req
    const newItem = await SomeRepository.create(body)
    res.status(201).json({ data: newItem, success: true })`
      case 'PUT':
      case 'PATCH':
        return `// Update logic
    const { id } = req.params
    const { body } = req
    const updatedItem = await SomeRepository.update(id, body)
    if (!updatedItem) {
      return res.status(404).json({ error: 'Item not found', success: false })
    }
    res.status(200).json({ data: updatedItem, success: true })`
      case 'DELETE':
        return `// Delete logic
    const { id } = req.params
    const deleted = await SomeRepository.delete(id)
    if (!deleted) {
      return res.status(404).json({ error: 'Item not found', success: false })
    }
    res.status(200).json({ message: 'Item deleted successfully', success: true })`
      default:
        return `res.status(200).json({ message: 'Endpoint implemented', success: true })`
    }
  }

  private generateExpressAuthMiddleware(): string {
    return `import { Request, Response, NextFunction } from 'express'
import jwt from 'jsonwebtoken'

export interface AuthenticatedRequest extends Request {
  user?: any
}

export const authMiddleware = (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
  // Skip authentication for public routes
  const publicRoutes = ['/auth/login', '/auth/register', '/health']
  if (publicRoutes.includes(req.path)) {
    return next()
  }

  const token = req.header('Authorization')?.replace('Bearer ', '')
  
  if (!token) {
    return res.status(401).json({ error: 'Access denied. No token provided.', success: false })
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'fallback-secret')
    req.user = decoded
    next()
  } catch (error) {
    res.status(400).json({ error: 'Invalid token.', success: false })
  }
}`
  }

  private generateExpressValidationMiddleware(): string {
    return `import { Request, Response, NextFunction } from 'express'
import { validationResult, ValidationChain } from 'express-validator'

export const validate = (validations: ValidationChain[]) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    // Run all validations
    await Promise.all(validations.map(validation => validation.run(req)))

    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({
        error: 'Validation failed',
        details: errors.array(),
        success: false
      })
    }

    next()
  }
}`
  }

  private generateExpressErrorMiddleware(): string {
    return `import { Request, Response, NextFunction } from 'express'

export interface AppError extends Error {
  statusCode?: number
  isOperational?: boolean
}

export const errorHandler = (err: AppError, req: Request, res: Response, next: NextFunction) => {
  const statusCode = err.statusCode || 500
  const isProduction = process.env.NODE_ENV === 'production'

  console.error(\`Error: \${err.message}\`)
  console.error(\`Stack: \${err.stack}\`)

  const errorResponse = {
    error: isProduction ? 'Something went wrong' : err.message,
    success: false,
    ...(isProduction ? {} : { stack: err.stack })
  }

  res.status(statusCode).json(errorResponse)
}`
  }

  private generateExpressDatabaseConfig(): string {
    const dbType = this.spec.database.type
    
    switch (dbType) {
      case 'postgresql':
        return `import { Pool } from 'pg'

const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME || '${this.spec.database.name}',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'password',
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
})

export const connectDatabase = async () => {
  try {
    await pool.connect()
    console.log('✅ Connected to PostgreSQL database')
  } catch (error) {
    console.error('❌ Database connection failed:', error)
    process.exit(1)
  }
}

export { pool }`
      case 'mongodb':
        return `import { MongoClient, Db } from 'mongodb'

let db: Db

export const connectDatabase = async () => {
  try {
    const client = new MongoClient(process.env.MONGODB_URL || 'mongodb://localhost:27017/${this.spec.database.name}')
    await client.connect()
    db = client.db('${this.spec.database.name}')
    console.log('✅ Connected to MongoDB database')
  } catch (error) {
    console.error('❌ Database connection failed:', error)
    process.exit(1)
  }
}

export const getDatabase = () => {
  if (!db) {
    throw new Error('Database not initialized')
  }
  return db
}`
      default:
        return `// Database configuration for ${dbType}
export const connectDatabase = async () => {
  console.log('Database connection configuration needed for ${dbType}')
}`
    }
  }

  private generateFastAPI(): BackendGeneratedCode {
    const files: Record<string, string> = {}
    
    // Main app file
    files['main.py'] = this.generateFastAPIMain()
    files['requirements.txt'] = this.generateFastAPIRequirements()
    
    // Database models
    files['models/__init__.py'] = ''
    this.spec.database.models.forEach(model => {
      files[`models/${model.name.toLowerCase()}.py`] = this.generateFastAPIModel(model)
    })
    
    // API routes
    files['routers/__init__.py'] = ''
    this.spec.api.endpoints.forEach(endpoint => {
      const routerName = this.getRouterName(endpoint.path)
      files[`routers/${routerName}.py`] = this.generateFastAPIRouter(endpoint)
    })
    
    // Database configuration
    files['database.py'] = this.generateFastAPIDatabase()
    files['schemas.py'] = this.generateFastAPISchemas()
    
    // Authentication
    files['auth.py'] = this.generateFastAPIAuth()
    
    return {
      framework: 'fastapi',
      files,
      dependencies: this.getFastAPIDependencies(),
      scripts: this.getFastAPIScripts(),
      configuration: [],
      dockerFile: this.generateFastAPIDockerfile(),
      documentation: this.generateFastAPIDocumentation()
    }
  }

  private generateFastAPIMain(): string {
    return `from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.security import HTTPBearer
import uvicorn
from database import engine, Base
${this.spec.api.endpoints.map(endpoint => {
  const routerName = this.getRouterName(endpoint.path)
  return `from routers import ${routerName}`
}).filter((value, index, self) => self.indexOf(value) === index).join('\n')}

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="${this.spec.name}",
    description="${this.spec.name} API",
    version="${this.spec.version}",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers
${this.spec.api.endpoints.map(endpoint => {
  const routerName = this.getRouterName(endpoint.path)
  return `app.include_router(${routerName}.router, prefix="/api")`
}).filter((value, index, self) => self.indexOf(value) === index).join('\n')}

@app.get("/health")
async def health_check():
    return {
        "status": "OK",
        "service": "${this.spec.name}",
        "version": "${this.spec.version}"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)`
  }

  private generateFastAPIModel(model: ModelSpec): string {
    const fields = model.fields.map(field => {
      const fieldType = this.mapFieldTypeToPython(field.type)
      const optional = field.required ? '' : ' = None'
      return `    ${field.name}: ${fieldType}${optional}`
    }).join('\n')

    return `from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ${model.name}(Base):
    __tablename__ = "${model.tableName || model.name.toLowerCase()}s"
    
${fields}
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)`
  }

  private generateFastAPIRouter(endpoint: EndpointSpec): string {
    const routerName = this.getRouterName(endpoint.path)
    const method = endpoint.method.toLowerCase()
    
    return `from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import ResponseModel

router = APIRouter()

@router.${method}("${endpoint.path}")
async def handle_${method}_${routerName}(db: Session = Depends(get_db)):
    """
    ${endpoint.description || `Handle ${endpoint.method} ${endpoint.path}`}
    """
    try:
        # TODO: Implement ${endpoint.method} ${endpoint.path}
        ${this.generateFastAPIEndpointLogic(endpoint)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))`
  }

  private generateFastAPIEndpointLogic(endpoint: EndpointSpec): string {
    switch (endpoint.method) {
      case 'GET':
        return `# Fetch data logic
        result = db.query(SomeModel).all()
        return {"data": result, "success": True}`
      case 'POST':
        return `# Create logic
        # new_item = SomeModel(**request_data)
        # db.add(new_item)
        # db.commit()
        return {"message": "Created successfully", "success": True}`
      case 'PUT':
      case 'PATCH':
        return `# Update logic
        # item = db.query(SomeModel).filter(SomeModel.id == item_id).first()
        # if not item:
        #     raise HTTPException(status_code=404, detail="Item not found")
        return {"message": "Updated successfully", "success": True}`
      case 'DELETE':
        return `# Delete logic
        # item = db.query(SomeModel).filter(SomeModel.id == item_id).first()
        # if not item:
        #     raise HTTPException(status_code=404, detail="Item not found")
        # db.delete(item)
        # db.commit()
        return {"message": "Deleted successfully", "success": True}`
      default:
        return `return {"message": "Endpoint implemented", "success": True}`
    }
  }

  private generateFastAPIDatabase(): string {
    return `from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/${this.spec.database.name}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()`
  }

  private generateFastAPISchemas(): string {
    return `from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime

class ResponseModel(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    error: Optional[str] = None

class PaginatedResponse(ResponseModel):
    data: List[Any]
    total: int
    page: int
    size: int
    pages: int`
  }

  private generateFastAPIAuth(): string {
    return `from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )`
  }

  private generateNestJS(): BackendGeneratedCode {
    // Implementation for NestJS would go here
    // For now, returning a basic structure
    return {
      framework: 'nestjs',
      files: {
        'src/main.ts': '// NestJS main file - implementation needed',
        'src/app.module.ts': '// NestJS app module - implementation needed'
      },
      dependencies: [],
      scripts: {},
      configuration: [],
      documentation: 'NestJS documentation - implementation needed'
    }
  }

  // Helper methods
  private getControllerName(path: string): string {
    const parts = path.split('/').filter(part => part && !part.startsWith(':'))
    return parts[parts.length - 1] || 'base'
  }

  private getActionName(method: string, path: string): string {
    const controller = this.getControllerName(path)
    const actionMap = {
      'GET': 'get',
      'POST': 'create',
      'PUT': 'update',
      'PATCH': 'update',
      'DELETE': 'delete'
    }
    return `${actionMap[method as keyof typeof actionMap] || 'handle'}${controller.charAt(0).toUpperCase() + controller.slice(1)}`
  }

  private getRouterName(path: string): string {
    return this.getControllerName(path)
  }

  private mapFieldTypeToTypeScript(type: string): string {
    const typeMap: Record<string, string> = {
      'string': 'string',
      'number': 'number',
      'boolean': 'boolean',
      'date': 'Date',
      'datetime': 'Date',
      'text': 'string',
      'json': 'any',
      'uuid': 'string',
      'email': 'string',
      'url': 'string',
      'array': 'any[]',
      'reference': 'string'
    }
    return typeMap[type] || 'any'
  }

  private mapFieldTypeToPython(type: string): string {
    const typeMap: Record<string, string> = {
      'string': 'str',
      'number': 'int',
      'boolean': 'bool',
      'date': 'datetime',
      'datetime': 'datetime',
      'text': 'str',
      'json': 'dict',
      'uuid': 'str',
      'email': 'str',
      'url': 'str',
      'array': 'list',
      'reference': 'str'
    }
    return typeMap[type] || 'str'
  }

  private getExpressDependencies() {
    return [
      { name: 'express', version: '^4.18.0', type: 'production' as const },
      { name: 'cors', version: '^2.8.5', type: 'production' as const },
      { name: 'helmet', version: '^7.0.0', type: 'production' as const },
      { name: 'morgan', version: '^1.10.0', type: 'production' as const },
      { name: 'compression', version: '^1.7.4', type: 'production' as const },
      { name: 'express-rate-limit', version: '^6.7.0', type: 'production' as const },
      { name: 'jsonwebtoken', version: '^9.0.0', type: 'production' as const },
      { name: 'express-validator', version: '^6.15.0', type: 'production' as const },
      { name: 'dotenv', version: '^16.0.0', type: 'production' as const },
      { name: '@types/express', version: '^4.17.0', type: 'development' as const },
      { name: '@types/cors', version: '^2.8.0', type: 'development' as const },
      { name: '@types/morgan', version: '^1.9.0', type: 'development' as const },
      { name: '@types/compression', version: '^1.7.0', type: 'development' as const },
      { name: '@types/jsonwebtoken', version: '^9.0.0', type: 'development' as const },
      { name: 'typescript', version: '^5.0.0', type: 'development' as const },
      { name: 'ts-node', version: '^10.9.0', type: 'development' as const },
      { name: 'nodemon', version: '^2.0.0', type: 'development' as const }
    ]
  }

  private getFastAPIDependencies() {
    return [
      { name: 'fastapi', version: '0.104.1', type: 'production' as const },
      { name: 'uvicorn', version: '0.24.0', type: 'production' as const },
      { name: 'sqlalchemy', version: '1.4.23', type: 'production' as const },
      { name: 'pydantic', version: '1.10.12', type: 'production' as const },
      { name: 'python-jose', version: '3.3.0', type: 'production' as const },
      { name: 'python-multipart', version: '0.0.6', type: 'production' as const },
      { name: 'psycopg2-binary', version: '2.9.7', type: 'production' as const },
      { name: 'alembic', version: '1.12.1', type: 'production' as const }
    ]
  }

  private getExpressScripts() {
    return {
      'start': 'node dist/server.js',
      'dev': 'nodemon src/server.ts',
      'build': 'tsc',
      'test': 'jest',
      'lint': 'eslint src/**/*.ts',
      'format': 'prettier --write src/**/*.ts'
    }
  }

  private getFastAPIScripts() {
    return {
      'start': 'uvicorn main:app --host 0.0.0.0 --port 8000',
      'dev': 'uvicorn main:app --reload',
      'test': 'pytest',
      'lint': 'flake8 .',
      'format': 'black .'
    }
  }

  private generateEnvExample(): string {
    return `# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=${this.spec.database.name}
DB_USER=postgres
DB_PASSWORD=password
DATABASE_URL=postgresql://postgres:password@localhost:5432/${this.spec.database.name}

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production

# Application Configuration
NODE_ENV=development
PORT=8000
FRONTEND_URL=http://localhost:3000

# API Configuration
API_VERSION=v1
API_PREFIX=/api

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001`
  }

  private generateExpressPackageJson(): string {
    return JSON.stringify({
      name: this.spec.name.toLowerCase().replace(/\s+/g, '-'),
      version: this.spec.version,
      description: `${this.spec.name} API Backend`,
      main: 'dist/server.js',
      scripts: this.getExpressScripts(),
      dependencies: Object.fromEntries(
        this.getExpressDependencies()
          .filter(dep => dep.type === 'production')
          .map(dep => [dep.name, dep.version])
      ),
      devDependencies: Object.fromEntries(
        this.getExpressDependencies()
          .filter(dep => dep.type === 'development')
          .map(dep => [dep.name, dep.version])
      ),
      keywords: ['api', 'backend', 'express', 'typescript'],
      author: 'Generated by Aether Builder',
      license: 'MIT'
    }, null, 2)
  }

  private generateFastAPIRequirements(): string {
    return this.getFastAPIDependencies()
      .map(dep => `${dep.name}==${dep.version}`)
      .join('\n')
  }

  private generateTsConfig(): string {
    return JSON.stringify({
      compilerOptions: {
        target: 'ES2020',
        module: 'commonjs',
        lib: ['ES2020'],
        outDir: './dist',
        rootDir: './src',
        strict: true,
        esModuleInterop: true,
        skipLibCheck: true,
        forceConsistentCasingInFileNames: true,
        resolveJsonModule: true,
        declaration: true,
        declarationMap: true,
        sourceMap: true
      },
      include: ['src/**/*'],
      exclude: ['node_modules', 'dist', 'tests']
    }, null, 2)
  }

  private generateExpressDockerfile(): string {
    return `FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["npm", "start"]`
  }

  private generateFastAPIDockerfile(): string {
    return `FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`
  }

  private generateDockerCompose(): string {
    const dbService = this.spec.database.type === 'postgresql' 
      ? `
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ${this.spec.database.name}
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data`
      : `
  db:
    image: mongo:6-slim
    environment:
      MONGO_INITDB_DATABASE: ${this.spec.database.name}
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db`

    return `version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=${this.spec.database.type}://postgres:password@db:5432/${this.spec.database.name}
    depends_on:
      - db
    volumes:
      - .:/app
      - /app/node_modules
${dbService}

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  ${this.spec.database.type === 'postgresql' ? 'postgres_data:' : 'mongo_data:'}`
  }

  private generateExpressDocumentation(): string {
    return `# ${this.spec.name} API Documentation

## Overview
${this.spec.name} backend API built with Express.js and TypeScript.

## Getting Started

### Prerequisites
- Node.js 18+
- ${this.spec.database.type} database
- Redis (optional, for caching)

### Installation
\`\`\`bash
npm install
cp .env.example .env
# Update .env with your configuration
npm run dev
\`\`\`

### Docker Setup
\`\`\`bash
docker-compose up -d
\`\`\`

## API Endpoints

${this.spec.api.endpoints.map(endpoint => `
### ${endpoint.method} ${endpoint.path}
${endpoint.description || 'No description provided'}

**Authentication:** ${endpoint.auth ? 'Required' : 'Not required'}
**Response:** ${endpoint.response.statusCode}
`).join('\n')}

## Database Schema

${this.spec.database.models.map(model => `
### ${model.name}
${model.fields.map(field => `- **${field.name}**: ${field.type} ${field.required ? '(required)' : '(optional)'}`).join('\n')}
`).join('\n')}

## Environment Variables
See \`.env.example\` for all required environment variables.

## Testing
\`\`\`bash
npm test
\`\`\`

## Deployment
The API can be deployed using Docker or directly to cloud platforms like Railway, Heroku, or Vercel.
`
  }

  private generateFastAPIDocumentation(): string {
    return `# ${this.spec.name} API Documentation

## Overview
${this.spec.name} backend API built with FastAPI and Python.

## Getting Started

### Prerequisites
- Python 3.11+
- ${this.spec.database.type} database

### Installation
\`\`\`bash
pip install -r requirements.txt
# Update environment variables
python main.py
\`\`\`

### Docker Setup
\`\`\`bash
docker-compose up -d
\`\`\`

## API Documentation
Visit \`http://localhost:8000/api/docs\` for interactive API documentation.

## Database Schema
${this.spec.database.models.map(model => `
### ${model.name}
${model.fields.map(field => `- **${field.name}**: ${field.type} ${field.required ? '(required)' : '(optional)'}`).join('\n')}
`).join('\n')}
`
  }
}
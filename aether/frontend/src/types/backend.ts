// Phase 3B: Backend Integration Types

export interface BackendSpec {
  id: string
  name: string
  framework: BackendFramework
  database: DatabaseSpec
  api: ApiSpec
  auth: AuthSpec
  deployment: DeploymentSpec
  version: string
}

export type BackendFramework = 
  | 'express' 
  | 'fastapi' 
  | 'nestjs' 
  | 'flask' 
  | 'django' 
  | 'spring-boot'

export interface DatabaseSpec {
  type: DatabaseType
  name: string
  connection: ConnectionConfig
  models: ModelSpec[]
  migrations?: MigrationSpec[]
  seeding?: SeedingSpec[]
}

export type DatabaseType = 
  | 'postgresql' 
  | 'mysql' 
  | 'mongodb' 
  | 'sqlite' 
  | 'redis'
  | 'supabase'
  | 'planetscale'
  | 'prisma'

export interface ConnectionConfig {
  host?: string
  port?: number
  username?: string
  password?: string
  database?: string
  url?: string
  options?: Record<string, any>
}

export interface ModelSpec {
  name: string
  tableName?: string
  fields: FieldSpec[]
  relationships?: RelationshipSpec[]
  indexes?: IndexSpec[]
  validations?: ValidationSpec[]
}

export interface FieldSpec {
  name: string
  type: FieldType
  required: boolean
  unique?: boolean
  default?: any
  constraints?: FieldConstraints
  description?: string
}

export type FieldType = 
  | 'string' 
  | 'number' 
  | 'boolean' 
  | 'date' 
  | 'datetime' 
  | 'text' 
  | 'json' 
  | 'uuid' 
  | 'email' 
  | 'url'
  | 'array'
  | 'reference'

export interface FieldConstraints {
  minLength?: number
  maxLength?: number
  min?: number
  max?: number
  pattern?: string
  enum?: string[]
}

export interface RelationshipSpec {
  type: 'one-to-one' | 'one-to-many' | 'many-to-many'
  target: string
  foreignKey?: string
  localKey?: string
  through?: string
}

export interface IndexSpec {
  name: string
  fields: string[]
  unique?: boolean
  type?: 'btree' | 'hash' | 'gin' | 'gist'
}

export interface ValidationSpec {
  field: string
  rules: ValidationRule[]
}

export interface ValidationRule {
  type: 'required' | 'email' | 'min' | 'max' | 'regex' | 'custom'
  value?: any
  message?: string
}

export interface MigrationSpec {
  version: string
  description: string
  up: string[]
  down: string[]
}

export interface SeedingSpec {
  model: string
  data: Record<string, any>[]
}

export interface ApiSpec {
  basePath: string
  version: string
  endpoints: EndpointSpec[]
  middleware: MiddlewareSpec[]
  documentation: DocumentationSpec
}

export interface EndpointSpec {
  path: string
  method: HttpMethod
  handler: string
  middleware?: string[]
  params?: ParamSpec[]
  body?: BodySpec
  response: ResponseSpec
  auth?: boolean
  validation?: ValidationSpec[]
  description?: string
}

export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'

export interface ParamSpec {
  name: string
  type: FieldType
  required: boolean
  description?: string
}

export interface BodySpec {
  type: 'json' | 'form' | 'multipart'
  schema: Record<string, FieldSpec>
  required?: string[]
}

export interface ResponseSpec {
  statusCode: number
  schema: Record<string, any>
  headers?: Record<string, string>
}

export interface MiddlewareSpec {
  name: string
  type: MiddlewareType
  config?: Record<string, any>
  order: number
}

export type MiddlewareType = 
  | 'cors' 
  | 'auth' 
  | 'logging' 
  | 'compression' 
  | 'ratelimit' 
  | 'validation' 
  | 'custom'

export interface DocumentationSpec {
  title: string
  description: string
  version: string
  contact?: ContactInfo
  license?: LicenseInfo
  servers: ServerInfo[]
}

export interface ContactInfo {
  name: string
  email: string
  url?: string
}

export interface LicenseInfo {
  name: string
  url?: string
}

export interface ServerInfo {
  url: string
  description: string
  environment: 'development' | 'staging' | 'production'
}

export interface AuthSpec {
  type: AuthType
  provider?: AuthProvider
  config: AuthConfig
  permissions?: PermissionSpec[]
  roles?: RoleSpec[]
}

export type AuthType = 
  | 'jwt' 
  | 'oauth2' 
  | 'basic' 
  | 'session' 
  | 'apikey'
  | 'custom'

export type AuthProvider = 
  | 'local' 
  | 'google' 
  | 'github' 
  | 'auth0' 
  | 'firebase' 
  | 'supabase'
  | 'clerk'

export interface AuthConfig {
  secretKey?: string
  expirationTime?: string
  refreshToken?: boolean
  twoFactor?: boolean
  passwordPolicy?: PasswordPolicy
  socialLogin?: SocialLoginConfig[]
}

export interface PasswordPolicy {
  minLength: number
  requireUppercase: boolean
  requireLowercase: boolean
  requireNumbers: boolean
  requireSpecialChars: boolean
}

export interface SocialLoginConfig {
  provider: AuthProvider
  clientId: string
  clientSecret?: string
  scopes: string[]
}

export interface PermissionSpec {
  name: string
  description: string
  resource: string
  actions: string[]
}

export interface RoleSpec {
  name: string
  description: string
  permissions: string[]
}

export interface DeploymentSpec {
  platform: DeploymentPlatform
  config: DeploymentConfig
  environment: EnvironmentConfig[]
  ci: CIConfig
}

export type DeploymentPlatform = 
  | 'vercel' 
  | 'netlify' 
  | 'aws' 
  | 'gcp' 
  | 'azure' 
  | 'railway' 
  | 'heroku'
  | 'digitalocean'

export interface DeploymentConfig {
  buildCommand?: string
  outputDirectory?: string
  nodeVersion?: string
  environmentVariables?: Record<string, string>
  customDomains?: string[]
}

export interface EnvironmentConfig {
  name: string
  url?: string
  variables: Record<string, string>
  secrets: string[]
}

export interface CIConfig {
  provider: 'github' | 'gitlab' | 'bitbucket' | 'custom'
  workflow: WorkflowSpec
}

export interface WorkflowSpec {
  name: string
  triggers: string[]
  jobs: JobSpec[]
}

export interface JobSpec {
  name: string
  steps: StepSpec[]
  environment?: string
}

export interface StepSpec {
  name: string
  action: string
  with?: Record<string, any>
}

// Backend Code Generation Types
export interface BackendGeneratedCode {
  framework: BackendFramework
  files: Record<string, string>
  dependencies: PackageDependency[]
  scripts: Record<string, string>
  configuration: ConfigurationFile[]
  dockerFile?: string
  documentation: string
}

export interface PackageDependency {
  name: string
  version: string
  type: 'production' | 'development'
}

export interface ConfigurationFile {
  name: string
  content: string
  type: 'json' | 'yaml' | 'env' | 'js' | 'ts'
}

// Backend Templates
export interface BackendTemplate {
  id: string
  name: string
  description: string
  framework: BackendFramework
  features: BackendFeature[]
  spec: BackendSpec
  preview: string
  tags: string[]
}

export type BackendFeature = 
  | 'authentication' 
  | 'authorization' 
  | 'crud-api' 
  | 'file-upload' 
  | 'email' 
  | 'notifications' 
  | 'payment' 
  | 'analytics' 
  | 'logging' 
  | 'monitoring'
  | 'testing'
  | 'documentation'

// Full-Stack Integration
export interface FullStackProject {
  id: string
  name: string
  frontend: {
    framework: string
    spec: any // InterfaceSpec from builder.ts
  }
  backend: BackendSpec
  deployment: FullStackDeployment
  integration: IntegrationConfig
}

export interface FullStackDeployment {
  frontend: DeploymentConfig
  backend: DeploymentConfig
  database: DatabaseDeployment
  cdn?: CDNConfig
}

export interface DatabaseDeployment {
  provider: string
  plan: string
  region: string
  backups: boolean
  scaling: ScalingConfig
}

export interface ScalingConfig {
  auto: boolean
  minInstances: number
  maxInstances: number
  cpuThreshold: number
  memoryThreshold: number
}

export interface CDNConfig {
  provider: string
  regions: string[]
  caching: CachingConfig
}

export interface CachingConfig {
  staticAssets: number
  apiResponses: number
  defaultTTL: number
}

export interface IntegrationConfig {
  apiBaseUrl: string
  authFlow: 'sso' | 'separate' | 'unified'
  dataFlow: DataFlowConfig[]
  errorHandling: ErrorHandlingConfig
}

export interface DataFlowConfig {
  source: string
  target: string
  transformation?: string
  realtime: boolean
}

export interface ErrorHandlingConfig {
  strategy: 'fail-fast' | 'graceful' | 'retry'
  retryPolicy?: RetryPolicy
  logging: boolean
  monitoring: boolean
}

export interface RetryPolicy {
  maxAttempts: number
  backoffStrategy: 'linear' | 'exponential'
  initialDelay: number
  maxDelay: number
}
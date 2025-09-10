# Aether Agents Frontend

Modern React frontend for the Aether Agents platform built with TypeScript, Tailwind CSS, and Framer Motion.

## Features

- **Modern React**: Built with React 18, TypeScript, and functional components
- **Responsive Design**: Mobile-first design with Tailwind CSS
- **Smooth Animations**: Framer Motion for elegant transitions and interactions
- **Authentication**: JWT-based authentication with protected routes
- **Agent Management**: Full CRUD operations for AI agents
- **Interactive Dashboard**: Real-time agent monitoring and execution
- **Pricing Page**: Multi-tier subscription showcase
- **Interactive Demo**: Live agent interface generation demo

## Quick Start

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Set up Environment**
   ```bash
   # Create .env file (optional)
   echo "REACT_APP_API_URL=http://localhost:8000/api/v1" > .env
   ```

3. **Start Development Server**
   ```bash
   npm start
   ```

4. **Build for Production**
   ```bash
   npm run build
   ```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Navbar.tsx      # Navigation component
│   ├── ProtectedRoute.tsx # Authentication guard
│   ├── PricingSection.tsx # Pricing tiers display
│   └── InteractiveDemo.tsx # Agent demo interface
├── pages/              # Main application pages
│   ├── LandingPage.tsx # Marketing landing page
│   ├── Login.tsx       # User authentication
│   ├── Register.tsx    # User registration
│   └── Dashboard.tsx   # Agent management dashboard
├── contexts/           # React contexts
│   └── AuthContext.tsx # Authentication state management
├── hooks/              # Custom React hooks
├── utils/              # Utility functions
│   └── api.ts          # API client and endpoints
├── types/              # TypeScript type definitions
│   └── index.ts        # Application types
└── App.tsx             # Main application component
```

## Key Features

### Authentication System
- JWT-based authentication
- Protected routes
- Automatic token refresh
- Login/register forms with validation

### Agent Management
- Create, edit, delete agents
- Real-time execution
- Agent status monitoring
- Execution history tracking

### Modern UI/UX
- Dark theme with Aether branding
- Responsive design (mobile-first)
- Smooth animations and transitions
- Loading states and error handling

### API Integration
- Axios HTTP client with interceptors
- Automatic token management
- Error handling and user feedback
- React Query for server state management

## Technology Stack

- **React 18** - Modern React with hooks
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **React Router** - Client-side routing
- **React Query** - Server state management
- **Axios** - HTTP client
- **React Hook Form** - Form handling
- **React Hot Toast** - Toast notifications
- **Lucide React** - Icon library

## Development

### Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

### Environment Variables

- `REACT_APP_API_URL` - Backend API URL (default: http://localhost:8000/api/v1)

### Styling Guidelines

- Use Tailwind CSS utility classes
- Follow the Aether design system colors
- Implement responsive design patterns
- Add smooth animations with Framer Motion

## Deployment

The frontend is designed for deployment to:

- **Netlify** - Automatic deployment from Git
- **Vercel** - Serverless deployment
- **AWS S3 + CloudFront** - Static hosting with CDN
- **Docker** - Containerized deployment

### Build Configuration

```bash
# Production build
npm run build

# Serve locally
npx serve -s build
```

## Contributing

1. Follow the existing code style
2. Use TypeScript for all new components
3. Add proper error handling
4. Test responsive design
5. Ensure accessibility compliance

## License

MIT License - see LICENSE file for details.
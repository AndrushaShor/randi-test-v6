# Frontend Team - Construction Project Portal

## Overview

This is a responsive React + TypeScript + Tailwind CSS UI for managing construction projects and their locations. Built with Vite for fast development and optimized builds.

## Architecture

### Tech Stack
- **React 18** - UI library with hooks
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router v6** - Client-side routing
- **React Query (@tanstack/react-query)** - Server state management
- **React Hook Form** - Form handling and validation
- **Axios** - HTTP client

### Project Structure

```
/src
  /api              # API integration layer
    client.ts       # Axios configuration
    projects.ts     # Projects API service
    locations.ts    # Locations API service
  /components       # Reusable UI components
    Layout.tsx      # Main layout with navigation
    Button.tsx      # Button component
    Card.tsx        # Card container
    Input.tsx       # Input field with validation
    Select.tsx      # Select dropdown
    Textarea.tsx    # Textarea field
    SearchBar.tsx   # Search input
    Badge.tsx       # Status badges
    LoadingSpinner.tsx
    Modal.tsx       # Modal dialog
  /pages            # Route-level components
    Dashboard.tsx   # Project overview with metrics
    ProjectList.tsx # Browse and filter projects
    ProjectForm.tsx # Create/edit project
    ProjectDetail.tsx # Project details + locations
    LocationForm.tsx # Create/edit location
  /features         # Feature-based modules
    /projects
      ProjectCard.tsx # Project card component
    /locations
      LocationList.tsx # Location list component
  /hooks            # Custom React hooks
    useProjects.ts  # Projects React Query hooks
    useLocations.ts # Locations React Query hooks
  /types            # TypeScript type definitions
    index.ts        # Project, Location, API types
  /utils            # Utility functions
    formatters.ts   # Date, currency formatting
    validation.ts   # Form validation helpers
  App.tsx           # Main app with routing
  main.tsx          # Entry point
  index.css         # Global styles + Tailwind
```

## Setup & Running

### Install Dependencies
```bash
npm install
```

### Development Server
```bash
npm run dev
```
Runs on `http://localhost:3000` with:
- Host: `0.0.0.0` (required for Docker)
- AllowedHosts: `true` (required for Docker host access)
- API Proxy: `/api` → `http://Backend:3000` (proxies to backend service)

### Build for Production
```bash
npm run build
```

### Lint Code
```bash
npm run lint
```

## API Integration

The frontend communicates with the Backend service via API proxy:
- Frontend calls: `/api/projects`, `/api/locations/{id}`, etc.
- Vite proxies these to: `http://Backend:3000/api/...`

### Expected API Endpoints

**Projects:**
- `GET /api/projects` - List projects (supports query params: status, search, dates)
- `POST /api/projects` - Create project
- `GET /api/projects/{id}` - Get project details
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

**Locations:**
- `GET /api/projects/{id}/locations` - List locations for project
- `POST /api/projects/{id}/locations` - Create location
- `GET /api/locations/{id}` - Get location details
- `PUT /api/locations/{id}` - Update location
- `DELETE /api/locations/{id}` - Delete location

## Key Features Implemented

### 1. Dashboard
- Project metrics cards (total, active, completed, on-hold)
- Quick overview of construction portfolio
- Responsive grid layout

### 2. Project List
- Search by project name
- Filter by status (planning, in-progress, on-hold, completed, cancelled)
- Clickable project cards
- Empty state with call-to-action

### 3. Project Forms
- Create new projects
- Edit existing projects
- Form validation (required fields, date validation, budget validation)
- React Hook Form for performance
- Error handling and display

### 4. Project Detail
- Full project information display
- Edit/Delete actions
- Locations section with add button
- Formatted dates and currency

### 5. Location Management
- Add locations to projects
- Edit/delete locations
- Coordinate support (latitude/longitude)
- Address fields (street, city, state, zip, country)
- Notes field for additional info

## Component Design Patterns

### Composition
- Small, focused components (`Button`, `Input`, `Card`)
- Compound components (`Layout`, `Modal`)
- Feature modules (`ProjectCard`, `LocationList`)

### Type Safety
- All props interfaces defined
- Strict TypeScript configuration
- Type inference from API responses

### State Management
- React Query for server state (caching, refetching, optimistic updates)
- React Hook Form for form state
- URL state for routing (React Router)

### Accessibility
- Semantic HTML elements
- ARIA labels where needed
- Keyboard navigation support
- Focus management in modals
- Form validation errors announced

## Responsive Design

Breakpoints (Tailwind defaults):
- **Mobile**: < 640px (sm)
- **Tablet**: 640px - 1024px (sm - lg)
- **Desktop**: > 1024px (lg)

All components are mobile-first and responsive:
- Grid layouts collapse on mobile
- Navigation adapts to screen size
- Cards stack on mobile, side-by-side on desktop

## Key Decisions

### 1. React Query over Redux
- Simpler API state management
- Built-in caching and refetching
- Automatic loading/error states
- Less boilerplate

### 2. React Hook Form
- Better performance (uncontrolled inputs)
- Less re-renders
- Built-in validation
- Smaller bundle size vs Formik

### 3. Tailwind CSS
- Fast development
- Consistent design system
- Tree-shaking (only used classes in bundle)
- No CSS-in-JS runtime cost

### 4. Vite over CRA
- 10-100x faster dev server startup
- HMR that stays fast as app grows
- Better build performance
- Native ESM support

### 5. Feature-based organization
- Scales better than type-based folders
- Easier to find related code
- Supports code splitting by feature

### 6. API Proxy in Vite
- Avoids CORS issues in development
- Simpler frontend code (relative URLs)
- Easy to change backend URL

## Next Steps

### Features to Implement
1. **Dashboard Project Cards** - Visual project cards with metrics
2. **Location Map View** - Show locations on a map using coordinates
3. **Project Progress Tracking** - Visual progress bars based on dates
4. **Bulk Operations** - Select multiple projects for batch actions
5. **Export/Import** - CSV export of projects and locations
6. **Advanced Filters** - Date range pickers, budget filters
7. **Sorting** - Sort by name, date, budget, status

### Enhancements
1. **Dark Mode** - Add theme toggle
2. **Animations** - Smooth transitions and loading states
3. **Notifications** - Toast messages for actions (success/error)
4. **Skeleton Loaders** - Better loading UX
5. **Infinite Scroll** - For large project lists
6. **Search Autocomplete** - Suggestions as you type
7. **Drag & Drop** - Reorder projects or locations

### Testing
1. Add Vitest for unit tests
2. Add React Testing Library for component tests
3. Add Playwright for E2E tests
4. Add visual regression testing

### Performance
1. Code splitting by route
2. Image optimization
3. Bundle size analysis
4. Lazy load heavy components

## TypeScript Interfaces

### Core Types

```typescript
type ProjectStatus = 'planning' | 'in-progress' | 'on-hold' | 'completed' | 'cancelled';

interface Project {
  id: number;
  name: string;
  description?: string;
  status: ProjectStatus;
  start_date: string;
  end_date?: string;
  budget?: number;
  actual_cost?: number;
  client_name?: string;
  project_manager?: string;
  created_at: string;
  updated_at: string;
}

interface Location {
  id: number;
  project_id: number;
  name: string;
  address: string;
  city?: string;
  state?: string;
  zip_code?: string;
  country?: string;
  latitude?: number;
  longitude?: number;
  notes?: string;
  created_at: string;
  updated_at: string;
}
```

## Configuration

### Vite Config (`vite.config.ts`)
```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    allowedHosts: true, // CRITICAL for Docker
    proxy: {
      '/api': 'http://Backend:3000'
    }
  }
})
```

### Tailwind Config
- Custom color palette (primary, secondary)
- Extended theme
- Content paths configured for all source files

## Troubleshooting

### Port 3000 already in use
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### API calls failing
1. Check backend is running: `curl http://Backend:3000/api/projects`
2. Check proxy config in `vite.config.ts`
3. Check network tab in browser DevTools

### TypeScript errors
```bash
# Check TypeScript config
npx tsc --noEmit
```

### Styling issues
```bash
# Rebuild Tailwind
npm run dev
```

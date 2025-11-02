# CrackSmith Frontend

React-based mobile-friendly frontend for the CrackSmith hash cracking service.

## Features

- Beautiful, responsive UI optimized for mobile
- User authentication with JWT
- PIN code security
- Job submission and management
- Statistics dashboard with charts
- Admin panel
- Real-time job status updates
- Material-UI components

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
# Create .env file
VITE_API_URL=http://localhost:5000/api
```

3. Start development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Build

Build for production:
```bash
npm run build
```

The build output will be in the `build` directory.

## Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── components/       # Reusable components
│   ├── Layout.jsx    # Main layout with navigation
│   └── PrivateRoute.jsx  # Protected route wrapper
├── context/          # React context providers
│   └── AuthContext.jsx   # Authentication context
├── pages/            # Page components
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── Dashboard.jsx
│   ├── Jobs.jsx
│   ├── Statistics.jsx
│   ├── Settings.jsx
│   ├── About.jsx
│   └── Admin.jsx
├── services/         # API services
│   ├── api.js        # Axios instance with interceptors
│   └── index.js      # Service functions
├── App.jsx           # Main app component
├── main.jsx          # Entry point
└── index.css         # Global styles
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Key Features

### Authentication
- Login with username/password
- Optional PIN code for extra security
- JWT token management with auto-refresh
- Persistent sessions

### Dashboard
- Submit new hash cracking jobs
- View recent jobs
- Quick statistics overview
- Account type display

### Jobs
- View all submitted jobs
- Filter by status
- Delete queued/failed jobs
- View cracking results
- Pagination support

### Statistics
- Job status distribution (pie chart)
- Hash type distribution (pie chart)
- Jobs over time (line chart)
- Success rate metrics

### Settings
- Update PIN code
- View account information
- App preferences
- Security settings

### Admin Panel (Admin users only)
- Platform statistics
- User management
- Installation tracking
- Job monitoring

## Technologies

- React 18
- React Router 6
- Material-UI 5
- Recharts (charts)
- Axios (HTTP client)
- JWT-decode
- Vite (build tool)

## Mobile Optimization

The app is fully responsive and optimized for mobile devices:
- Touch-friendly interface
- Responsive layouts
- Mobile-first design
- Optimized performance
- PWA-ready

## License

MIT License - See LICENSE file

# Frontend File Structure

## Root Directory
```
frontend/
├── app/                    # Next.js App Router directory
├── components/             # React components
├── public/                # Static assets
├── middleware.ts          # Route protection middleware
├── next.config.ts         # Next.js configuration
├── tsconfig.json          # TypeScript configuration
├── postcss.config.mjs     # PostCSS configuration
├── package.json           # Dependencies
├── .gitignore            # Git ignore rules
└── .env.local            # Environment variables (create this)
```

## App Directory Structure
```
app/
├── layout.tsx             # Root layout with AuthProvider
├── page.tsx               # Homepage (redirects to /login)
├── globals.css            # Global styles
├── favicon.ico            # Site icon
├── api/
│   └── auth/
│       └── [...nextauth]/
│           └── route.ts   # NextAuth API route
├── login/
│   └── page.tsx           # Login page (/login)
└── dashboard/
    └── page.tsx           # Dashboard page (/dashboard)
```

## Components Directory
```
components/
├── auth-provider.tsx      # SessionProvider wrapper
└── MonitorCard.tsx        # Camera feed component
```

## Key Files

### Authentication
- `middleware.ts` - Protects /dashboard routes
- `app/api/auth/[...nextauth]/route.ts` - NextAuth configuration
- `components/auth-provider.tsx` - Session context provider
- `app/login/page.tsx` - Login form

### Pages
- `app/page.tsx` - Root page (redirects to /login)
- `app/dashboard/page.tsx` - Protected dashboard with camera feeds

### Components
- `components/MonitorCard.tsx` - Live camera feed card with controls

## Environment Variables Required

Create `.env.local` in the `frontend/` directory:
```env
AUTH_USERNAME=admin
AUTH_PASSWORD=your_password
NEXTAUTH_SECRET=your_secret_key
NEXTAUTH_URL=http://localhost:3000
```

See `ENV_SETUP.md` for detailed setup instructions.


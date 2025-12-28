# Environment Variables Setup

NextAuth requires environment variables to work. Create a `.env.local` file in the `frontend` directory with the following:

```env
# Authentication credentials
AUTH_USERNAME=admin
AUTH_PASSWORD=your_secure_password_here

# NextAuth secret (generate a random string)
# You can generate one using: openssl rand -base64 32
NEXTAUTH_SECRET=your_nextauth_secret_key_here

# NextAuth URL (optional, defaults to http://localhost:3000)
NEXTAUTH_URL=http://localhost:3001
```

## Quick Setup

1. Create `.env.local` file in the `frontend` directory
2. Copy the content above
3. Replace `your_secure_password_here` with your desired password
4. Replace `your_nextauth_secret_key_here` with a random secret (or use the fallback for development)
5. Restart the dev server

## Generate NEXTAUTH_SECRET

On Windows PowerShell:
```powershell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```

Or use an online generator: https://generate-secret.vercel.app/32



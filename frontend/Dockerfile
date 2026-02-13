FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Build the Next.js app for production
RUN npm run build

# Expose port
EXPOSE 3000

# Run production server (listens on 0.0.0.0 by default)
CMD ["npm", "run", "start"]

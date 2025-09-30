# Stage 1: Build Angular app
FROM --platform=$BUILDPLATFORM node:24.9.0-bullseye-slim as builder

WORKDIR /app

# Install Angular CLI
RUN npm install -g @angular/cli@20

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy source code and build
COPY . .
RUN ng build --configuration production

# Stage 2: Serve with ng serve (on 0.0.0.0:4201)
CMD ["ng", "serve", "--configuration=production", "--host", "0.0.0.0", "--port", "4201"]
FROM node:20-alpine

WORKDIR /app

# Install deps first (cache friendly)
COPY package*.json ./
RUN npm ci

# Copy the rest
COPY . .

EXPOSE 5173

# Vite must listen on 0.0.0.0 inside a container
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]

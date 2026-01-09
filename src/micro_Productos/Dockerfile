# Dockerfile para Microservicio de Productos
FROM node:18-alpine

WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
RUN npm install --production

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 5002

# Comando para ejecutar la aplicación
CMD ["node", "app.js"]

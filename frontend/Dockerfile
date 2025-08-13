# Stage 1: istall dependencies and build
FROM node:22-alpine AS build

WORKDIR /app
COPY package*.json .npmrc ./

RUN npm ci

COPY . .
RUN npm run build

# Stage 2: serve the build
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

CMD [ "nginx", "-g", "daemon off;" ]
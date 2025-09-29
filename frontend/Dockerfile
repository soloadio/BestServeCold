FROM --platform=$BUILDPLATFORM node:24.9.0-bullseye-slim as builder

RUN mkdir /src
WORKDIR /src

RUN npm install -g @angular/cli@13

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
CMD ["ng", "serve", "--host", "0.0.0.0"]
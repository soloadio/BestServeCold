FROM node:lts AS development
ARG NODE_ENV=production
ENV NODE_ENV $NODE_ENV

WORKDIR /src

# Set PORT to 81
ARG PORT=81
ENV PORT $PORT
EXPOSE $PORT 9229 9230

COPY package.json /src/package.json
COPY package-lock.json /src/package-lock.json
RUN npm ci

COPY . /src

# Ensure Node listens on $PORT
CMD ["node", "build/index.js"]
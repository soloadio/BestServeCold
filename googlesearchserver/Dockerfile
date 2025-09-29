FROM node:lts AS development
ARG NODE_ENV=production
ENV NODE_ENV $NODE_ENV


WORKDIR /src


ARG PORT=80
ENV PORT $PORT
EXPOSE $PORT 9229 9230

COPY package.json /src/package.json
COPY package-lock.json /src/package-lock.json
RUN npm ci

COPY . /src

CMD ["node", "build/index.js"]
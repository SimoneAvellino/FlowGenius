FROM node:21.5.0

WORKDIR /usr/app

COPY /producer .

RUN npm install -g npm@10.7.0
RUN npm install



CMD ["npm", "start"]
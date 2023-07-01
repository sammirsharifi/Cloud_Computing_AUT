
FROM node:alpine3.16
WORKDIR /app
COPY package*.json ./
RUN npm install --registry=https://npm.iranrepo.ir/
COPY . .
CMD [ "npm", "start" ]
EXPOSE 80

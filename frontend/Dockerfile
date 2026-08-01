FROM node:24-alpine

WORKDIR /app

RUN npm install -g live-server

COPY . .

EXPOSE 3000

CMD ["live-server", "--port=3000", "--host=0.0.0.0"]
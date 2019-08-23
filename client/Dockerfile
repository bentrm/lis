FROM node:lts

COPY . /app

WORKDIR /app
RUN npm install

ENTRYPOINT ["npm"]
CMD ["build"]

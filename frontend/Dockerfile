FROM node:22.5-alpine AS dev

# ENV CI=true
ENV PORT=8000

# WORKDIR /
# RUN npx create-react-app frontend

WORKDIR /frontend

# COPY package.json /code/package.json
# COPY package-lock.json /code/package-lock.json
# RUN npm start
# COPY . .
EXPOSE 8000
# dev
EXPOSE 8001

CMD [ "npm", "start" ]
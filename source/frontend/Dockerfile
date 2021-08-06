FROM node as build-stage
LABEL authors="박경규 <kkpark@clouflake.com"
WORKDIR /
ADD . .
RUN yarn install
RUN yarn run build

# production stage
FROM nginx:stable-alpine as production-stage
MAINTAINER kkpark@clouflake.com
COPY  ./docker/nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build-stage /dist /usr/share/nginx/html
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]

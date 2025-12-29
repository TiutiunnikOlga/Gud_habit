FROM nginx:1.25-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/nginx.conf

RUN mkdir -p /var/www/html/static /var/www/html/media

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]

FROM nginx:alpine

# Copy static frontend assets
COPY index.html  /usr/share/nginx/html/index.html
COPY css/        /usr/share/nginx/html/css/
COPY js/         /usr/share/nginx/html/js/

# Replace default Nginx config with our custom one
COPY nginx.conf  /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

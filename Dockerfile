FROM nginx:alpine

# Copy web files to default nginx html directory
COPY index.html /usr/share/nginx/html/index.html
COPY README.md /usr/share/nginx/html/README.md

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

from nginx:alpine
run "cp -r public/* /usr/share/nginx/html/"
expose 80 
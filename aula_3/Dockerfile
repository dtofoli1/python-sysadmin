
FROM ubuntu

RUN apt update && apt install apache2 -y

COPY index.html /var/www/html/index.html

COPY entrypoint.sh /usr/local/bin/

ENTRYPOINT [ "sh", "/usr/local/bin/entrypoint.sh" ]

CMD [ "/bin/bash" ]
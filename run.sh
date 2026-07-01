#!/bin/bash

INPUT=$1

case "$INPUT" in
    start)
        sudo docker run -d --name mycontainer --env-file .env -p 80:80 myimage
        ;;
    remove)
        sudo docker rm -f mycontainer
        ;;
    restart)
        sudo docker restart mycontainer
        ;;
    active)
        sudo docker ps
        ;;
    logs)
        sudo docker logs -f mycontainer
        ;;
    *)
        exit 1
        ;;
esac
#!/bin/bash
docker run -d  \
    --name dev-postgres \
    -e POSTGRES_PASSWORD=1122 \
    -v ${HOME}/work/sbercloud/database/:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:alpine
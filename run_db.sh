#!/usr/bin/env bash
docker stop markybox
docker rm markybox
docker run -d -p 5432 -e POSTGRES_PASSWORD=Cfhfnjd123 -e POSTGRES_USER=marky -e POSTGRES_DB=markybox --name markybox postgres:10.5-alpine
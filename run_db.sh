#!/usr/bin/env bash
docker stop markybox
docker rm markybox
docker run --name postgres-db -e POSTGRES_PASSWORD=docker -p 5432:5432 -d postgres
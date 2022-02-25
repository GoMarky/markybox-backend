create role marky WITH LOGIN PASSWORD 'password';
create database markybox;
GRANT ALL PRIVILEGES ON DATABASE markybox TO marky;

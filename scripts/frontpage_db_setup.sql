DROP DATABASE IF EXISTS frontpage;
CREATE DATABASE frontpage;
DROP USER IF EXISTS frontpage;
CREATE USER frontpage;
ALTER USER frontpage with encrypted password 'frontpage';
ALTER USER frontpage CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE frontpage TO frontpage;

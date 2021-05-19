Self-hosted RSS news aggregator for your browser home page

![PC View](docs/img/PC.png)

<img src="docs/img/Mobile%20Dark.jpg" alt="Mobile Dark" width="400px;"/>
<img src="docs/img/Mobile%20Light.jpg" alt="Mobile Light" width="400px;"/>


# Features
- PC/Mobile view
- Dark Theme
- Automatically update every 15 mins.


# Demo
https://frontpageshowcase.herokuapp.com/feeds/

May take 10-20 secs as Heroku wakes sleeping container up.

# Setup

## Requirements
- PostgreSQL Server
    - Create database and user  for this application. See `scripts/db/setup_postgres.sql` for detail.

## Docker Compose

1. Create `.env` file with following format. 
    - `SECRET_KEY`: run `scripts/generate_secret_key.sh`
    - `DATABASE_URL`: `postgres://<username>:<password>@<host>:<port>/<db_name>`

Sample `.env`
```sh
SECRET_KEY=84xC&l)z+FXxp0o8morC(GXF{U0)#pzs6eutXC+*(di~rEtlnN
DATABASE_URL=postgres://frontpage:frontpage@192.168.0.100:5432/frontpage
```


2. Run `docker-compose`
```sh
docker-compose up -d
```

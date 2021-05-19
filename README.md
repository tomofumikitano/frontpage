Self-hosted RSS news aggregator for your browser home page

# Features
- PC/Mobile view
- Dark Theme
- Automatically update feeds every 15 mins

# Screenshots

PC             |
:-------------:|
![PC View](docs/img/PC.png) |

<br/>

Mobile Dark             |  Mobile Light
:-------------------------:|:-------------------------:
<img src="docs/img/Mobile%20Dark.jpg" alt="Mobile Dark" width="350px;"/>  |  <img src="docs/img/Mobile%20Light.jpg" alt="Mobile Light" width="350px;"/>

<br/>


# Demo
https://frontpageshowcase.herokuapp.com/feeds/

May take 10-20 secs before Heroku wakes sleeping container up.


# Setup

## Requirements
- PostgreSQL Server
    - Create database and user  for this application. See `scripts/db/setup_postgres.sql` for detail.

## Docker Compose

1. Create `.env` file with following format. 
```sh
SECRET_KEY=<YOUR SECRET KEY HERE>
DATABASE_URL=postgres://frontpage:frontpage@192.168.0.100:5432/frontpage
```
- `SECRET_KEY`: run `scripts/generate_secret_key.sh`
- `DATABASE_URL`: `postgres://<username>:<password>@<host>:<port>/<db_name>`


2. Run `docker-compose`
```sh
docker-compose up -d
```

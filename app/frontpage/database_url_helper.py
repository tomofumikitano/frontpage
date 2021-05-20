#!/usr/bin/env python3
import os
from urllib.parse import urlparse

ENGINE_LOOKUP = {
    'postgres': 'django.db.backends.postgresql'
}

def load_database_url():

    database_url = os.getenv('DATABASE_URL')
    # print(f"DATABASE_URL: {database_url}")
    if not database_url:
        raise Exception('DATABASE_URL env variable is not deined!')

    o = urlparse(database_url)
    # print(o)

    cred, host = o.netloc.split('@')
    user, password = cred.split(':')
    host, port = host.split(':')

    os.environ['DB_USER'] = user
    os.environ['DB_PASSWORD'] = password
    os.environ['DB_HOST'] = host
    os.environ['DB_PORT'] = port
    os.environ['DB_ENGINE'] = ENGINE_LOOKUP[o.scheme]
    os.environ['DB_NAME'] = o.path.strip('/')

    # print("Set env variables")
    # for k in ['DB_ENGINE', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']:
    #     print(f"{k:>11}: {os.getenv(k)}")

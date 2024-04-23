import os
from psycopg_pool import ConnectionPool

pool=None

def get_pool():
    global pool
    if pool is None:
        from psycopg_pool import ConnectionPool
        pool = ConnectionPool(
            conninfo=os.getenv("DATABASE_URL", "") 
        )
    return pool 
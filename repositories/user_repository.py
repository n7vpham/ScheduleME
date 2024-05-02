from typing import Any
from repositories.db import get_pool
from psycopg.rows import dict_row


def does_user_email_exist(user_email: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        SELECT
                            user_id
                        FROM
                            users
                        WHERE user_email = %s
                        ''', [user_email])
            user_id = cur.fetchone()
            print(user_id)
            return user_id is not None
        
def get_user_by_user_email(user_email: str) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT
                            user_id,
                            user_email,
                            user_password AS hashed_password
                        FROM
                            users
                        WHERE user_email = %s
                        ''', [user_email])
            user = cur.fetchone()
            if user is None:
                raise Exception('User not found')
            return user        


def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT
                            user_id,
                            user_fname,
                            user_lname,
                            user_email,
                            user_since
                        FROM
                            users
                        WHERE user_id = %s
                        ''', [user_id])
            return cur.fetchone()
        

def create_user(user_fname: str,user_lname: str,user_email: str, user_password: str) -> dict[str, Any]:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        INSERT INTO users (user_fname, user_lname, user_email, user_password)
                        VALUES (%s, %s, %s, %s)
                        RETURNING user_id
                        ''', [user_fname, user_lname, user_email, user_password]
                        )
            user_id = cur.fetchone()
            
            if user_id is None:
                raise Exception('failed to create user')
            
            return {
                'user_id': user_id,
                'user_email': user_email
            }
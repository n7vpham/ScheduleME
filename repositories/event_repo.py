from repositories.db import get_pool
from psycopg.rows import dict_row

def get_all_events_for_table():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT
                            event_id,
                            event_name, 
                            start_time,
                            end_time, 
                            event_address
                        FROM 
                            events
                        ;
                        ''')
            return cur.fetchall()
        
def get_event_address_for_table():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT
                            event_address
                        FROM 
                            events
                        ;
                        ''')
            
            event_addressdb = cur.fetchone()
            return event_addressdb
        
def get_event_by_id(event_id : int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT
                            event_id,
                            event_name, 
                            event_description,
                            start_time,
                            end_time, 
                            event_address
                        FROM 
                            events
                        WHERE event_id = %s
                        ;
                        ''', [event_id])
            return cur.fetchone()
        
def create_event(host_id: int, event_name: str, event_description: str, start_time: str, end_time: str, event_address: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        INSERT INTO events
                            (host_id, event_name, event_description, start_time, end_time, event_address)
                        VALUES
                            (%s, %s, %s, %s, %s, %s)
                        RETURNING event_id
                        ;
                        ''', [host_id, event_name, event_description, start_time, end_time, event_address])
            res = cur.fetchone()
            if not res:
                raise Exception('Failed to create event')
            return res[0]
            
        
from repositories.db import get_pool
from psycopg.rows import dict_row

def get_all_events_for_table():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT
                            title, 
                        start_time,
                        end_time, 
                        address
                        FROM 
                            events
                        ;
                        ''')
            return cur.fetchall()
        
#this function was meant to implement the get_event_by_title function from event_repo.py( Single even)
   
        
        

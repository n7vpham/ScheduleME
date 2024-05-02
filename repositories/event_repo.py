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
            
        
def delete_event(event_id : int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        DELETE
                        FROM
                            events
                        WHERE event_id = %s
                        ;
                        ''', [event_id])
            return None; 
            res = cur.fetchone()
            if res: 
                raise Exception('Failed to delete event.')
            return res[0]

#edit event function
#update event name
def update_eventName(event_id:int, event_name: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        UPDATE
                            events
                        SET
                            event_name = %s
                        WHERE
                            event_id = %s
                        ;
                        ''', [event_id, event_name])
            return None


#update event description
def update_eventDescription(event_id:int, event_description: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        UPDATE
                            events
                        SET
                            event_description = %s
                        WHERE
                            event_id = %s
                        ;
                        ''', [event_id, event_description])
            return None


#update event start time
def update_eventStartTime(event_id:int, start_time: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        UPDATE
                            events
                        SET
                            start_time = %s
                        WHERE
                            event_id = %s
                        ;
                        ''', [event_id, start_time])
            return None


#update event end time
def update_eventEndTime(event_id:int, end_time: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        UPDATE
                            events
                        SET
                            end_time = %s
                        WHERE
                            event_id = %s
                        ;
                        ''', [event_id, end_time])
            return None


#update event address
def update_eventAddress(event_id:int, event_address: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        UPDATE
                            events
                        SET
                            event_address = %s
                        WHERE
                            event_id = %s
                        ;
                        ''', [event_id, event_address])
            return None


def get_all_events_by_user_id(user_id:int):
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
                        WHERE host_id = %s
                        ;
                        ''', [user_id])
            return cur.fetchall()

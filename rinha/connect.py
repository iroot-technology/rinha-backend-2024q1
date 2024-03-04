import psycopg2
from config import load_db_config

def connect():
    """ Connect to the PostgreSQL database server """
    config = load_db_config()
    try:
        with psycopg2.connect(**config) as pconn:
            print('')
        return pconn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

#if __name__ == '__main__':
    #config = load_db_config()
    #connect(config)
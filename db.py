import mysql.connector
from mysql.connector import Error


db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Mbappe87!!",
    "database": "userDB"
}

# Create a global MySQL Connection Pool
mysql_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config)

def get_mysql_connection():
    # Get a connection from the pool
    return mysql_pool.get_connection()

def query_db(query, args=(), one=False):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def modify_db(query, args=()):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute(query, args)
    conn.commit()
    lastrowid = cursor.lastrowid
    cursor.close()
    conn.close()
    return lastrowid

def upload_message(sender_id, receiver_id, message_content):
    query = """
    INSERT INTO messages (sender_id, receiver_id, message_content, timestamp)
    VALUES (%s, %s, %s, NOW())
    """
    args = (sender_id, receiver_id, message_content)
    lastrowid = modify_db(query, args)
    return lastrowid
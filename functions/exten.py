import mysql.connector
from settings import db

def get_list():
    sip_dict = {}

    try:
        db_connection = mysql.connector.connect(
            host=db['host'], 
            user=db['user'], 
            passwd=db['passwd'], 
            database=db['db_manutencao']
            )
        cursor = db_connection.cursor()
        query = "SELECT username, callerid FROM sip" 
        cursor.execute(query)

        for (username, callerid) in cursor:
            sip_dict[username] = callerid

        cursor.close()
        db_connection.commit()
        db_connection.close()
        
    except:
        pass

    return sip_dict

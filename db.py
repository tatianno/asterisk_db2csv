
from datetime import date
import mysql.connector
from settings import db


class mysql_conn():

  def __init__(self):
    self.db_connection = mysql.connector.connect(
      host=db['host'], 
      user=db['user'], 
      passwd=db['passwd'], 
      database=db['database']
    )
    self.cursor = self.db_connection.cursor()

  def query(self, query):
    self.cursor.execute(query)
    return self.cursor

  def disconnect(self):
    self.cursor.close()
    self.db_connection.commit()
    self.db_connection.close()
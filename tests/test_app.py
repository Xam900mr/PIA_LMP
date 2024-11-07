import unittest
from Aplicacion_Crud import main
import mysql.connector

class FlaskAppTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = main.test_client()
        self.app.testing = True
 
   
    def test_index(self):
        response = self.app.get('/')  
        self.assertEqual(response.status_code, 200)  
        self.assertIn('Hello, World!', response.data.decode())  

 
class TestDatabaseConnection(unittest.TestCase):
 
    def test_db_connection(self):

        conn = mysql.connector.connect(
            user="root",
            password="ramm160799",
            host="localhost",
            database="adtareas"
        )
        self.assertIsInstance(conn, mysql.connector.MySQLConnection) 
        conn.close()
 

 
if __name__ == '__main__':
    unittest.main()
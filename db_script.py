import psycopg2
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


# Parametters for our connection
myconn = psycopg2.connect(
		database= os.getenv("DBNAME"),
		user= os.getenv("DBUSER"),
		password= os.getenv("DBPASSWORD"),
		host= os.getenv("DBHOST")
		)


# Connect to database

def connect_db():
	
	# Create cursor that will allows us to make sql queries
	mycur= myconn.cursor()
	
	mycur.execute("SELECT version();")
	record = mycur.fetchone()
	print(f"Database Version: {record}")


def create_table():

	connect_db()
	mycur= myconn.cursor()

	commands=''' CREATE TABLE users ( id BIGSERIAL PRIMARY KEY NOT NULL,
					first_name VARCHAR(50) NOT NULL,
					last_name VARCHAR(50) NOT NULL,
					phone VARCHAR(100) NOT NULL,
					email VARCHAR(200) NOT NULL ) '''
	mycur.execute(commands)
	mycur.close()
	myconn.commit()

	print("Table created")


# Add new employees to our table/database
def add_user(first_name, last_name, phone,email):

	connect_db()
	mycur= myconn.cursor()

	commands= ''' INSERT INTO users (first_name, last_name, phone,email) VALUES (%s, %s, %s, %s) '''
	mycur.execute(commands, (first_name, last_name, phone,email))
	print("Registered employee")
	
	
# Erase employees data from our database
def delete_user_data(id):

	connect_db()
	mycur= myconn.cursor()

	commands= ''' DELETE FROM users WHERE id = %s '''
	mycur.execute(commands, [str(id)])
	print("Employee data deleted")


# Update data from our database
def update_user_data(id, first_name, last_name, phone,email):
	
	connect_db()
	mycur=myconn.cursor()

	commands= ''' UPDATE users SET first_name= %s, last_name= %s, phone=%s, email=%s WHERE id=%s '''
	mycur.execute(commands, (id, first_name, last_name, phone,email))
	print("Data update")

	
# Display all data
def show_users():
	
	connect_db()
	mycur=myconn.cursor()
	commands= ''' SELECT * FROM users ORDER BY id ASC'''
	
	mycur.execute(commands)
	myconn.commit()
    
    	rows = mycur.fetchall()

   	for row in rows:
		print("Id =", row[0])
        	print("First Name =", row[1])
        	print("Last Name =", row[2])
        	print("Phone =", row[3])
        	print("Email =", row[4], "\n")

	myconn.commit()
	myconn.close()

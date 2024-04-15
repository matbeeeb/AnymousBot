import sqlite3
import os

srcdir = os.path.abspath(os.getcwd())
bddir = os.path.abspath(os.path.join(srcdir, 'db'))
dbfile = os.path.abspath(os.path.join(bddir, 'anonym_quest_db.sqlite3'))

conn = sqlite3.connect(dbfile)
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER NOT NULL,
        quest_wait INTEGER DEFAULT 0
    )               
""")

def add_user_id(user_id):
    cursor.execute("""
    INSERT INTO users (user_id)
    VALUES (?)                  
""", (user_id,))
    conn.commit()
    
def check_user(user_id):
    #Функция дла проверки наличия пользователя в базе данных 
    cursor.execute(
	"""
	SELECT *
    FROM users 
    WHERE user_id = ?
	""",(user_id,))
    result = cursor.fetchone()
    return result

def check_quest_wait(user_id):
    #Функция дла проверки наличия пользователя в базе данных 
    cursor.execute(
	"""
	SELECT quest_wait
    FROM users 
    WHERE user_id = ?
	""",(user_id,))
    result = cursor.fetchone()
    return result

def update_quest_await(question_wait, user_id):
    cursor.execute("""
    UPDATE users        
    SET quest_wait=?  
    WHERE user_id=?         
""", (question_wait, user_id))
    conn.commit()
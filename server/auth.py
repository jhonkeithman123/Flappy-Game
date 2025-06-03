import bcrypt
from db_config import get_db_connection

def signup(username, password):
    db = get_db_connection()
    cursor = db.cursor()

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO players (username, password_hash) VALUES (%s, %s", (username, hashed_pw))
        db.commit()
        return {"message": "Signup successful!"}
    except:
        return {"error": "Username already exists"}
    finally:
        cursor.close()
        db.close()

def login(username, password):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT password_hash FROM players WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
        return {"message": "Login Successful!"}
    else:
        return {"error": "Invalid username or password"}

    cursor.close()
    db.close()
import bcrypt
from db_config import get_db_connection
from mysql.connector.errors import IntegrityError

def signup(username, password):
    db = get_db_connection()
    cursor = db.cursor()

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO players (username, password_hash) VALUES (%s, %s)", (username, hashed_pw))
        db.commit()
        return {"message": "Signup successful!"}
    except IntegrityError:
        return {"error": "Username already exists"}
    except Exception as e:
        print(f"Error during signup: {e}")
        return {"error": f"unexpected error occurred: {str(e)}"}
    finally:
        cursor.close()
        db.close()

def login(username, password):
    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("SELECT password_hash FROM players WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
            return {"message": "Login Successful!"}
        else:
            return {"error": "Invalid username or password"}
        
    except IntegrityError:
        return {"error": "Database error occurred"}

    except Exception as e:
        print(f"Error during login: {e}")
        return {"error": f"unexpected error occurred: {str(e)}"}

    finally:
        cursor.close()
        db.close()
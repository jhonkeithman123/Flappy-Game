from flask import Flask
from db_config import get_db_connection
from routes import routes

app = Flask(__name__)
app.register_blueprint(routes)
db = get_db_connection()
cursor = db.cursor()

if __name__ == "__main__":
    app.run(debug=True)
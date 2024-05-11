import os
import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Connect to MongoDB
    # client = MongoClient(os.getenv("MONGODB_URI"))
    client = MongoClient("mongodb+srv://khasihanai:chikaka9@microbloaapp.dtohvyt.mongodb.net/")
   
    # Use a specific database
    app.db = client.microblog

    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            entry_content = request.form.get('content')
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            try:
                # Insert the entry into the database
                app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
            except Exception as e:
                # Handle database errors
                return f"An error occurred: {str(e)}"

        # Retrieve entries from the database
        entries = app.db.entries.find({})

        # Format entries with date for display
        entries_with_date = [(entry["content"], entry["date"],
                              datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d"))
                             for entry in entries]

        return render_template('home.html', entries=entries_with_date)

    return app


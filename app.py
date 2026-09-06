import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_apscheduler import APScheduler
from models import db, ChatHistory
from bot_engine import generate_bot_response
from scraper import scrape_internee_data

load_dotenv()

# Detect Vercel Environment
IS_VERCEL = os.getenv("VERCEL") == "1"

# Top-level Flask App Instance required by Vercel
app = Flask(__name__, instance_path='/tmp' if IS_VERCEL else None)

# Database Configuration
if IS_VERCEL:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/internee_chatbot.db"
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///internee_chatbot.db"

app.secret_key = os.getenv("FLASK_SECRET_KEY", "3d9b8a1c4o7f2a5b8c4d0e1f7a4b5n6d")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Database Initialize
db.init_app(app)

# Background Scheduler ONLY on Local System
if not IS_VERCEL:
    try:
        scheduler = APScheduler()

        @scheduler.task('interval', id='scheduled_scrape', hours=24)
        def scheduled_scrape():
            print("Running 24-hour knowledge base refresh...")
            scrape_internee_data()

        scheduler.init_app(app)
        scheduler.start()
    except Exception as e:
        print(f"Scheduler init skipped: {e}")

# Create tables within app context safely
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"DB creation log: {e}")

@app.route("/")
def index():
    try:
        chat_logs = ChatHistory.query.order_by(ChatHistory.timestamp.asc()).all()
        return render_template("dashboard.html", chat_logs=chat_logs)
    except Exception:
        return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()
    
    if not user_message:
        return jsonify({"error": "Empty prompt"}), 400

    try:
        past_chats = ChatHistory.query.order_by(ChatHistory.timestamp.desc()).limit(5).all()
        past_chats.reverse()
    except Exception:
        past_chats = []

    bot_reply = generate_bot_response(user_message, past_chats)

    try:
        new_log = ChatHistory(user_message=user_message, bot_response=bot_reply)
        db.session.add(new_log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    if not os.path.exists("knowledge_base/internee_website_scraped.txt"):
        try:
            scrape_internee_data()
        except Exception:
            pass
            
    app.run(debug=True, port=5000, use_reloader=False)
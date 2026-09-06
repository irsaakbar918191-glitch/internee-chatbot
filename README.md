# Internee.pk - AI Assistant & Intern Chatbot Platform

An enterprise-ready, 24/7 AI-powered chatbot system designed specifically for **Internee.pk** interns. The chatbot handles questions regarding internship tasks, submission guidelines, leave policies, and company FAQs using Retrieval-Augmented Generation (RAG), multi-language Natural Language Understanding (NLU), and background web scraping.

---

## Key Features

* **Authentication System:** Secure User Registration and Login with password hashing (`Werkzeug`).
* **Multi-Language NLU Support:** Understands queries in English, Roman Urdu, Urdu, and other regional variations.
* **Smart Knowledge Base (RAG):** Answers queries strictly using Internee.pk PDF guidelines and scraped website text.
* **Automated Web Scraper:** Built-in `BeautifulSoup` script to fetch latest FAQs and portal updates directly from `internee.pk`.
* **24-Hour Scheduler:** Integrates `APScheduler` to automatically re-scrape and refresh the knowledge base every 24 hours.
* **Persistent Conversation Memory:** Saves chat logs per user in a `SQLite` database (`internee_chatbot.db`) for context retention and previous query lookups.
* **Source Attribution:** Explicitly cites referenced files (`.pdf` or `.txt`) at the bottom of AI responses.
* **Modern UI/UX:** Responsive, dark-themed interactive dashboard crafted with Tailwind CSS.

---

## Tech Stack & Tools

| Area | Technology / Library |
| --- | --- |
| **Backend Framework** | Python, Flask, Flask-SQLAlchemy |
| **Database** | SQLite (User Authentication & Chat Logs) |
| **AI / NLU Model** | Hugging Face Inference API (`meta-llama/Llama-3.2-3B-Instruct`) |
| **Document Processing** | `pdfplumber` (PDF extraction) |
| **Web Scraping & Automation** | `BeautifulSoup4`, `requests`, `Flask-APScheduler` |
| **Frontend UI** | HTML5, JavaScript (Fetch API), Tailwind CSS |
| **IDE Environment** | Visual Studio Code |

---

## Project Folder Structure

```text
internee-chatbot/
│
├── knowledge_base/               # Knowledge Base Directory
│   ├── internee_rules.txt        # Policy/FAQ text guidelines
│   └── internee_website_scraped.txt # Auto-scraped site content
│
├── instance/                     # Auto-created by Flask
│   └── internee_chatbot.db       # SQLite Database
│
├── static/                       # Custom Frontend Assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── chat.js
│
├── templates/                    # Dashboard HTML Views
│   ├── login.html                # Login & Registration Page
│   └── dashboard.html            # Interactive Chat Dashboard
│
├── .env                          # Secret keys & API Tokens
├── .gitignore                    # Version control ignore file
├── app.py                        # Main Flask server & API routes
├── bot_engine.py                 # NLU, Context Retrieval & AI logic
├── models.py                     # SQLAlchemy Database Schemas
├── scraper.py                    # Web scraper for Internee.pk
├── requirements.txt              # Project Python Dependencies
└── README.md                     # Project documentation
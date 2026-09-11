"""
Real Estate FAQ Chatbot - Demo / Portfolio Project
----------------------------------------------------
A simple Flask backend that powers a website chat widget for a
real estate agency. It answers common questions about properties
(location, price, size, availability) using Google's Gemini API
(free tier, no card needed), and captures the visitor's name +
phone number as a "lead" whenever they show interest - saved to
a simple SQLite database.

HOW TO USE THIS AS A DEMO / SELLABLE PROJECT:
1. Edit AGENCY_INFO and PROPERTIES below with a real (or sample)
   agency's details - this is what makes the bot "custom" per client.
2. Get a free Gemini API key from https://aistudio.google.com/apikey
   and set it as GEMINI_API_KEY (see README.md).
3. Run: python app.py
4. Open http://127.0.0.1:5000 in your browser and chat with the bot.
5. Leads (name + phone) get saved automatically to leads.db - you
   can show a client this as proof the bot captures real inquiries.
"""

import os
import sqlite3
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# ---------------------------------------------------------------
# 1. CUSTOMIZE THIS SECTION PER CLIENT
# ---------------------------------------------------------------
AGENCY_INFO = {
    "name": "Prime Estates Lahore",
    "phone": "0300-1234567",
    "areas": "DHA Lahore, Bahria Town Lahore, Johar Town, Wapda Town",
}

PROPERTIES = [
    {"title": "5 Marla House - DHA Phase 6", "price": "PKR 2.1 Crore",
     "details": "3 bed, 3 bath, corner plot, ready to move"},
    {"title": "10 Marla Plot - Bahria Town Sector C", "price": "PKR 1.8 Crore",
     "details": "Possession available, near main boulevard"},
    {"title": "1 Kanal House - DHA Phase 8", "price": "PKR 6.5 Crore",
     "details": "5 bed, modern design, basement, servant quarter"},
    {"title": "Commercial Shop - Johar Town", "price": "PKR 95 Lac",
     "details": "Prime location, ground floor, 350 sq ft"},
]

SYSTEM_PROMPT = f"""You are a friendly, helpful assistant for {AGENCY_INFO['name']},
a real estate agency operating in {AGENCY_INFO['areas']}.

Your job:
- Answer visitor questions about the properties listed below (price, size, location, availability).
- Keep answers short and conversational, like a helpful real estate agent texting a client.
- If the visitor seems interested in a property, politely ask for their NAME and PHONE NUMBER
  so an agent can follow up. Do not ask for this on the very first message.
- If a visitor gives their name and phone number, thank them and say an agent will contact them soon.
- If you don't know something specific (exact possession date, negotiation, etc.), say an agent
  will confirm that on call, and again offer to take their contact details.
- Never make up properties that are not in the list below.

Available properties:
{json.dumps(PROPERTIES, indent=2)}

Agency contact number (only share if asked): {AGENCY_INFO['phone']}
"""

# ---------------------------------------------------------------
# 2. GEMINI CLIENT (free tier - no card required)
# ---------------------------------------------------------------
# Reads your key from the GEMINI_API_KEY environment variable.
# Get a free key at: https://aistudio.google.com/apikey
# Never hardcode your real API key directly in this file.
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction=SYSTEM_PROMPT,
)

# ---------------------------------------------------------------
# 3. SIMPLE LEAD STORAGE (SQLite - no setup needed)
# ---------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(__file__), "leads.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            message TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_lead_if_present(user_message, bot_reply):
    """
    Very simple heuristic lead-capture: if the user's message looks like
    it contains a phone number, save it as a lead along with their message.
    (For a real client project, you'd usually ask the AI to extract this
    more reliably - this keeps the demo simple and dependency-free.)
    """
    import re
    phone_match = re.search(r"(03\d{2}[-\s]?\d{7}|03\d{9})", user_message)
    if phone_match:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO leads (name, phone, message, created_at) VALUES (?, ?, ?, ?)",
            ("(from chat)", phone_match.group(0), user_message, datetime.utcnow().isoformat())
        )
        conn.commit()
        conn.close()


# ---------------------------------------------------------------
# 4. ROUTES
# ---------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html", agency_name=AGENCY_INFO["name"])


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = (data.get("message") or "").strip()
    history = data.get("history") or []  # list of {role, content} from the frontend

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Gemini expects roles "user" / "model" and a "parts" list instead of "content"
    gemini_history = []
    for turn in history:
        role = "model" if turn.get("role") == "assistant" else "user"
        gemini_history.append({"role": role, "parts": [turn.get("content", "")]})

    try:
        chat_session = model.start_chat(history=gemini_history)
        response = chat_session.send_message(user_message)
        reply = response.text
    except Exception as exc:
        return jsonify({"error": f"AI request failed: {exc}"}), 500

    save_lead_if_present(user_message, reply)

    return jsonify({"reply": reply})


@app.route("/api/leads", methods=["GET"])
def view_leads():
    """Simple endpoint to see captured leads - useful when demoing to a client."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM leads ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)

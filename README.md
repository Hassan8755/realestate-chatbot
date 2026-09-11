# Real Estate FAQ Chatbot — Demo Project

Ye ek ready-to-run demo hai: Flask backend + OpenAI API + simple
chat widget. Isay aap apna pehla Fiverr/portfolio project bana
sakte hain.

## 1. Apne computer pe chalane ke liye (Local Setup)

```bash
# 1. Is folder mein jaayein
cd realestate_bot

# 2. (Recommended) virtual environment banayein
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Dependencies install karein
pip install -r requirements.txt

# 4. Apni Gemini API key set karein
export GEMINI_API_KEY="AIza...aapki-key-yahan"     # Windows: set GEMINI_API_KEY=AIza...

# 5. App run karein
python app.py
```

Ab browser mein **http://127.0.0.1:5000** kholein — chatbot ready hai.

## 2. Gemini API Key Kahan Se Milegi (FREE — koi card nahi chahiye)

1. https://aistudio.google.com/apikey pe jaayein.
2. Apne Google account se sign in karein.
3. "Create API Key" pe click karein — key turant ban jayegi, bilkul
   free, koi card ya billing zaroori nahi.
4. Key ko copy kar ke safe jagah save kar lein.

## 3. Ise Kisi Naye Client Ke Liye Customize Kaise Karein

`app.py` file kholein aur ye do cheezein badlein:

- `AGENCY_INFO` — client ki agency ka naam, phone number, areas
- `PROPERTIES` — client ki actual property listings (title, price, details)

Bas itna karne se bot us client ke business ke hisaab se jawab
dene lag jayega. Chat ka look/design badalne ke liye
`templates/index.html` mein colors/text edit kar sakte hain.

## 4. Free Deploy Kaise Karein (Demo Link Client Ko Bhejne Ke Liye)

**Render.com** (free tier available):
1. GitHub pe is code ka repo bana kar upload karein.
2. Render.com pe "New Web Service" banayein, apna GitHub repo connect karein.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app` (requirements.txt mein `gunicorn` bhi add kar lein)
4. Environment variable mein `GEMINI_API_KEY` add karein.
6. Deploy hone ke baad aapko ek live link mil jayega (jaise
   `https://your-bot.onrender.com`) — yahi link Fiverr gig ya
   client ko demo ke tor pe bhej sakte hain.

## 5. Leads Kaise Dekhein

Jab koi visitor chat mein apna phone number likhta hai, wo
automatically `leads.db` file mein save ho jata hai. Browser mein
`http://127.0.0.1:5000/api/leads` khol kar saari leads dekhi ja
sakti hain (client ko ye dikha kar proof de sakte hain ke bot
sach mein leads capture karta hai).

## 6. Agla Kadam

- Isi structure ko copy kar ke "Clinic Appointment Bot" ya
  "Coaching Center Bot" bhi bana sakte hain — bas `AGENCY_INFO`,
  `PROPERTIES` (ya jo bhi data ho), aur `SYSTEM_PROMPT` badalna hoga.
- WhatsApp pe bhi isi bot ko connect kiya ja sakta hai (Twilio ya
  WhatsApp Business API ke zariye) — ye agla upgrade hai jab
  pehla client mil jaye.

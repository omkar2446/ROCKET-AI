from flask import Flask, render_template, request, jsonify
import datetime
import wikipedia
import pytz

# Optional imports (safe on local only)
try:
    import pyjokes
except:
    pyjokes = None

app = Flask(__name__)

# ---------------- CONFIG ----------------
CREATOR_NAME = "Omkar Tambe"
IST = pytz.timezone("Asia/Kolkata")

# ----------------------------------------
def process_command(query):
    query = query.lower().strip()

    if not query:
        return {"response": "Please say something."}

    # -------- STOP / EXIT --------
    if any(word in query for word in ["stop", "exit", "offline", "goodbye"]):
        return {"response": "TERMINATE"}

    # -------- TIME & DATE (IST) --------
    now = datetime.datetime.now(IST)

    if "time" in query:
        return {
            "response": f"Sir, the time is {now.strftime('%I:%M %p')}"
        }

    if "date" in query:
        return {
            "response": f"Sir, today's date is {now.strftime('%d %B %Y')}"
        }

    # -------- GREETING --------
    if query in ["hello", "hi", "hey"]:
        return {
            "response": "Hello Sir! I am Rocket AI. How can I help you?"
        }

    # -------- GOOGLE SEARCH --------
    if "google search" in query:
        search = query.replace("google search", "").strip()
        return {
            "action": "open_url",
            "url": f"https://www.google.com/search?q={search}",
            "response": f"Searching Google for {search}"
        }

    # -------- JOKES --------
    if "joke" in query:
        if pyjokes:
            return {"response": pyjokes.get_joke()}
        return {"response": "Joke feature is unavailable."}

    # -------- MUSIC --------
    if "play" in query and "spotify" in query:
        song = query.replace("play", "").replace("spotify", "").strip()
        return {
            "action": "open_url",
            "url": f"https://open.spotify.com/search/{song}",
            "response": f"Playing {song} on Spotify"
        }

    if "play" in query:
        song = query.replace("play", "").strip()
        return {
            "action": "open_url",
            "url": f"https://www.youtube.com/results?search_query={song}",
            "response": f"Playing {song} on YouTube"
        }

    # -------- OPEN WEBSITES --------
    if "open" in query:
        sites = {
            "instagram": "https://www.instagram.com",
            "facebook": "https://www.facebook.com",
            "whatsapp": "https://web.whatsapp.com",
            "twitter": "https://twitter.com",
            "x": "https://x.com",
            "linkedin": "https://www.linkedin.com",
            "telegram": "https://web.telegram.org",
            "discord": "https://discord.com",
            "reddit": "https://www.reddit.com",
            "youtube": "https://www.youtube.com",
            "spotify": "https://open.spotify.com",
            "github": "https://github.com",
            "google": "https://www.google.com",
            "gmail": "https://mail.google.com",
            "amazon": "https://www.amazon.in",
            "flipkart": "https://www.flipkart.com",
            "netflix": "https://www.netflix.com",
        }

        for site, url in sites.items():
            if site in query:
                return {
                    "action": "open_url",
                    "url": url,
                    "response": f"Opening {site}"
                }

        return {"response": "I couldn't find that website."}

    # -------- UNIVERSAL QUESTION ANSWER --------
    try:
        answer = wikipedia.summary(query, sentences=2)
        return {"response": answer}

    except wikipedia.exceptions.DisambiguationError:
        return {"response": "Your question is too broad. Please be specific."}

    except wikipedia.exceptions.PageError:
        return {
            "action": "open_url",
            "url": f"https://www.google.com/search?q={query}",
            "response": "I couldn't find a direct answer. Opening Google for you."
        }

    except Exception:
        return {"response": "I am not able to answer that right now."}

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    query = data.get("query", "")
    return jsonify(process_command(query))

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

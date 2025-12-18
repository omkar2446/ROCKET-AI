from flask import Flask, render_template, request, jsonify
import datetime
import wikipedia
import webbrowser

# Optional imports
try:
    import pyautogui
except:
    pyautogui = None

try:
    import pyjokes
except:
    pyjokes = None

app = Flask(__name__)

# ---------------- CONFIG ----------------
CREATOR_NAME = "Omkar Tambe"

# ----------------------------------------
def process_command(query):
    query = query.lower().strip()

    if not query:
        return "Please say something."

    # -------- STOP / EXIT --------
    if any(word in query for word in ["stop", "exit", "offline", "goodbye"]):
        return "TERMINATE"

    # -------- BASIC INFO --------
    if "time" in query:
        return f"Sir, the time is {datetime.datetime.now().strftime('%I:%M %p')}"

    if "date" in query:
        return f"Sir, today's date is {datetime.datetime.now().strftime('%d %B %Y')}"

    if query in ["hello", "hi", "hey"]:
        return "Hello Sir! I am Rocket AI. How can I help you?"

    # -------- GOOGLE SEARCH --------
    if "google search" in query:
        search = query.replace("google search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search}")
        return f"Searching Google for {search}"

    # -------- JOKES --------
    if "joke" in query:
        return pyjokes.get_joke() if pyjokes else "Joke feature is unavailable."

    # -------- MUSIC --------
    if "play" in query and "spotify" in query:
        song = query.replace("play", "").replace("spotify", "").strip()
        webbrowser.open(f"https://open.spotify.com/search/{song}")
        return f"Playing {song} on Spotify"

    if "play" in query:
        song = query.replace("play", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        return f"Playing {song} on YouTube"

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
                webbrowser.open(url)
                return f"Opening {site}"

        return "I couldn't find that website."

    # -------- SYSTEM CONTROLS --------
    if "screenshot" in query:
        if pyautogui:
            pyautogui.screenshot("rocket_screenshot.png")
            return "Screenshot saved."
        return "Screenshot feature not available."

    if "volume up" in query:
        if pyautogui:
            for _ in range(5):
                pyautogui.press("volumeup")
            return "Volume increased."
        return "Volume control not available."

    if "volume down" in query:
        if pyautogui:
            for _ in range(5):
                pyautogui.press("volumedown")
            return "Volume decreased."
        return "Volume control not available."

    # -------- UNIVERSAL QUESTION ANSWER --------
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.DisambiguationError:
        return "Your question is too broad. Please be specific."
    except wikipedia.exceptions.PageError:
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return "I couldn't find a direct answer. Opening Google for you."
    except:
        return "I am not able to answer that right now."

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    query = data.get("query", "")
    response = process_command(query)
    return jsonify({"response": response})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)

import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from models.ai_models import get_all_summaries
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Access environment variables
app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
app.config['DEBUG'] = app.config['ENV'] == 'development'
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

def get_video_details(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    video_data = response.json()

    if "items" in video_data and video_data["items"]:
        snippet = video_data["items"][0]["snippet"]
        title = snippet["title"]
        channel_title = snippet["channelTitle"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return title, channel_title, video_url
    else:
        return None, None, None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        video_id = youtube_url.split("v=")[-1]

        try:
            # Get video details
            title, channel_title, video_url = get_video_details(video_id)

            # Get the transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            full_text = " ".join([item['text'] for item in transcript])

            # Get summaries from all models
            summaries = get_all_summaries(full_text)

            return render_template("index.html", title=title, channel_title=channel_title, video_url=video_url, summaries=summaries)

        except Exception as e:
            error_message = str(e)
            return render_template("index.html", error=error_message)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 5001)))

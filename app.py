from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

RESOLUTION_MAP = {
    "144p": "bestvideo[height<=144]+bestaudio/best",
    "240p": "bestvideo[height<=240]+bestaudio/best",
    "360p": "bestvideo[height<=360]+bestaudio/best",
    "480p": "bestvideo[height<=480]+bestaudio/best",
    "720p": "bestvideo[height<=720]+bestaudio/best",
    "1080p": "bestvideo[height<=1080]+bestaudio/best",
    "2k": "bestvideo[height<=1440]+bestaudio/best",
    "4k": "bestvideo[height<=2160]+bestaudio/best",
    "8k": "bestvideo[height<=4320]+bestaudio/best"
}


@app.route("/download", methods=["POST"])
def download():
    try:
        data = request.get_json(force=True)
        url = data.get("url")
        resolution = data.get("resolution", "best")

        if not url:
            return jsonify({"error": "Missing URL"}), 400

<<<<<<< HEAD
        uid = str(uuid.uuid4())
        output_template = os.path.join(DOWNLOADS_DIR, f"{uid}.%(ext)s")

        ydl_opts = {
            "format": RESOLUTION_MAP.get(resolution, "best"),
            "outtmpl": output_template,
=======
        ydl_opts = {
            "format": RESOLUTION_MAP.get(resolution, "best"),
            "outtmpl": os.path.join(
                DOWNLOADS_DIR,
                "%(title).200s_%(id)s.%(ext)s"
            ),
>>>>>>> c9f43ec (Use YouTube title as filename and fix download logic)
            "merge_output_format": "mp4",
            "noplaylist": True,
            "quiet": True,
            "restrictfilenames": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

<<<<<<< HEAD
        # Send downloaded file
        for file in os.listdir(DOWNLOADS_DIR):
            if file.startswith(uid):
                file_path = os.path.join(DOWNLOADS_DIR, file)
                return send_file(file_path, as_attachment=True)

        return jsonify({"error": "File not found after download"}), 500
=======
            # Get final merged filename
            file_path = ydl.prepare_filename(info)

            if not file_path.endswith(".mp4"):
                file_path = os.path.splitext(file_path)[0] + ".mp4"

        return send_file(file_path, as_attachment=True)
>>>>>>> c9f43ec (Use YouTube title as filename and fix download logic)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def health():
    return "Backend running 🚀"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

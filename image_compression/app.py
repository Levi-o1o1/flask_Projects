import os
from flask import Flask, render_template, request, send_file
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

QUALITY_MAP = {
    "low": 85,
    "medium": 60,
    "high": 30
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/compress", methods=["POST"])
def compress():
    file = request.files.get("image")
    level = request.form.get("level")

    if not file or level not in QUALITY_MAP:
        return "Invalid input"

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_filename = "compressed_" + file.filename.rsplit(".", 1)[0] + ".jpg"
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)

    file.save(input_path)

    # Open and compress
    img = Image.open(input_path)

    # Fix for PNG with transparency
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    quality = QUALITY_MAP[level]
    img.save(output_path, "JPEG", quality=quality, optimize=True)

    # Size calculation
    original_size = round(os.path.getsize(input_path) / 1024, 2)
    compressed_size = round(os.path.getsize(output_path) / 1024, 2)

    return render_template(
        "index.html",
        success=True,
        original=original_size,
        compressed=compressed_size,
        file=output_filename
    )


@app.route("/download/<filename>")
def download(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
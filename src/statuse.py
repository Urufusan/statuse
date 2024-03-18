from flask import Flask, request, render_template
from pysysstats import Stats

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    user_agent = request.headers.get("User-Agent", "")
    if "curl" in user_agent:
        return Stats.plaintext()
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False)

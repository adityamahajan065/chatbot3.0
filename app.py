from flask import Flask, render_template, request, jsonify
from chatbot import SmartBot

app = Flask(__name__)
bot = SmartBot()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    response = bot.handle_input(message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, url_for, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq

app = Flask(__name__)

load_dotenv()
api_key = os.getenv("API_Key_GROQ")
client = Groq(
    api_key=api_key,
)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")
        
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": question,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    answer = chat_completion.choices[0].message.content
    return jsonify({"response": answer}), 200

@app.route("/summarize", methods=["POST"])
def summarize():
    email_text = request.form.get("email")
    prompt = f"summarize the following email in 2-3 sentences: {email_text}"

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Act like an expert email assistant"
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    summary = chat_completion.choices[0].message.content
    return jsonify({"response": summary}), 200

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)

# Allow CORS for all domains & methods
CORS(app, resources={r"/chat": {"origins": "*"}}, supports_credentials=True)

# Configure Gemini API Key
GENAI_API_KEY = "AIzaSyDSKXQV3Xye-m9Wucf24y_gQk-C9iDwpK4"
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":  # Handle preflight requests
        return jsonify({"message": "CORS preflight successful"}), 200

    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "Empty message"}), 400

    response = model.generate_content(user_input)

    # Beautify the response
    formatted_response = format_response(response.text)

    return jsonify({"response": formatted_response})

def format_response(text):
    """Formats the AI response with proper paragraphs and bullet points."""
    sentences = text.split(". ")  # Split sentences
    formatted_text = "\n\n".join(["• " + sentence.strip() + "." for sentence in sentences if sentence])
    return formatted_text

if __name__ == "__main__":
    app.run(debug=True)
# Using flask backend to build a web app and connect frontend HTML/CSS to Python
# Using Google's Gemini AI to generate chatbot responses
import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv # Lets you load environment variables from the .env file
from google import genai

# Load personal key
load_dotenv(dotenv_path="sympto.env")
GEMINI_KEY = os.getenv("GOOGLE_API_KEY") 

# Creates a connetion to the AI using API key 
client = genai.Client(api_key=GEMINI_KEY)

# Create the flask app and specify folders for static files and HTML templates
app = Flask(__name__, static_folder='static', template_folder='templates')

# Route one home page
@app.route("/")
def home():
    return render_template("symptoChat.html") # Displays the html page

# Route handling chat messages from frontend
@app.route("/chat", methods=["POST"])
def chat():
    # Get user input message from the JSON sent by frontend
    user_message = request.json.get("message")
    
    # Returns this message if the user sends an empty one
    if not user_message:
        return jsonify({"reply": "Please enter a message."})

    # This tells the chatbot how to respond (tone, length, behavior)
    system_instruction = (
    "You are SymptoChat, a friendly medical assistant. "
    "Provide response in a **conversational and natural** tone. "
    "Keep your answers to **one or two short paragraphs**. "
    "Focus on being supportive and clear, without using lists or bullet points. "
    "Only give a serious medical warning if you detect 'red flag' symptoms like chest pain."
)

    try:
        # Sends the users message to the Gemini AI and generates a responds
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config={'system_instruction': system_instruction},
            contents=user_message
        )
        # Get the text reply from the model
        reply = response.text

    # Print an error message if something goes wrong
    except Exception as e:
        print(f"Error: {e}")
        reply = "Oops! Something went wrong. Please try again later."
   
    # Return the AI response back to the frontend as JSON
    return jsonify({"reply": reply})

# Run the Flask app 
if __name__ == "__main__":
    app.run(debug=True, port=5000) # Starts the server
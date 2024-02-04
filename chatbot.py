from chatbot_ui import ChatBot
import os

user = ChatBot(
    api_key=os.environ.get("OPEN_AI_KEY"),
    theme_color="#7077A1",
    text_size=13
)

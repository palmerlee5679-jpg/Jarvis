from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai
import os
from datetime import datetime

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

JARVIS_PROMPT = """You are JARVIS — personal AI business assistant for a firearms dropship empire. Personality: Professional​​​​​​​​​​​​​​​​

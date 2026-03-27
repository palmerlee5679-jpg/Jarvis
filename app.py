from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai
import os
from datetime import datetime

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

JARVIS_PROMPT = """You are JARVIS — personal AI business assistant for a firearms dropship empire. Personality: Professional but with swagger. Think Harvey Specter meets Tony Stark's JARVIS. Confident, sharp, occasionally witty. Call the owner 'Boss' sometimes. Straight to the point. Expert in: Coreware, GunBroker, RSR Group, FFL compliance, MAP pricing, distributor margins, pricing strategy, competitor analysis, product listings, order management, margin tracking, business growth."""

conversation_history = []

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history
    data = request.json
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message"}), 400
    conversation_history.append({"role": "user", "parts": [user_message]})
    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]
    try:
        chat_session = model.start_chat(history=conversation_history[:-1])
        response = chat_session.send_message(JARVIS_PROMPT + "\n\nUser: " + user_message)
        assistant_message = response.text
        conversation_history.append({"role": "model", "parts": [assistant_message]})
        return jsonify({"response": assistant_message, "timestamp": datetime.now().strftime("%I:%M %p")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/clear", methods=["POST"])
def clear():
    global conversation_history
    conversation_history = []
    return jsonify({"status": "cleared"})

@app.route("/health")
def health():
    return jsonify({"status": "Jarvis is online, Boss."})

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="JARVIS">
<title>JARVIS</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root{--bg:#080810;--surface:#0e0e1a;--card:#12121f;--border:#1c1c35;--gold:#f5c842;--gold2:#e8a020;--blue:#4f8ef7;--green:#2ecc71;--text:#d0d0e8;--dim:#555570;}
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
body{background:var(--bg);color:var(--text);font-family:'DM Mono',monospace;height:100vh;height:100dvh;display:flex;flex-direction:column;overflow:hidden;}
.header{background:var(--surface);border-bottom:1px solid var(--border);padding:12px 16px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0;}
.logo{font-family:'Bebas Neue',sans-serif;font-size:28px;letter-spacing:4px;color:var(--gold);text-shadow:0 0 20px rgba(245,200,66,0.4);}
.status{display:flex;align-items:center;gap:5px;font-size:9px;color:var(--green);letter-spacing:1px;}
.status-dot{width:6px;height:6px;background:var(--green);border-radius:50%;animation:pulse 2s infinite;}
.clear-btn{background:transparent;border:1px solid var(--border);color:var(--dim);font-family:'DM Mono',monospace;font-size:9px;padding:5px 10px;border-radius:3px;cursor:pointer;letter-spacing:1px;}
.messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px;-webkit-overflow-scrolling:touch;}
.welcome{text-align:center;padding:32px 16px;}
.welcome-title{font-family:'Bebas Neue',sans-serif;font-size:48px;letter-spacing:6px;color:var(--gold);text-shadow:0 0 30px rgba(245,200,66,0.3);margin-bottom:8px;}
.welcome-sub{font-size:10px;color:var(--dim);letter-spacing:2px;margin-bottom:24px;}
.quick-actions{display:flex;flex-direction:column;gap:8px;max-width:320px;margin:0 auto;}
.quick-btn{background:var(--card);border:1px solid var(--border);color:var(--text);font-family:'DM Mono',monospace;font-size:11px;padding:12px 16px;border-radius:4px;cursor:pointer;text-align:left;letter-spacing:0.5px;}
.message{display:flex;flex-direction:column;max-width:88%;animation:fadeIn 0.3s ease;}
.message.user{align-self:flex-end;align-items:flex-end;}
.message.jarvis{align-self:flex-start;align-items:flex-start;}
.message-label{font-size:8px;letter-spacing:2px;color:var(--dim);margin-bottom:4px;text-transform:uppercase;}
.message.jarvis .message-label{color:var(--gold2);}
.bubble{padding:12px 14px;border-radius:4px;font-size:13px;line-height:1.6;white-space:pre-wrap;word-break:break-word;}
.message.user .bubble{background:var(--blue);color:white;border-radius:4px 4px 0 4px;}
.message.jarvis .bubble{background:var(--card);border:1px solid var(--border);color:var(--text);border-radius:4px 4px 4px 0;}
.timestamp{font-size:8px;color:var(--dim);margin-top:3px;}
.typing{display:flex;align-items:center;gap:4px;padding:12px 14px;background:var(--card);border:1px solid var(--border);border-radius:4px;width:fit-content;}
.typing span{width:6px;height:6px;background:var(--gold);border-radius:50%;animation:bounce 1.2s infinite;}
.typing span:nth-child(2){animation-delay:0.2s;}
.typing span:nth-child(3){animation-delay:0.4s;}
.input-area{background:var(--surface);border-top:1px solid var(--border);padding:12px 16px;padding-bottom:max(12px,env(safe-area-inset-bottom));display:flex;gap:10px;align-items:flex-end;flex-shrink:0;}
.input-wrapper{flex:1;background:var(--card);border:1px solid var(--border);border-radius:4px;display:flex;align-items:flex-end;}
textarea{flex:1;background:transparent;border:none;color:var(--text);font-family:'DM Mono',monospace;font-size:13px;padding:10px 12px;resize:none;outline:none;max-height:100px;min-height:40px;line-height:1.5;}
textarea::placeholder{color:var(--dim);}
.send-btn{background:var(--gold);border:none;color:#000;width:42px;height:42px;border-radius:4px;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:18px;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.4;}}
@keyframes bounce{0%,60%,100%{transform:translateY(0);}30%{transform:translateY(-6px);}}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:translateY(0);}}
</style>
</head>
<body>
<div class="header">
<div style="display:flex;align-items:center;gap:10px;">
<div class="logo">JARVIS</div>
<div class="status"><div class="status-dot"></div>ONLINE</div>
</div>
<button class="clear-btn" onclick="clearChat()">CLEAR</button>
</div>
<div class="messages" id="messages">
<div class="welcome" id="welcome">
<div class="welcome-title">JARVIS</div>
<div class="welcome-sub">YOUR EMPIRE. AUTOMATED.</div>
<div class="quick-actions">
<button class="quick-btn" onclick="quickSend('What are my best margin products right now?')">📊 Best margin products</button>
<button class="quick-btn" onclick="quickSend('Write me a professional GunBroker listing for a Glock 19 Gen 5')">📝 Write a GunBroker listing</button>
<button class="quick-btn" onclick="quickSend('How should I price against competitors on GunBroker?')">💰 Pricing strategy</button>
<button class="quick-btn" onclick="quickSend('What should I focus on today to grow the business?')">👑 Daily focus</button>
</div>
</div>
</div>
<div class="input-area">
<div class="input-wrapper">
<textarea id="input" placeholder="Ask Jarvis anything..." rows="1" onkeydown="handleKey(event)" oninput="autoResize(this)"></textarea>
</div>
<button class="send-btn" id="sendBtn" onclick="sendMessage()">↑</button>
</div>
<script>
let isTyping=false;
function autoResize(el){el.style.height='auto';el.style.height=Math.min(el.scrollHeight,100)+'px';}
function handleKey(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMessage();}}
function quickSend(text){document.getElementById('input').value=text;sendMessage();}
function addMessage(role,content,time){
const welcome=document.getElementById('welcome');
if(welcome)welcome.remove();
const messages=document.getElementById('messages');
const div=document.createElement('div');
div.className=`message ${role}`;
div.innerHTML=`<div class="message-label">${role==='user'?'YOU':'JARVIS'}</div><div class="bubble">${content}</div>${time?`<div class="timestamp">${time}</div>`:''}`;
messages.appendChild(div);
messages.scrollTop=messages.scrollHeight;}
function showTyping(){const messages=document.getElementById('messages');const div=document.createElement('div');div.className='message jarvis';div.id='typing';div.innerHTML='<div class="message-label">JARVIS</div><div class="typing"><span></span><span></span><span></span></div>';messages.appendChild(div);messages.scrollTop=messages.scrollHeight;}
function removeTyping(){const t=document.getElementById('typing');if(t)t.remove();}
async function sendMessage(){
if(isTyping)return;
const input=document.getElementById('input');
const message=input.value.trim();
if(!message)return;
input.value='';input.style.height='auto';
addMessage('user',message,new Date().toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit'}));
isTyping=true;document.getElementById('sendBtn').disabled=true;showTyping();
try{
const response=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message})});
const data=await response.json();
removeTyping();
if(data.response){addMessage('jarvis',data.response,data.timestamp);}
else{addMessage('jarvis','Something went wrong. Try again, Boss.','');}
}catch(err){removeTyping();addMessage('jarvis','Connection issue. Try again.','');}
isTyping=false;document.getElementById('sendBtn').disabled=false;}
async function clearChat(){await fetch('/clear',{method:'POST'});document.getElementById('messages').innerHTML='<div class="welcome" id="welcome"><div class="welcome-title">JARVIS</div><div class="welcome-sub">YOUR EMPIRE. AUTOMATED.</div><div class="quick-actions"><button class="quick-btn" onclick="quickSend(\'What are my best margin products right now?\')">📊 Best margin products</button><button class="quick-btn" onclick="quickSend(\'Write me a professional GunBroker listing for a Glock 19 Gen 5\')">📝 Write a GunBroker listing</button><button class="quick-btn" onclick="quickSend(\'How should I price against competitors on GunBroker?\')">💰 Pricing strategy</button><button class="quick-btn" onclick="quickSend(\'What should I focus on today to grow the business?\')">👑 Daily focus</button></div></div>';}
</script>
</body>
</html>"""

if __name__=="__main__":
    app.run(host="0.0.0.0",port=3000,debug=False)

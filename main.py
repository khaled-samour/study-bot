import os
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_fake_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

server_thread = threading.Thread(target=run_fake_server, daemon=True)
server_thread.start()

from google import genai
import telebot

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = (
    "أنت 'حلبة النقاش المنطقي' (Logic and Debate Agent). شخصيتك حادة، ذكية جداً،"
    " فلسفية، وتحب تفكيك الفرضيات وتحدي الأفكار بعمق واستفزاز فكري محترم."
    " لا تعطِ إجابات جاهزة أو سطحية، بل ناقش، حُجّ، واطرح أسئلة تفكيكية"
    " تضرب في صلب الفكرة المطروحة. تحدث باللغة العامية الفلسطينية الغزاوية دائماً."
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    bot.reply_to(
        message,
        f"أهلاً بك يا {user_name} يا هندسة.\nاطرح أي فكرة، نظرية، أو معتقد، ولنرى صمود حجتك."
    )

@bot.message_handler(func=lambda message: True)
def handle_ai_debate(message):
    user_text = message.text.strip()
    bot.send_chat_action(message.chat.id, 'typing')

    max_retries = 3
    success = False
    reply_text = ""

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=f"{SYSTEM_PROMPT}\n\nالمستخدم يقول: {user_text}",
            )
            reply_text = response.text
            success = True
            
            if attempt > 0:
                reply_text = f"بتعذر على التأخير، بس حصلت بعض المشاكل وتم حلها.\n\n{reply_text}"
            
            break
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(1)

    if success:
        bot.reply_to(message, reply_text)
    else:
        try:
            error_report = f"🚨 تنبيه خطأ يا مهندس!\"
            bot.send_message(5035269101, error_report)
        except Exception as sub_e:
            print(f"Failed to send admin alert: {sub_e}")
        
        user_msg = "حصلت بعض المشاكل التقنية حاول مرة اخرى\nاذا استمرت المشكلة تواصل مع المهندس 0567322381"
        bot.reply_to(message, user_msg)

if __name__ == "__main__":
    print("البوت بذكائه الحقيقي يعمل الآن...")
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(5)
            

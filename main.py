import os
import time
from google import genai
import telebot

# 1. إعدادات التوكن والمفاتيح
TELEGRAM_TOKEN = "8866562008:AAGy4Qf8qjU36XAGoa0yg2_HWPso61JO4fA"

# (ملاحظة: يفضل لاحقاً تحط مفتاح الجيميني في الـ Environment Variables على Render للأمان،
# أو تضعه هنا مباشرة مؤقتاً للتجربة)
GEMINI_API_KEY = "AIzaSyCvokebvFGSGH4H7DCIgXumzaQX0DT6nIs"



bot = telebot.TeleBot(TELEGRAM_TOKEN)

# إعداد عميل Gemini بالنموذج الأقوى والأحدث
client = genai.Client(api_key=GEMINI_API_KEY)

# شخصية البوت (System Instructions) عشان يضل ضمن إطار "المنطق والجدل الحاد"
SYSTEM_PROMPT = (
    "أنت 'حلبة النقاش المنطقي' (Logic and Debate Agent). شخصيتك حادة، ذكية جداً،"
    " فلسفية، وتحب تفكيك الفرضيات وتحدي الأفكار بعمق واستفزاز فكري محترم."
    " لا تعطِ إجابات جاهزة أو سطحية، بل ناقش، حُجّ، واطرح أسئلة تفكيكية"
" تضرب في صلب الفكرة المطروحة. تحدث باللغة العامية الفلسطينية الغزاوية دائماً."
)


@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(
      message,
      "أهلاً بك يا هندسة في الحلبة الكبرى! "
      " اطرح أي فكرة، نظرية، أو معتقد، ولنرى صمود حجتك "
        
  )


@bot.message_handler(func=lambda message: True)
def handle_ai_debate(message):
  user_text = message.text.strip()

  # إرسال مؤشر أن البوت يكتب/يفكر
  bot.send_chat_action(message.chat.id, 'typing')

  try:
    # توليد الرد باستخدام عقل Gemini الحقيقي مع توجيه الشخصية
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"{SYSTEM_PROMPT}\n\nالمستخدم يقول: {user_text}",
    )

    reply_text = response.text
    bot.reply_to(message, reply_text)

  except Exception as e:
    print(f"Gemini API Error: {e}")
    bot.reply_to(message, f"خطأ تقني يا هندسة: {e}")
      


if __name__ == "__main__":
  print("البوت بذكائه الحقيقي يعمل الآن...")
  while True:
    try:
      bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
      print(f"Error occurred: {e}")
      time.sleep(5)
      

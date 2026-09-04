import os
import time
from google import genai
import telebot

# 1. إعدادات التوكن والمفاتيح
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")


# (ملاحظة: يفضل لاحقاً تحط مفتاح الجيميني في الـ Environment Variables على Render للأمان،
# أو تضعه هنا مباشرة مؤقتاً للتجربة)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")




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
      "\n أهلاً بك يا هندسة "
      " اطرح أي فكرة، نظرية، أو معتقد، ولنرى صمود حجتك "
        
  )


@bot.message_handler(func=lambda message: True)
def handle_ai_debate(message):
  user_text = message.text.strip()
  
  # إرسال مؤشر أن البوت يكتب/يفكر
  bot.send_chat_action(message.chat.id, 'typing')

  max_retries = 3
  success = False
  reply_text = ""

  # نظام إعادة المحاولة التلقائي (Retry Loop)
  for attempt in range(max_retries):
      try:
          response = client.models.generate_content(
              model='gemini-3.6-flash',
              contents=f"{SYSTEM_PROMPT}\n\nالمستخدم يقول: {user_text}",
          )
          reply_text = response.text
          success = True
          
          # لو نجحت المحاولة (سواء الأولى أو بعد إعادة محاولة)
          if attempt > 0:
              reply_text = f"بتعذر على التأخير، بس حصلت بعض المشاكل وتم حلها.\n\n{reply_text}"
          
          break  # اطلع من اللوب طالما ضبطت الأمور
          
      except Exception as e:
          print(f"Attempt {attempt + 1} failed: {e}")
          time.sleep(1)  # استراحة ثانية بين كل محاولة والثانية

  # إذا نجحت العملية، ابعت الرد للمستخدم
  if success:
      bot.reply_to(message, reply_text)
  
  # إذا فشلت كل المحاولات للأسف، ابعتلك تقرير ع الخاص ونبه المستخدم
  else:
      # 1. إرسال تقرير الخطأ المفصل لك شخصياً على الخاص
      try:
          error_report = f"🚨 تنبيه خطأ يا مهندس!\nفشلت كل محاولات الاتصال مع الجيميناي."
          bot.send_message(5035269101, error_report)
      except Exception as sub_e:
          print(f"Failed to send admin alert: {sub_e}")
      
      # 2. إرسال رسالة الاعتذار النهائية للمستخدم
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
        

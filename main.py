import time
import telebot

TOKEN = "8866562008:AAGy4Qf8qjU36XAGoa0yg2_HWPso61JO4fA"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(
      message,
      "أهلاً بك يا هندسة في حلبة النقاش المنطقي المطور! 🔥🧠\n\nأنا الآن مستعد"
      " لتفكيك أي فرضية تطرحها.\nجرب اطرح فكرة فلسفية، تقنية، أو مجتمعية، ودعنا"
      " نرى صمود حجتك!",
  )


@bot.message_handler(func=lambda message: True)
def handle_debate(message):
  text = message.text.strip()

  if "لماذا" in text or "ليه" in text:
    bot.reply_to(
        message,
        f"سؤالك ('{text}') يفترض أن السبب بديهي، لكن ما هو الدليل القاطع على"
        " هذه الفرضية؟ ألا ترى أن هناك زاوية أخرى لم تدركها بعد؟ 🤔",
    )
  elif "صح" in text or "خطأ" in text:
    bot.reply_to(
        message,
        f"حكمك المطلق بأن الأمر ('{text}') مثير للاهتمام يا هندسة، لكن دعني"
        " أسألك: ما هو المعيار الذي بنيت عليه هذا الحكم؟ وكيف تستقيم الأمور"
        " هكذا؟",
    )
  else:
    bot.reply_to(
        message,
        f"مغزى كلامك ('{text}') يدفعنا للتأمل بعمق.. دعنا نضع هذه الفكرة تحت"
        " المجهر: لو افترضنا عكس كلامك تماماً، كيف سيكون شكل الواقع؟",
    )


if __name__ == "__main__":
  print("بوت النقاش المطور يعمل الآن...")
  while True:
    try:
      bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
      print(f"Error occurred: {e}")
      time.sleep(5)
        

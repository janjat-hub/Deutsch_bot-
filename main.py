from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests

BOT_TOKEN = "8989298829:AAEHwDvG6Yyf12boLQ-my-Bkr3bUuIeJvYY"
GEMINI_API_KEY = "AQ.Ab8RN6IJHCWPKCLqEdlZ0PPnnArUUDVcFDaUobG9dgYZt1ViNg"

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    prompt = f"""
Kamu adalah guru bahasa Jerman.

Jika user mengirim 1 kata:
- Beri arti Indonesia
- Beri artikel jika ada
- Beri plural jika ada
- Beri 1 contoh kalimat sederhana

Jika user mengirim kalimat:
- Terjemahkan
- Koreksi grammar jika salah
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt + "\n\n" + user_text
                    }
                ]
            }
        ]
    }

    response = requests.post(url, json=data)

    result = response.json()

    answer = result["candidates"][0]["content"]["parts"][0]["text"]

    await update.message.reply_text(answer)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, chat))

app.run_polling()

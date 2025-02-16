import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

API_URL = "https://tele-social.vercel.app/down?url="
BOT_TOKEN = "7871066189:AAGXwyceZLDBpC8pjAr_P-pyBqEK_jX02ww"

def download_video(update: Update, context: CallbackContext):
    user_text = update.message.text

    if "http" not in user_text:
        update.message.reply_text("❌ වැරදි Link එකක්. කරුණාකර නිවැරදි URL එකක් එවන්න!")
        return

    update.message.reply_text("📥 Downloading... කරුණාකර රැඳී සිටින්න!")

    try:
        response = requests.get(API_URL + user_text)
        data = response.json()
        print(data)

        if data.get("status") == True and "data" in data and len(data["data"]) > 0:
            video_url = data["data"][0]["url"]
            print("🔗 API Video URL:", video_url)

            # Direct Download URL එකට Convert කරන්න
            if video_url.startswith("https://d.rapidcdn.app/d?token="):
                video_url = video_url + "&dl=1"  

            # 🔽 Video File එක Download කරලා Send කරන්න
            video_data = requests.get(video_url).content
            with open("video.mp4", "wb") as f:
                f.write(video_data)

            with open("video.mp4", "rb") as video:
                update.message.reply_video(video=video, caption="🎥 ඔබේ Video එක මෙන්න!")
        else:
            update.message.reply_text("⚠️ Video එක Download කරන්න නොහැක!")
    except Exception as e:
        update.message.reply_text(f"🚨 දෝෂයක් ඇතිවී ඇත: {str(e)}")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 හෙලෝ! මම Social Media Video Download Bot. \n📌 Instagram, TikTok, Facebook Video Links එවන්න!")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
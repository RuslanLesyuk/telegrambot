from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from gtts import gTTS
import datetime
import logging
import os
import pytz  # Додаємо модуль для роботи з часовими поясами

# Налаштування логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Токен вашого бота
TOKEN = "5785082469:AAEGvie0GTt0AhPFSZF1D_yjJ-GyEMmQYfg"

# Список працівників
workers = ["Олександр Демків", "Юрій Чирук", "Руслан Лесюк"]
current_worker_index = 0  # Індекс першого працівника

# Глобальна змінна для зберігання chat_id
chat_id = 4540389383

# Часовий пояс (заміни 'Europe/Warsaw' на потрібний)
timezone = pytz.timezone('Europe/Warsaw')

# Функція для генерації голосового повідомлення
def generate_voice_message(text):
    tts = gTTS(text=text, lang='pl')
    filename = "voice_message.ogg"
    tts.save(filename)
    return filename

# Функція, яка відправляє голосове повідомлення за розкладом
async def send_voice_message(context: CallbackContext):
    global current_worker_index, chat_id

    if chat_id is None:
        logging.warning("Chat ID не визначено.")
        return

    # Отримуємо ім'я працівника
    worker_name = workers[current_worker_index]

    # Генеруємо голосове повідомлення
    voice_file = generate_voice_message(f"Dzisiaj firmę zamyka {worker_name}.i nie miaucz, bo cię wyrzucę z pracy.")

    # Відправляємо голосове повідомлення у групу або конкретному користувачеві
    await context.bot.send_voice(chat_id=chat_id, voice=open(voice_file, 'rb'))

    # Видаляємо аудіофайл після відправки
    os.remove(voice_file)

    # Оновлюємо чергу працівників
    current_worker_index = (current_worker_index + 1) % len(workers)

# Функція для запуску бота
async def start(update: Update, context: CallbackContext):
    global chat_id
    chat_id = update.message.chat_id
    await update.message.reply_text("Бот запущений. Голосові повідомлення будуть надсилатись що п'ятниці о 9:50.")

    # Встановлюємо час відправки в обраному часовому поясі
    time_in_timezone = datetime.time(hour=9, minute=50, tzinfo=timezone)

    # Плануємо завдання на кожну п'ятницю о 9:50 за часовим поясом
    context.job_queue.run_daily(
        send_voice_message,
        time=time_in_timezone,
        days=(5,),  # 5 представляє п'ятницю
    )

# Функція для команди "pierdol"
async def pierdol(update: Update, context: CallbackContext):
    # Генеруємо голосове повідомлення з текстом "payo yayo payo yayo"
    voice_file = generate_voice_message("payo yayo payo yayo")

    # Відправляємо голосове повідомлення користувачу
    await update.message.reply_voice(voice=open(voice_file, 'rb'))

    # Видаляємо аудіофайл після відправки
    os.remove(voice_file)

def main():
    # Створюємо додаток
    application = Application.builder().token(TOKEN).build()

    # Додаємо обробник для команди /start
    application.add_handler(CommandHandler("start", start))

    # Додаємо обробник для команди /pierdol
    application.add_handler(CommandHandler("pierdol", pierdol))

    # Запускаємо бота
    application.run_polling()

if __name__ == '__main__':
    main()

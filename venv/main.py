import pandas as pd 
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import nest_asyncio
import asyncio

# Активируем nest_asyncio
nest_asyncio.apply()

# Токен вашего Telegram-бота
TOKEN = '7880573746:AAGlpWe2Qyod2aK53e88VLy9i30GA5yBI6g'

# Словарь с решениями для различных проблем
SOLUTIONS = {
    "broken_plane": "Ситуация: Сломался самолет.\n\n"
                   "Решение:\n1. Немедленно уведомите техническую службу.\n"
                   "2. Оцените масштаб повреждений.\n"
                   "3. Если требуется, обратитесь к производителю самолета за помощью.\n"
                   "4. Сообщите пассажирам о задержке рейса и предоставьте информацию о статусе ремонта.",

    "no_boarding_bridge": "Ситуация: Не приехал трап.\n\n"
                         "Решение:\n1. Проверьте местонахождение трапа.\n"
                         "2. Свяжитесь с диспетчерской службой.\n"
                         "3. Если трап недоступен, используйте мобильный трап.\n"
                         "4. Объявите пассажирам об изменении планов посадки.",

    "broken_gpu": "Ситуация: Сломался ГПУ (Ground Power Unit).\n\n"
                  "Решение:\n1. Сообщите механикам о поломке.\n"
                  "2. Используйте резервный ГПУ, если он доступен.\n"
                  "3. Если резервного ГПУ нет, подключите самолет к аэродромной сети питания.\n"
                  "4. Убедитесь, что самолет функционирует корректно после подключения.",

    "fuckup": "Ситуация: Отъебнуло всё(резервы под резервы тоже!).\n\n"
              "Решений особо нет(только молиться):\n1. Сообщите ЧВР о поломке.\n"
              "2. Получите устные пиздюли.\n"
              "3. Если резервного резерва нет, подключите самолет к своей жопе через коннектор(если коннектор отсутствует–повтори шаги 1 и 2.)\n"
              "4. Убедитесь, что самолет функционирует корректно после подключения.",

    "gelik": "Ситуация: Тебя везут на чëрном тонированном гелике выяснять почему экипаж не на борту(ГП уже на месте).\n\n"
             "Решения:\n1. Тебе пиздец.\n"
             "2. Тебе полный пиздец.\n"
             "3. Тебе настолько пиздец, что пиздец.\n"
             "4. Убедитесь, что анус функционирует корректно после подключения."
}

# Шаг 1: Чтение данных из Excel
def read_excel(file_path):
    # Читаем Excel-файл в DataFrame
    df = pd.read_excel(file_path)
    return df

# Шаг 2: Создание базы данных SQLite
def create_database(df, db_name='airplanes.db'):
    # Подключение к базе данных (если файл не существует, он будет создан)
    conn = sqlite3.connect(db_name)
    
    # Запись данных из DataFrame в таблицу SQLite
    df.to_sql('airplanes', conn, if_exists='replace', index=False)
    
    # Закрытие соединения
    conn.close()

# Шаг 3: Поиск данных в базе данных
def search_database(keyword):
    conn = sqlite3.connect('airplanes.db')
    cursor = conn.cursor()

    query = """
    SELECT * FROM airplanes
    WHERE ТИП LIKE ? OR МАССА LIKE ? OR РАСХОД LIKE ? 
    """
    cursor.execute(query, (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))

    results = cursor.fetchall()
    conn.close()
    return results

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Сломался самолет", callback_data="broken_plane")],
        [InlineKeyboardButton("Не приехал трап", callback_data="no_boarding_bridge")],
        [InlineKeyboardButton("Сломался ГПУ", callback_data="broken_gpu")],
        [InlineKeyboardButton("Полный пиздец", callback_data="fuckup")],
        [InlineKeyboardButton("Гелик", callback_data="gelik")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите проблему:", reply_markup=reply_markup)

# Обработка выбора проблемы
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Получаем выбранную проблему из callback_data
    problem = query.data

    # Отправляем решение для выбранной проблемы
    if problem in SOLUTIONS:
        await query.edit_message_text(text=SOLUTIONS[problem])
    else:
        await query.edit_message_text(text="Решение для данной проблемы не найдено.")

# Команда /search
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyword = ' '.join(context.args)  # Получаем ключевое слово из аргументов команды
    if not keyword:
        await update.message.reply_text("Пожалуйста, укажите ключевое слово для поиска.")
        return

    results = search_database(keyword)
    if results:
        response = "Результаты поиска:\n"
        for row in results:
            response += f"ТИП: {row[0]}, МАССА: {row[1]}, РАСХОД: {row[2]}\n"
    else:
        response = "По вашему запросу ничего не найдено."

    await update.message.reply_text(response)

# Главная функция для запуска бота

async def keywords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('airplanes.db')
    cursor = conn.cursor()

    # Получаем уникальные значения из каждого столбца
    cursor.execute("SELECT DISTINCT ТИП FROM airplanes")
    models = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT МАССА FROM airplanes")
    weight = [str(row[0]) for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT РАСХОД FROM airplanes")
    fuel = [str(row[0]) for row in cursor.fetchall()]

    conn.close()

    response = (
        "Доступные ключевые слова:\n"
        f"ТИПЫ ВС: {', '.join(models)}\n"
        f"МАССА ВС: {', '.join(weight)}\n"
        f"РАСХОД: {', '.join(fuel)}"
    )
    await update.message.reply_text(response)
    
async def main() -> None:
    # Создаем экземпляр Application и передаем токен бота
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(CommandHandler("keywords", keywords))
    # Запускаем бота
    await application.run_polling()

# Регистрация обработчика
    
# Инициализация базы данных при первом запуске
if __name__ == '__main__':
    # Путь к файлу Excel
    excel_file = '/Users/dariapoliakova/vs code/ттх.xlsx'
    
    # Чтение данных из Excel
    data = read_excel(excel_file)
    
    # Создание базы данных
    create_database(data)
    
    print("База данных успешно создана!")

    # Запуск бота
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
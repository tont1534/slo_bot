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
                  "3. Если резервного резерва нет, подключите самолет к своей жопе.\n"
                  "4. Убедитесь, что самолет функционирует корректно после подключения."    
}

# Функция для начала работы с ботом
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Сломался самолет", callback_data="broken_plane")],
        [InlineKeyboardButton("Не приехал трап", callback_data="no_boarding_bridge")],
        [InlineKeyboardButton("Сломался ГПУ", callback_data="broken_gpu")],
        [InlineKeyboardButton("Полный пиздец", callback_data="fuckup")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите проблему:", reply_markup=reply_markup)

# Функция для обработки выбора проблемы
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

async def main() -> None:
    # Создаем экземпляр Application и передаем токен бота
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Запускаем бота
    await application.run_polling()

if __name__ == '__main__':
    # Запускаем бота через asyncio
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
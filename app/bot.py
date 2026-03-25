import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from app.utils.config import settings
from app.utils.logger import get_logger
from app.database.manager import DatabaseManager
from app.handlers import main_menu, premium, stars, nft, payments, admin

logger = get_logger(__name__)

def create_application() -> Application:
    """Создание приложения"""
    application = Application.builder().token(settings.telegram_bot_token).build()
    
    # Инициализация БД
    db_manager = DatabaseManager(settings.database_url)
    
    # Команды
    application.add_handler(CommandHandler("start", main_menu.start_command))
    application.add_handler(CommandHandler("help", main_menu.help_command))
    application.add_handler(CommandHandler("admin", admin.admin_panel))
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(main_menu.show_main_menu, pattern="^back_main$"))
    application.add_handler(CallbackQueryHandler(premium.show_premium_menu, pattern="^category_premium$"))
    application.add_handler(CallbackQueryHandler(stars.show_stars_menu, pattern="^category_stars$"))
    application.add_handler(CallbackQueryHandler(nft.show_nft_menu, pattern="^category_nft$"))
    application.add_handler(CallbackQueryHandler(payments.process_payment, pattern="^buy_"))
    
    return application

async def main():
    """Главная функция"""
    logger.info("🚀 Starting Telegram Shop Bot...")
    
    app = create_application()
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    logger.info("✅ Bot is running...")
    # Держим бота активным
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
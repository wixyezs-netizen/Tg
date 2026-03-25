from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from app.utils.logger import get_logger
from app.database.manager import DatabaseManager
from app.languages import get_text

logger = get_logger(__name__)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать главное меню"""
    user = update.effective_user
    query = update.callback_query
    
    # Получаем пользователя из БД
    db_manager = DatabaseManager("sqlite:///shop.db")
    db_user = db_manager.get_user(user.id)
    
    if not db_user:
        db_manager.create_user(user.id, user.username, user.first_name, user.language_code)
    
    keyboard = [
        [
            InlineKeyboardButton("💎 Telegram Premium", callback_data="category_premium"),
            InlineKeyboardButton("⭐ Telegram Stars", callback_data="category_stars"),
        ],
        [InlineKeyboardButton("🖼️ NFT Collection", callback_data="category_nft")],
        [
            InlineKeyboardButton("👤 Profile", callback_data="profile"),
            InlineKeyboardButton("ℹ️ Help", callback_data="help"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.edit_message_text(
            get_text("main_menu", user.language_code),
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            get_text("main_menu", user.language_code),
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
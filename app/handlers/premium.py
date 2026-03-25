from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from app.languages import get_text

PREMIUM_ITEMS = {
    "1_month": {"price": 250, "name": "1 месяц"},
    "3_months": {"price": 750, "name": "3 месяца"},
    "6_months": {"price": 1000, "name": "6 месяцев"},
    "12_months": {"price": 2000, "name": "12 месяцев"},
}

async def show_premium_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню Telegram Premium"""
    query = update.callback_query
    user = update.effective_user
    
    keyboard = []
    for item_id, item in PREMIUM_ITEMS.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{item['name']} – {item['price']}₽",
                callback_data=f"buy_premium_{item_id}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_main")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"{get_text('premium_title', user.language_code)}\n\n{get_text('premium_desc', user.language_code)}",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
"""
PromptWriterBot — a Rytr-style AI writing assistant for Telegram.

Flow:
  /start -> pick a category -> pick a template -> enter topic/text
          -> (optionally) pick a tone -> get generated content
          -> Regenerate / New template / Done
"""

import logging
import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from ai import generate_text
from templates import CATEGORIES, TEMPLATES, TONES, templates_in_category

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
CHOOSING_TEMPLATE, ENTERING_INPUT, CHOOSING_TONE = range(3)

CB_CATEGORY_PREFIX = "cat:"
CB_TEMPLATE_PREFIX = "tpl:"
CB_TONE_PREFIX = "tone:"
CB_REGENERATE = "regen"
CB_NEW_TEMPLATE = "newtpl"
CB_DONE = "done"


def category_menu() -> InlineKeyboardMarkup:
    rows = []
    row = []
    for cat_id, label in CATEGORIES.items():
        row.append(InlineKeyboardButton(label, callback_data=f"{CB_CATEGORY_PREFIX}{cat_id}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(rows)


def template_menu(category_id: str) -> InlineKeyboardMarkup:
    rows = []
    row = []
    for tid, t in templates_in_category(category_id).items():
        row.append(InlineKeyboardButton(t["name"], callback_data=f"{CB_TEMPLATE_PREFIX}{tid}"))
        if len(row) == 1:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton("⬅️ Back to categories", callback_data="back_categories")])
    return InlineKeyboardMarkup(rows)


def tone_menu() -> InlineKeyboardMarkup:
    rows = []
    row = []
    for tone in TONES:
        row.append(InlineKeyboardButton(tone, callback_data=f"{CB_TONE_PREFIX}{tone}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(rows)


def result_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🔄 Regenerate", callback_data=CB_REGENERATE),
                InlineKeyboardButton("🆕 New template", callback_data=CB_NEW_TEMPLATE),
            ],
            [InlineKeyboardButton("✅ Done", callback_data=CB_DONE)],
        ]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        "👋 Welcome to *PromptWriterBot* — your AI writing assistant.\n\n"
        "Pick a category to get started, or use /help to see all commands.",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=category_menu(),
    )
    return CHOOSING_TEMPLATE


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "*Commands*\n"
        "/start — show the template menu\n"
        "/help — this message\n"
        "/cancel — cancel the current flow\n\n"
        "Just pick a template, tell me the topic, choose a tone (if asked), "
        "and I'll generate the content for you.",
        parse_mode=ParseMode.MARKDOWN,
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text("Cancelled. Send /start to begin again.")
    return ConversationHandler.END


async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Pick a category:", reply_markup=category_menu())
    return CHOOSING_TEMPLATE


async def category_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    category_id = query.data[len(CB_CATEGORY_PREFIX):]
    label = CATEGORIES.get(category_id, category_id)
    await query.edit_message_text(
        f"*{label}* — choose a template:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=template_menu(category_id),
    )
    return CHOOSING_TEMPLATE


async def template_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    template_id = query.data[len(CB_TEMPLATE_PREFIX):]
    template = TEMPLATES[template_id]
    context.user_data["template_id"] = template_id

    await query.edit_message_text(
        f"✍️ *{template['name']}*\n\nSend me the topic, keywords, or text to work with.",
        parse_mode=ParseMode.MARKDOWN,
    )
    return ENTERING_INPUT


async def input_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["input_text"] = update.message.text
    template = TEMPLATES[context.user_data["template_id"]]

    if template["needs_tone"]:
        await update.message.reply_text("Choose a tone:", reply_markup=tone_menu())
        return CHOOSING_TONE

    await update.message.reply_text("⏳ Generating...")
    return await _generate_and_send(update.message.reply_text, context)


async def tone_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    tone = query.data[len(CB_TONE_PREFIX):]
    context.user_data["tone"] = tone
    await query.edit_message_text(f"⏳ Generating ({tone} tone)...")
    return await _generate_and_send(query.message.reply_text, context)


async def _generate_and_send(send_fn, context: ContextTypes.DEFAULT_TYPE) -> int:
    template = TEMPLATES[context.user_data["template_id"]]
    prompt = template["prompt"].format(
        input=context.user_data["input_text"],
        tone=context.user_data.get("tone", "Neutral"),
    )
    try:
        result = await generate_text(prompt)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Generation failed")
        await send_fn(f"⚠️ Something went wrong generating your content: {exc}")
        return ConversationHandler.END

    context.user_data["last_prompt"] = prompt
    await send_fn(result, reply_markup=result_menu())
    return CHOOSING_TEMPLATE


async def regenerate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    if "template_id" not in context.user_data:
        await query.edit_message_text("Session expired, send /start to begin again.")
        return ConversationHandler.END
    await query.edit_message_text("⏳ Regenerating...")
    return await _generate_and_send(query.message.reply_text, context)


async def new_template(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.message.reply_text("Pick a category:", reply_markup=category_menu())
    return CHOOSING_TEMPLATE


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.edit_message_reply_markup(reply_markup=None)
    await query.message.reply_text("All done! Send /start any time to write more. ✨")
    return ConversationHandler.END


def build_app() -> Application:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable is not set.")

    application = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_TEMPLATE: [
                CallbackQueryHandler(category_chosen, pattern=f"^{CB_CATEGORY_PREFIX}"),
                CallbackQueryHandler(template_chosen, pattern=f"^{CB_TEMPLATE_PREFIX}"),
                CallbackQueryHandler(show_categories, pattern="^back_categories$"),
                CallbackQueryHandler(regenerate, pattern=f"^{CB_REGENERATE}$"),
                CallbackQueryHandler(new_template, pattern=f"^{CB_NEW_TEMPLATE}$"),
                CallbackQueryHandler(done, pattern=f"^{CB_DONE}$"),
            ],
            ENTERING_INPUT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, input_received),
            ],
            CHOOSING_TONE: [
                CallbackQueryHandler(tone_chosen, pattern=f"^{CB_TONE_PREFIX}"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    return application


def main() -> None:
    app = build_app()
    logger.info("PromptWriterBot starting (polling mode)...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

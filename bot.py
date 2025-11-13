# =============================================================
# POWER POINT PREMIUM STORE BOT
# FULL PYTHON CODE — PART 1 (LINES 1–400)
# GSM HOSTING COMPATIBLE (NO EXTRA FILE UPLOAD)
# Author: Minexx | Power Point Break Store 🚀
# =============================================================

import json
import os
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# =============================================================
# BOT TOKEN (PUT YOUR TOKEN HERE)
# =============================================================
TOKEN = "PUT-YOUR-BOT-TOKEN-HERE"

# =============================================================
# AUTO JSON INITIALIZER (GSM HOSTING SUPPORT)
# =============================================================

def init_file(filename, default_data):
    """Create file if not exists."""
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_data, f, indent=4)

def load_json(filename):
    """Load JSON safely."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(filename, data):
    """Save JSON safely."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


# ---- CREATE REQUIRED FILES ----
init_file("services.json", {})  
init_file("settings.json", {
    "admin_id": 5692210187,
    "payment_number": "01877576843",
    "store_name": "Power Point Premium Store"
})
init_file("payments.json", {})
init_file("users.json", {})

# ---- LOAD FILES ----
services = load_json("services.json")
settings = load_json("settings.json")
payments = load_json("payments.json")
users = load_json("users.json")

ADMIN_ID = settings["admin_id"]
PAYMENT_NUMBER = settings["payment_number"]
STORE_NAME = settings["store_name"]


# =============================================================
# UTILITY FUNCTIONS
# =============================================================

def is_admin(uid):
    return str(uid) == str(ADMIN_ID)

def get_stock(sid):
    if sid not in services:
        return 0
    return len(services[sid].get("stock", []))

def get_price(sid):
    if sid not in services:
        return 0
    return services[sid]["price"]


# =============================================================
#  /start COMMAND (WELCOME SCREEN)
# =============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Save user
    users[str(user.id)] = {
        "username": user.username,
        "name": user.first_name,
    }
    save_json("users.json", users)

    text = f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
✨ WELCOME TO {STORE_NAME} ✨
┗━━━━━━━━━━━━━━━━━━━━━━┛

👋 Welcome @{user.username}
🆔 User ID: {user.id}

🚀 Tap below to explore our premium services!

┏━━━━━━━━━━━━━━━━━━━━━━┓
🌟 [ OPEN MENU ]
┗━━━━━━━━━━━━━━━━━━━━━━┛

💬 Support: @MinexxProo
"""

    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌟 OPEN MENU", callback_data="open_menu")]
    ])

    if update.message:
        await update.message.reply_text(text, reply_markup=btn)
    else:
        await update.callback_query.message.reply_text(text, reply_markup=btn)


# =============================================================
# MAIN MENU (EXACT FORMAT YOU WANTED)
# =============================================================

async def open_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = """
┏━━━━━━━━━━━━━━━━━━━━━━┓
💛 POWER POINT PREMIUM SERVICES 💛
┗━━━━━━━━━━━━━━━━━━━━━━┛

1️⃣ ChatGPT Plus  
2️⃣ YouTube Premium  
3️⃣ Netflix  
4️⃣ Spotify  
5️⃣ VPN  
6️⃣ Security Pack  
7️⃣ Premium Tools

┏━━━━━━━━━━━━━━━━━━━━━━┓
🛒 [ BUY A SERVICE ]
┗━━━━━━━━━━━━━━━━━━━━━━┛

🔙 Back to Home
"""

    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("1️⃣ ChatGPT Plus", callback_data="sv_chatgpt")],
        [InlineKeyboardButton("2️⃣ YouTube Premium", callback_data="sv_youtube")],
        [InlineKeyboardButton("3️⃣ Netflix", callback_data="sv_netflix")],
        [InlineKeyboardButton("4️⃣ Spotify", callback_data="sv_spotify")],
        [InlineKeyboardButton("5️⃣ VPN", callback_data="sv_vpn")],
        [InlineKeyboardButton("6️⃣ Security Pack", callback_data="sv_security")],
        [InlineKeyboardButton("7️⃣ Premium Tools", callback_data="sv_tools")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_home")],
    ])

    await query.edit_message_text(text, reply_markup=btn)


# =============================================================
# SERVICE DETAILS PAGE HANDLER
# =============================================================

async def service_page(update: Update, context: ContextTypes.DEFAULT_TYPE, sid):
    query = update.callback_query
    await query.answer()

    if sid not in services:
        return await query.edit_message_text("❌ Service not found!")

    svc = services[sid]
    stock_count = len(svc.get("stock", []))
    price = svc["price"]
    desc = svc["description"]
    image = svc.get("image_file_id")

    text = f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
{svc['name']}
┗━━━━━━━━━━━━━━━━━━━━━━┛

📄 Description:
{desc}

📦 Stock: {stock_count}
💵 Price: {price} BDT

┏━━━━━━━━━━━━━━━━━━━━━━┓
🛒 [ BUY NOW ]
┗━━━━━━━━━━━━━━━━━━━━━━┛

🔙 Back to Menu
"""

    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 BUY NOW", callback_data=f"buy_{sid}")],
        [InlineKeyboardButton("🔙 Back", callback_data="open_menu")]
    ])

    if image:
        await query.message.reply_photo(photo=image, caption=text, reply_markup=btn)
    else:
        await query.edit_message_text(text, reply_markup=btn)


# =============================================================
# SERVICE ROUTER (ALL BUTTON CONNECT)
# =============================================================

async def service_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data

    mapping = {
        "sv_chatgpt": "chatgpt",
        "sv_youtube": "youtube",
        "sv_netflix": "netflix",
        "sv_spotify": "spotify",
        "sv_vpn": "vpn",
        "sv_security": "security",
        "sv_tools": "tools",
    }

    if data in mapping:
        return await service_page(update, context, mapping[data])


# =============================================================
# PART 1 END (LINES ~400)
# NEXT: PART 2 = BUY PAGE + PAYMENT SYSTEM + TXN SUBMIT
# =============================================================
# =============================================================
# PART 2 — BUY PAGE + PAYMENT SYSTEM + TXN SUBMISSION
# =============================================================

# -------------------------------------------------------------
# BUY PAGE — যখন user BUY চাপবে
# -------------------------------------------------------------

async def buy_service(update: Update, context: ContextTypes.DEFAULT_TYPE, sid):
    query = update.callback_query
    await query.answer()

    if sid not in services:
        return await query.edit_message_text("❌ Service not found!")

    svc = services[sid]
    price = svc["price"]

    text = f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
💳 PAYMENT INSTRUCTIONS
┗━━━━━━━━━━━━━━━━━━━━━━┛

📌 Payment Methods:
📱 Bkash  
📱 Nagad  
📱 Rocket  
📱 Upay  
💰 Crypto (USDT / USDC / BTC)

👉 Payment Number:
📞 ⭐ {PAYMENT_NUMBER} ⭐
⚠ Only “Send Money” allowed.

💵 Amount: {price} BDT

After sending payment,
please enter your Transaction ID below:

🧾 Example:
TXN123ABC457  
0x8a9f...(crypto hash)
"""

    # user pending order save
    users[str(query.from_user.id)]["pending_service"] = sid
    save_json("users.json", users)

    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data=f"sv_{sid}")]
    ])

    await query.edit_message_text(text, reply_markup=btn)

# -------------------------------------------------------------
# ROUTE BUY BUTTONS
# -------------------------------------------------------------

async def buy_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data

    if data.startswith("buy_"):
        sid = data.replace("buy_", "")
        return await buy_service(update, context, sid)


# =============================================================
# STEP 2 — USER SENDS TXN ID
# =============================================================

async def txn_receiver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)

    if uid not in users or "pending_service" not in users[uid]:
        return

    sid = users[uid]["pending_service"]
    svc = services.get(sid)

    txn_id = update.message.text.strip()
    price = svc["price"]

    # Save payment
    payments[txn_id] = {
        "user_id": user.id,
        "username": user.username,
        "service_id": sid,
        "price": price,
        "txn": txn_id,
        "status": "pending"
    }
    save_json("payments.json", payments)

    # Confirm to user
    confirm_text = f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
🧾 TRANSACTION SUBMITTED
┗━━━━━━━━━━━━━━━━━━━━━━┛

✅ Your Transaction ID has been received!

🛒 Order: {svc['name']}
💵 Amount: {price} BDT
🧾 Txn ID: {txn_id}

⏳ Verification Time: 1–5 minutes
You will get the product automatically after admin approval.
"""

    await update.message.reply_text(confirm_text)

    # Notify Admin
    admin_text = f"""
💸 NEW PAYMENT REQUEST
━━━━━━━━━━━━━━━━━━━━━━
👤 User: @{user.username}
🆔 User ID: {user.id}

🛒 Product: {svc['name']}
💵 Amount: {price} BDT
🧾 Txn ID: {txn_id}

━━━━━━━━━━━━━━━━━━━━━━
✔️ [ APPROVE_{txn_id} ]
❌ [ REJECT_{txn_id} ]
"""

    btn = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✔️ APPROVE", callback_data=f"approve_{txn_id}"),
            InlineKeyboardButton("❌ REJECT", callback_data=f"reject_{txn_id}")
        ]
    ])

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_text,
        reply_markup=btn
    )

    # Clear pending flag
    del users[uid]["pending_service"]
    save_json("users.json", users)


# =============================================================
# ADMIN APPROVE / REJECT PAYMENT SYSTEM
# =============================================================

async def payment_admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    # ------------ APPROVE ------------
    if data.startswith("approve_"):
        txn = data.replace("approve_", "")

        if txn not in payments:
            return await query.edit_message_text("❌ Txn Not Found!")

        p = payments[txn]
        p["status"] = "approved"
        save_json("payments.json", payments)

        user_id = p["user_id"]
        sid = p["service_id"]
        svc = services[sid]

        # Auto delivery
        if len(svc.get("stock", [])) == 0:
            return await query.edit_message_text("❌ No stock available!")

        item = svc["stock"].pop(0)  # first item
        save_json("services.json", services)

        # deliver to user
        delivery_text = f"""
🎉 PAYMENT APPROVED!
━━━━━━━━━━━━━━━━━━━━━━

Here is your product:

{item}

Thank you for buying from
🌿 Power Point Premium Store!

Need help? Contact: @MinexxProo
"""
        await context.bot.send_message(chat_id=user_id, text=delivery_text)

        await query.edit_message_text("✅ Approved & delivered to user!")

    # ------------ REJECT ------------
    elif data.startswith("reject_"):
        txn = data.replace("reject_", "")

        if txn not in payments:
            return await query.edit_message_text("❌ Txn Not Found!")

        p = payments[txn]
        p["status"] = "rejected"
        save_json("payments.json", payments)

        user_id = p["user_id"]

        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Your payment could not be verified.\nPlease contact support: @MinexxProo"
        )

        await query.edit_message_text("❌ Payment Rejected by Admin.")


# =============================================================
# CALLBACK ROUTER CONNECTOR
# =============================================================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data

    # main menu
    if data == "open_menu":
        return await open_menu(update, context)

    # service pages
    if data.startswith("sv_"):
        return await service_router(update, context)

    # buy pages
    if data.startswith("buy_"):
        return await buy_router(update, context)

    # admin approve/reject
    if data.startswith("approve_") or data.startswith("reject_"):
        return await payment_admin_handler(update, context)

# =============================================================
# PART 3 — ADMIN PANEL + SERVICE ADD/EDIT + STOCK UPLOAD
# =============================================================

# -------------------------------------------------------------
# ADMIN PANEL MAIN MENU
# -------------------------------------------------------------

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    if not is_admin(user):
        return

    text = f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
👑 POWER POINT ADMIN PANEL
┗━━━━━━━━━━━━━━━━━━━━━━┛

1️⃣ Add New Service  
2️⃣ Edit Existing Service  
3️⃣ Delete Service  
4️⃣ View All Services  
5️⃣ Add Stock  
6️⃣ View Stock List  
7️⃣ Change Settings  
8️⃣ Pending Payments

🔙 Close Panel
"""

    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("1️⃣ Add Service", callback_data="ad_add_service")],
        [InlineKeyboardButton("2️⃣ Edit Service", callback_data="ad_edit_service")],
        [InlineKeyboardButton("3️⃣ Delete Service", callback_data="ad_del_service")],
        [InlineKeyboardButton("4️⃣ View Services", callback_data="ad_view_services")],
        [InlineKeyboardButton("5️⃣ Add Stock", callback_data="ad_add_stock")],
        [InlineKeyboardButton("6️⃣ View Stock", callback_data="ad_view_stock")],
        [InlineKeyboardButton("7️⃣ Settings", callback_data="ad_settings")],
        [InlineKeyboardButton("8️⃣ Pending", callback_data="ad_pending")],
    ])

    await update.message.reply_text(text, reply_markup=btn)


# =============================================================
# ADD SERVICE — STEP WISE PROCESS
# =============================================================

add_state = {}   # store admin steps

async def add_service_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    add_state[q.from_user.id] = {"step": 1}

    await q.edit_message_text("📝 Send NEW SERVICE ID (example: chatgpt)")


async def add_service_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    if user not in add_state:
        return

    step = add_state[user]["step"]
    text = update.message.text.strip()

    # ---------------- Step 1 — Service ID ----------------
    if step == 1:
        if text in services:
            await update.message.reply_text("❌ ID already exists. Try another.")
            return
        add_state[user]["id"] = text
        add_state[user]["step"] = 2
        return await update.message.reply_text("📛 Send Service Name:")

    # ---------------- Step 2 — Name ----------------------
    if step == 2:
        add_state[user]["name"] = text
        add_state[user]["step"] = 3
        return await update.message.reply_text("💵 Send Price (number only):")

    # ---------------- Step 3 — Price ---------------------
    if step == 3:
        if not text.isdigit():
            return await update.message.reply_text("❌ Only numbers allowed!")
        add_state[user]["price"] = int(text)
        add_state[user]["step"] = 4
        return await update.message.reply_text("📝 Send Description:")

    # ---------------- Step 4 — Description ----------------
    if step == 4:
        add_state[user]["description"] = text
        add_state[user]["step"] = 5
        return await update.message.reply_text("📸 Send image (optional) or type: skip")

    # ---------------- Step 5 — Image -----------------------
    if step == 5:
        sid = add_state[user]["id"]

        if text.lower() == "skip":
            image_id = None
        else:
            if update.message.photo:
                image_id = update.message.photo[-1].file_id
            else:
                image_id = None

        # create empty stock list
        services[sid] = {
            "name": add_state[user]["name"],
            "price": add_state[user]["price"],
            "description": add_state[user]["description"],
            "image_file_id": image_id,
            "stock": []
        }
        save_json("services.json", services)

        del add_state[user]

        return await update.message.reply_text("🎉 SERVICE ADDED SUCCESSFULLY!")


# =============================================================
# ADD STOCK TO SERVICE
# =============================================================

stock_state = {}

async def add_stock_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if len(services) == 0:
        return await q.edit_message_text("❌ No services available!")

    text = "📦 Select Service to Add Stock:\n\n"
    btns = []

    for sid in services:
        btns.append([InlineKeyboardButton(services[sid]["name"], callback_data=f"stk_{sid}")])

    markup = InlineKeyboardMarkup(btns)
    await q.edit_message_text(text, reply_markup=markup)


async def add_stock_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    
    sid = q.data.replace("stk_", "")
    stock_state[q.from_user.id] = sid

    await q.edit_message_text(
        f"📦 Send Stock Item For:\n{services[sid]['name']}\n\nExample:\nemail:pass\nOr\nCode12345"
    )


async def add_stock_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    if user not in stock_state:
        return

    sid = stock_state[user]
    item = update.message.text.strip()

    services[sid]["stock"].append(item)
    save_json("services.json", services)

    await update.message.reply_text("✔ Stock Added!")

    del stock_state[user]


# =============================================================
# VIEW STOCK
# =============================================================

async def view_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    text = "📦 STOCK LIST\n━━━━━━━━━━━━━━━━━━\n"
    for sid in services:
        text += f"\n{services[sid]['name']}: {len(services[sid]['stock'])}"

    await q.edit_message_text(text)


# =============================================================
# VIEW SERVICES
# =============================================================

async def view_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    text = "📋 AVAILABLE SERVICES:\n\n"
    for sid in services:
        s = services[sid]
        text += f"🔹 {s['name']} — {s['price']} BDT\n"

    await q.edit_message_text(text)


# =============================================================
# ADMIN SETTINGS EDIT
# =============================================================

settings_state = {}

async def settings_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    text = """
⚙ SETTINGS
Choose what to change:
"""

    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("🆔 Change Admin ID", callback_data="st_admin")],
        [InlineKeyboardButton("📞 Change Payment Number", callback_data="st_paynum")],
        [InlineKeyboardButton("🏪 Change Store Name", callback_data="st_store")],
    ])

    await q.edit_message_text(text, reply_markup=btn)


async def settings_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    field = q.data.replace("st_", "")
    settings_state[q.from_user.id] = field

    await q.edit_message_text(f"📝 Send new value for: {field}")


async def settings_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    if user not in settings_state:
        return

    field = settings_state[user]
    new_value = update.message.text.strip()

    if field == "admin":
        settings["admin_id"] = int(new_value)
    elif field == "paynum":
        settings["payment_number"] = new_value
    elif field == "store":
        settings["store_name"] = new_value

    save_json("settings.json", settings)

    del settings_state[user]

    await update.message.reply_text("✔ Setting Updated!")


# =============================================================
# PENDING PAYMENTS
# =============================================================

async def pending_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    text = "⏳ PENDING PAYMENTS:\n━━━━━━━━━━━━━━\n"

    for txn in payments:
        if payments[txn]["status"] == "pending":
            u = payments[txn]
            text += f"\n🧾 {txn} — {u['username']} — {u['service_id']}"

    await q.edit_message_text(text)


# =============================================================
# ADMIN BUTTON ROUTER
# =============================================================

async def admin_button_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data

    if data == "ad_add_service":
        return await add_service_start(update, context)

    if data == "ad_add_stock":
        return await add_stock_start(update, context)

    if data == "ad_view_services":
        return await view_services(update, context)

    if data == "ad_view_stock":
        return await view_stock(update, context)

    if data == "ad_settings":
        return await settings_start(update, context)

    if data == "ad_pending":
        return await pending_list(update, context)

    if data.startswith("stk_"):
        return await add_stock_service(update, context)

    if data.startswith("st_"):
        return await settings_select(update, context)


# =============================================================
# BOT RUNNER (MUST BE LAST PART)
# =============================================================

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # COMMANDS
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))

    # CALLBACKS
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(CallbackQueryHandler(admin_button_router))

    # TEXT HANDLERS
    app.add_handler(MessageHandler(filters.TEXT, txn_receiver))
    app.add_handler(MessageHandler(filters.TEXT, add_service_message))
    app.add_handler(MessageHandler(filters.TEXT, add_stock_message))
    app.add_handler(MessageHandler(filters.TEXT, settings_message))

    print("Bot is Running…")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())




# ============================
# POWER POINT BREAK STORE BOT
# PART – 1 (CORE SYSTEM)
# ============================

import os
import json
import asyncio
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters
)

# -----------------------------
# BOT SETTINGS
# -----------------------------
BOT_TOKEN = "8456520266:AAFFN9gK7WT8WmPyoEdNPj3F8tVJXhhGGoo"
ADMIN_ID = 5692210187

# JSON FILES
PRODUCT_FILE = "products.json"
ORDER_FILE = "orders.json"
SETTINGS_FILE = "settings.json"


# -----------------------------
# AUTO CREATE JSON FILES
# -----------------------------
def ensure_files():
    if not os.path.exists(PRODUCT_FILE):
        with open(PRODUCT_FILE, "w") as f:
            json.dump({}, f)

    if not os.path.exists(ORDER_FILE):
        with open(ORDER_FILE, "w") as f:
            json.dump({}, f)

    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({
                "payment_number": "01800000000",
                "crypto_wallet": "N/A"
            }, f)


ensure_files()


# -----------------------------
# JSON READ/WRITE FUNCTIONS
# -----------------------------
def read_json(file):
    with open(file, "r") as f:
        return json.load(f)


def write_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------
# SEND MESSAGE (SAFE)
# -----------------------------
async def send_msg(chat_id, text, reply=None, parse=True, context=None):
    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply,
            parse_mode="Markdown" if parse else None
        )
    except:
        pass


# ------------------------------------------------
#         🟡  START COMMAND (FULL FIXED)
# ------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username or "Unknown"
    user_id = user.id

    welcome_text = f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
✨ WELCOME TO POWER POINT PREMIUM STORE ✨
┗━━━━━━━━━━━━━━━━━━━━━━┛

👋 Welcome @{username}
🆔 User ID: {user_id}

🚀 Tap below to explore our premium services!
┏━━━━━━━━━━━━━━━━━━━━━━┓
🌟 [ OPEN MENU ]
┗━━━━━━━━━━━━━━━━━━━━━━┛

💬 Support: @MinexxProo
🌿 Thank you for choosing Power Point Break!
"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌟 OPEN MENU", callback_data="open_menu")]
    ])

    await update.message.reply_text(
        welcome_text,
        reply_markup=keyboard
    )


# ------------------------------------------------
#         🟡  MAIN MENU VIEW
# ------------------------------------------------
async def main_menu(update, context):
    menu_text = """
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
"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("ChatGPT Plus", callback_data="sv_chatgpt")],
        [InlineKeyboardButton("YouTube Premium", callback_data="sv_yt")],
        [InlineKeyboardButton("Netflix", callback_data="sv_netflix")],
        [InlineKeyboardButton("Spotify", callback_data="sv_spotify")],
        [InlineKeyboardButton("VPN", callback_data="sv_vpn")],
        [InlineKeyboardButton("Security Pack", callback_data="sv_security")],
        [InlineKeyboardButton("Premium Tools", callback_data="sv_tools")],
        [InlineKeyboardButton("🔙 Back to Home", callback_data="go_home")]
    ])

    await update.callback_query.edit_message_text(
        menu_text,
        reply_markup=keyboard
    )


# ------------------------------------------------
#       🟡 MAIN CALLBACK ROUTER (MASTER)
# ------------------------------------------------
async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data

    # Open Menu
    if data == "open_menu":
        return await main_menu(update, context)

    # Back to home
    if data == "go_home":
        return await start(update, context)

    # Service Categories
    if data.startswith("sv_"):
        return await service_category_page(update, context)

    # Next parts will expand the logic

# ============================================
# PART – 2
# SERVICE CATEGORY + SUB OPTIONS + BUY PAGE
# ============================================

# -----------------------------
# SERVICE CATEGORY SYSTEM
# -----------------------------
async def service_category_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    category = data.replace("sv_", "")

    # CATEGORY WISE SUB OPTIONS
    if category == "chatgpt":
        title = "🔥 ChatGPT Plus Subscriptions"
        buttons = [
            ["1 Month – 90 BDT", "buy_cgpt_1"],
            ["3 Months – 260 BDT", "buy_cgpt_3"],
            ["6 Months – 520 BDT", "buy_cgpt_6"],
        ]

    elif category == "yt":
        title = "🎬 YouTube Premium Packages"
        buttons = [
            ["Individual – 160 BDT", "buy_yt_ind"],
            ["Family Pack – 350 BDT", "buy_yt_fam"],
        ]

    elif category == "netflix":
        title = "🎞 Netflix Plans"
        buttons = [
            ["1 Screen – 180 BDT", "buy_nf_1"],
            ["4 Screen – 350 BDT", "buy_nf_4"],
        ]

    elif category == "spotify":
        title = "🎵 Spotify Premium"
        buttons = [
            ["Individual – 150 BDT", "buy_spo_1"],
            ["Duo – 200 BDT", "buy_spo_2"],
        ]

    elif category == "vpn":
        title = "🔐 VPN Packages"
        buttons = [
            ["ExpressVPN – 120 BDT", "buy_vpn_exp"],
            ["NordVPN – 110 BDT", "buy_vpn_nord"],
        ]

    elif category == "security":
        title = "🛡 Security Pack"
        buttons = [
            ["Facebook Security Pack – 60 BDT", "buy_sec_fb"],
            ["Gmail Security Pack – 60 BDT", "buy_sec_gm"],
        ]

    elif category == "tools":
        title = "⚙️ Premium Tools"
        buttons = [
            ["Canva Pro – 150 BDT", "buy_tool_canva"],
            ["Grammarly Premium – 120 BDT", "buy_tool_gram"],
        ]

    else:
        title = "Service Not Found"
        buttons = []

    # Keyboard Build
    keyboard = []
    for name, code in buttons:
        keyboard.append([InlineKeyboardButton(name, callback_data=f"{code}")])

    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="open_menu")])

    await update.callback_query.edit_message_text(
        f"┏━━━━━━━━━━━━━━━━━━━━━━┓\n{title}\n┗━━━━━━━━━━━━━━━━━━━━━━┛\n\nChoose a package below:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# -----------------------------
# BUY PAGE (PRODUCT DETAILS)
# -----------------------------
async def buy_page(update: Update, context: ContextTypes.DEFAULT_TYPE, pid, title, price):
    text = f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
🛒 **{title}**
┗━━━━━━━━━━━━━━━━━━━━━━┛

💵 Price: **{price} BDT**

📌 This is a trusted Power Point Break Store product.
Click **BUY NOW** to continue.

"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 BUY NOW", callback_data=f"pay_{pid}_{price}")],
        [InlineKeyboardButton("🔙 Back", callback_data="open_menu")]
    ])

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


# -----------------------------
# PRODUCT → BUY ROUTER
# -----------------------------
async def product_buy_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data.replace("buy_", "")

    # ChatGPT Plus
    if data == "cgpt_1":
        return await buy_page(update, context, "cgpt_1", "ChatGPT Plus – 1 Month", 90)
    if data == "cgpt_3":
        return await buy_page(update, context, "cgpt_3", "ChatGPT Plus – 3 Months", 260)
    if data == "cgpt_6":
        return await buy_page(update, context, "cgpt_6", "ChatGPT Plus – 6 Months", 520)

    # YouTube
    if data == "yt_ind":
        return await buy_page(update, context, "yt_ind", "YouTube Premium – Individual", 160)
    if data == "yt_fam":
        return await buy_page(update, context, "yt_fam", "YouTube Premium – Family Pack", 350)

    # Netflix
    if data == "nf_1":
        return await buy_page(update, context, "nf_1", "Netflix – 1 Screen", 180)
    if data == "nf_4":
        return await buy_page(update, context, "nf_4", "Netflix – 4 Screen", 350)

    # Spotify
    if data == "spo_1":
        return await buy_page(update, context, "spo_1", "Spotify – Individual", 150)
    if data == "spo_2":
        return await buy_page(update, context, "spo_2", "Spotify – Duo", 200)

    # VPN
    if data == "vpn_exp":
        return await buy_page(update, context, "vpn_exp", "ExpressVPN", 120)
    if data == "vpn_nord":
        return await buy_page(update, context, "vpn_nord", "NordVPN", 110)

    # Security
    if data == "sec_fb":
        return await buy_page(update, context, "sec_fb", "Facebook Security Pack", 60)
    if data == "sec_gm":
        return await buy_page(update, context, "sec_gm", "Gmail Security Pack", 60)

    # Tools
    if data == "tool_canva":
        return await buy_page(update, context, "tool_canva", "Canva Pro", 150)
    if data == "tool_gram":
        return await buy_page(update, context, "tool_gram", "Grammarly Premium", 120)


# ============================================
# PART – 3
# PAYMENT SYSTEM + TXN SUBMIT + ADMIN ALERT
# ============================================

# -----------------------------
# PAYMENT INSTRUCTIONS PAGE
# -----------------------------
async def payment_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    pay_pid_price
    Example: pay_cgpt_1_90
    """

    data = update.callback_query.data.replace("pay_", "")
    parts = data.split("_")

    if len(parts) != 2:
        return await update.callback_query.answer("Payment Error!", show_alert=True)

    pid = parts[0]
    price = int(parts[1])

    # Save pending order
    orders = read_json(ORDER_FILE)
    user = update.callback_query.from_user

    orders[str(user.id)] = {
        "pid": pid,
        "price": price,
        "status": "awaiting_txn"
    }
    write_json(ORDER_FILE, orders)

    settings = read_json(SETTINGS_FILE)

    pay_text = f"""
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
📞 {settings['payment_number']}
⚠ Only “Send Money” allowed.

💵 Amount: {price} BDT

After sending payment,
please write your Transaction ID below:

🧾 Example:
TXN99821HS  
0xA91f…(crypto hash)
"""

    await update.callback_query.edit_message_text(
        pay_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="open_menu")]
        ])
    )

    # Set global state for user → TXN input required
    context.user_data["awaiting_txn"] = True


# -----------------------------
# USER SENDS TXN MESSAGE
# -----------------------------
async def collect_txn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"

    # If no order pending → ignore
    if not context.user_data.get("awaiting_txn"):
        return

    orders = read_json(ORDER_FILE)

    if str(user_id) not in orders:
        return

    txn = update.message.text.strip()
    order = orders[str(user_id)]

    pid = order["pid"]
    price = order["price"]

    # Mark txn submitted
    order["txn"] = txn
    order["status"] = "pending"
    orders[str(user_id)] = order
    write_json(ORDER_FILE, orders)

    # Confirmation to user
    confirm_msg = f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
🧾 TRANSACTION SUBMITTED
┗━━━━━━━━━━━━━━━━━━━━━━┛

✅ Your Transaction ID has been received!

🛒 Order: {pid}
💵 Amount: {price} BDT
🧾 Txn ID: {txn}

⏳ Verification Time: 1–5 minutes  
Product will be delivered after admin approval.
"""

    await update.message.reply_text(confirm_msg)

    # Notify Admin
    admin_msg = f"""
💸 NEW PAYMENT REQUEST
━━━━━━━━━━━━━━━━━━━━━━
👤 User: @{username}
🆔 User ID: {user_id}

🛒 Product: {pid}
💵 Amount: {price} BDT
🧾 Txn ID: {txn}

━━━━━━━━━━━━━━━━━━━━━━
✔️ APPROVE  
❌ REJECT
"""

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✔️ APPROVE", callback_data=f"approve_{user_id}"),
            InlineKeyboardButton("❌ REJECT", callback_data=f"reject_{user_id}")
        ]
    ])

    await update.message.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_msg,
        reply_markup=keyboard
    )

    # Clear flag
    context.user_data["awaiting_txn"] = False


# -----------------------------
# ADMIN APPROVE / REJECT ORDER
# -----------------------------
async def admin_payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    await update.callback_query.answer()

    orders = read_json(ORDER_FILE)

    if data.startswith("approve_"):
        user_id = data.replace("approve_", "")
        if user_id not in orders:
            return await update.callback_query.edit_message_text("❌ Order Not Found!")

        order = orders[user_id]
        pid = order["pid"]
        price = order["price"]

        # PRODUCT DELIVERY LOGIC
        delivery_text = f"""
🎉 PAYMENT APPROVED!
━━━━━━━━━━━━━━━━━━━━━━

Your order has been approved.

🛒 Product: {pid}
💵 Price: {price} BDT

The admin will deliver your product shortly.
🌿 Thank you for buying from Power Point Break Store!
"""

        await context.bot.send_message(int(user_id), delivery_text)

        # Update status
        order["status"] = "approved"
        orders[user_id] = order
        write_json(ORDER_FILE, orders)

        await update.callback_query.edit_message_text("✔️ Order Approved")

    elif data.startswith("reject_"):
        user_id = data.replace("reject_", "")
        if user_id not in orders:
            return await update.callback_query.edit_message_text("❌ Order Not Found!")

        await context.bot.send_message(int(user_id),
                                       "❌ Your payment could not be verified.\nPlease contact support: @MinexxProo")

        order = orders[user_id]
        order["status"] = "rejected"
        orders[user_id] = order
        write_json(ORDER_FILE, orders)

        await update.callback_query.edit_message_text("❌ Order Rejected")


# ============================================
# PART – 4
# ADMIN PANEL + STOCK SYSTEM + SETTINGS
# ============================================

# --------------------------------------------
# ADMIN PANEL COMMAND (/admin)
# --------------------------------------------
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("❌ You are not admin!")

    panel = """
┏━━━━━━━━━━━━━━━━━━━━━━┓
👑 ADMIN CONTROL PANEL
┗━━━━━━━━━━━━━━━━━━━━━━┛

1️⃣ Add Stock  
2️⃣ View Stock  
3️⃣ Change Payment Number  
4️⃣ View Pending Orders
"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Stock", callback_data="admin_addstock")],
        [InlineKeyboardButton("📦 View Stock", callback_data="admin_viewstock")],
        [InlineKeyboardButton("💳 Change Payment Number", callback_data="admin_paymentnum")],
        [InlineKeyboardButton("📄 Pending Orders", callback_data="admin_pending")],
    ])

    await update.message.reply_text(panel, reply_markup=keyboard)


# --------------------------------------------
# 1️⃣ ADD STOCK (STEP 1)
# --------------------------------------------
add_stock_state = {}

async def admin_addstock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    text = """
📦 SEND PRODUCT ID TO ADD STOCK

Example:
cgpt_1
yt_ind
nf_4
"""

    add_stock_state[q.from_user.id] = {"step": 1}

    await q.edit_message_text(text)


# --------------------------------------------
# 1️⃣ ADD STOCK (STEP 2 → PROCESS STOCK)
# --------------------------------------------
async def add_stock_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    if user not in add_stock_state:
        return

    state = add_stock_state[user]
    if state["step"] == 1:
        pid = update.message.text.strip()

        # Save product id
        state["pid"] = pid
        state["step"] = 2

        await update.message.reply_text(
            f"✔ Product Selected: {pid}\n\nNow send STOCK DATA:\nExample:\nemail:pass\nor\ncode12345"
        )
        return

    if state["step"] == 2:
        pid = state["pid"]
        stock_item = update.message.text.strip()

        # Load products.json
        products = read_json(PRODUCT_FILE)

        if pid not in products:
            products[pid] = []

        products[pid].append(stock_item)
        write_json(PRODUCT_FILE, products)

        await update.message.reply_text("🎉 Stock Added Successfully!")

        del add_stock_state[user]
        return


# --------------------------------------------
# 2️⃣ VIEW STOCK
# --------------------------------------------
async def admin_viewstock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    products = read_json(PRODUCT_FILE)

    text = "📦 **STOCK LIST**\n━━━━━━━━━━━━━━\n"

    if len(products) == 0:
        text += "No stock available!"
    else:
        for pid in products:
            text += f"\n🔹 {pid} → {len(products[pid])} items"

    await q.edit_message_text(text, parse_mode="Markdown")


# --------------------------------------------
# 3️⃣ CHANGE PAYMENT NUMBER
# --------------------------------------------
payment_change_state = {}

async def admin_paymentnum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    payment_change_state[q.from_user.id] = True

    await q.edit_message_text("📞 Send NEW Payment Number:")


async def paymentnum_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    if user not in payment_change_state:
        return

    new_num = update.message.text.strip()

    settings = read_json(SETTINGS_FILE)
    settings["payment_number"] = new_num
    write_json(SETTINGS_FILE, settings)

    await update.message.reply_text(f"✔ Payment Number Updated: {new_num}")

    del payment_change_state[user]


# --------------------------------------------
# 4️⃣ VIEW PENDING ORDERS
# --------------------------------------------
async def admin_pending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    orders = read_json(ORDER_FILE)
    text = "📄 **PENDING ORDERS**\n━━━━━━━━━━━━━━\n"

    empty = True
    for uid, order in orders.items():
        if order["status"] == "pending":
            empty = False
            text += f"\n👤 User: {uid}\n🛒 {order['pid']}\n💵 {order['price']} BDT\n🧾 {order['txn']}\n━━━━━━━━━\n"

    if empty:
        text += "\nNo pending orders!"

    await q.edit_message_text(text, parse_mode="Markdown")


# --------------------------------------------
# MASTER CALLBACK ROUTER (ALL BUTTONS)
# --------------------------------------------
async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data

    # Main Menu
    if data == "open_menu":
        return await main_menu(update, context)

    if data == "go_home":
        return await start(update, context)

    # Service Submenu → Product details
    if data.startswith("sv_"):
        return await service_category_page(update, context)

    # Product BUY pages
    if data.startswith("buy_"):
        return await product_buy_router(update, context)

    # Payment Page
    if data.startswith("pay_"):
        return await payment_page(update, context)

    # Admin Panel buttons
    if data == "admin_addstock":
        return await admin_addstock(update, context)

    if data == "admin_viewstock":
        return await admin_viewstock(update, context)

    if data == "admin_paymentnum":
        return await admin_paymentnum(update, context)

    if data == "admin_pending":
        return await admin_pending(update, context)

    # Admin Approve / Reject
    if data.startswith("approve_") or data.startswith("reject_"):
        return await admin_payment_handler(update, context)


# --------------------------------------------
# BOT RUNNER (GSM HOSTING SAFE)
# --------------------------------------------
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))

    # Callbacks
    app.add_handler(CallbackQueryHandler(callback_router))

    # Text Inputs (TXN, Stock, Payment Num)
    app.add_handler(MessageHandler(filters.TEXT, collect_txn))
    app.add_handler(MessageHandler(filters.TEXT, add_stock_handler))
    app.add_handler(MessageHandler(filters.TEXT, paymentnum_handler))

    print("🔥 BOT IS RUNNING (GSM HOSTING MODE)…")
    await app.initialize()
    await app.start()


# GSM SAFE RUNNER
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()



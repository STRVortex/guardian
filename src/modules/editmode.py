from pymongo import MongoClient
from config import MONGO_DB_URI, BOT_OWNER_ID
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from src import app

# Initialize MongoDB connection
DATABASE = MongoClient(MONGO_DB_URI)
DB = DATABASE["MAIN"]
EDIT_ENABLED = DB["delenable"]
AUTH_USERS = DB["auth_users"]

async def get_group_admins(chat_id):
    admins = []
    async for member in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        admins.append(member.user.id)
    return admins

def is_edit_mode_enabled(group_id: int):
    return EDIT_ENABLED.find_one({"group_id": group_id}) is not None

def toggle_edit_mode(group_id: int, enable: bool):
    if enable:
        EDIT_ENABLED.update_one({"group_id": group_id}, {"$set": {"enabled": True}}, upsert=True)
    else:
        EDIT_ENABLED.delete_one({"group_id": group_id})

def is_user_authorized(user_id: int, chat_id: int):
    return AUTH_USERS.find_one({"user_id": user_id, "chat_id": chat_id}) is not None

def toggle_user_auth(user_id: int, chat_id: int, authorize: bool):
    if authorize:
        AUTH_USERS.update_one({"user_id": user_id, "chat_id": chat_id}, {"$set": {"authorized": True}}, upsert=True)
    else:
        AUTH_USERS.delete_one({"user_id": user_id, "chat_id": chat_id})

@app.on_message(filters.command("editmode"))
async def editmode_command(_, message):
    if message.chat.type not in ["group", "supergroup"]:
        return await message.reply("This command can only be used in groups.")

    admins = await get_group_admins(message.chat.id)
    if message.from_user.id not in admins:
        return await message.reply("You must be an admin to use this command.")

    if len(message.command) != 2 or message.command[1] not in ["on", "off"]:
        return await message.reply("Usage: /editmode on/off")

    enable = message.command[1] == "on"
    toggle_edit_mode(message.chat.id, enable)
    status = "enabled" if enable else "disabled"
    await message.reply(f"Edit mode has been {status}.")

@app.on_message(filters.command(["auth", "unauth"]))
async def auth_command(_, message):
    if message.chat.type not in ["group", "supergroup"]:
        return await message.reply("This command can only be used in groups.")

    admins = await get_group_admins(message.chat.id)
    if message.from_user.id not in admins and message.from_user.id != BOT_OWNER_ID:
        return await message.reply("Only group admins and bot owner can use this command.")

    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply("Reply to a user's message to authorize or unauthorize them.")

    target_user = message.reply_to_message.from_user
    authorize = message.command[0].lower() == "auth"
    toggle_user_auth(target_user.id, message.chat.id, authorize)

    action = "authorized" if authorize else "unauthorized"
    await message.reply(f"{target_user.mention} has been {action}.")

@app.on_edited_message(filters.text & filters.group)
async def handle_edited_message(_, message):
    if not is_edit_mode_enabled(message.chat.id):
        return

    admins = await get_group_admins(message.chat.id)
    if message.from_user.id in admins or is_user_authorized(message.from_user.id, message.chat.id):
        return

    await message.reply(f"{message.from_user.mention} edited a message, so I deleted it.")
    await message.delete()

# Add this to your main.py or wherever you initialize your bot
app.add_handler(filters.command("editmode"), editmode_command)
app.add_handler(filters.command(["auth", "unauth"]), auth_command)
app.add_handler(filters.edited_message & filters.text & filters.group, handle_edited_message)

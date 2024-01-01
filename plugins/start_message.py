import config
import asyncio

from bot import Bot

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant

from save_data import getUser, addUser, getAlluser, delUser

@Bot.on_message(filters.command("start") & filters.private)
async def start_msg(bot: Client, msg: Message):
    subs = await subschannel(bot, msg)
    if (not subs):
        await subschannel_msg(bot, msg)
        return
    user = await getUser(msg.from_user.id)
    if (not user):
        await addUser(msg.from_user.id)
    await msg.reply(f"Hello {msg.from_user.first_name}\n\nDOOD Downloader merupakan bot pengunduh di telegram yang mendukung URL/Tautan Doodstream dalam bentuk media tanpa Ads/Iklan.\n\nKetik /help untuk melihat perintah bot yang tersedia")

@Bot.on_message(filters.command("help") & filters.private)
async def help_msg(bot: Client, msg: Message):
    if msg.from_user.id != config.OWNER_ID:
        await msg.reply("📋 Perintah Yang Tersedia 📋\n\n/start - Memulai bot\n/help - Menampilkan Pesan Ini\n/download [url dood] - Mendownload Video DoodStream\n/folder [url folder] - Menampilkan Semua Link Video Di Dalam Folder DoodStream")
    else:
        await msg.reply("📋 Perintah Yang Tersedia 📋\n\n/start - Memulai bot\n/help - Menampilkan Pesan Ini\n/download [url dood] - Mendownload Video DoodStream\n/folder [url folder] - Menampilkan Semua Link Video Di Dalam Folder DoodStream\n/broadcast - mengirim pesan kesemua user\n/user - melihat jumlah user")

@Bot.on_message(filters.command('user') & filters.private)
async def users_msg(bot: Client, msg: Message):
    if msg.from_user.id != config.OWNER_ID:
        return
    users = await getAlluser()
    await msg.reply(f"{len(users)} <b>pengguna menggunakan bot ini</b>")

@Bot.on_message(filters.command('broadcast') & filters.private)
async def broadcast_msg(bot: Client, msg: Message):
    if msg.from_user.id != config.OWNER_ID:
        return
    if (not msg.reply_to_message):
        await msg.reply("Untuk melakukan broadcast, silahkan reply sebuah pesan!")
        return
    users = await getAlluser()
    broadcast_msg = msg.reply_to_message
    total = 0
    successful = 0
    blocked = 0
    deleted = 0
    unsuccessful = 0
    
    pls_wait = await msg.reply("<code>Broadcasting Message Tunggu Sebentar...</code>")
    for chat_id in users:
        try:
            await broadcast_msg.copy(chat_id)
            successful += 1
        except FloodWait as e:
            try:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except:
                unsuccessful += 1
        except UserIsBlocked:
            await delUser(chat_id)
            blocked += 1
        except InputUserDeactivated:
            await delUser(chat_id)
            deleted += 1
        except:
            unsuccessful += 1
            pass
        total += 1
    
    status = f"""<b><u>Broadcast Completed</u>

Jumlah pengguna\t: <code>{total}</code>
Berhasil\t: <code>{successful}</code>
Pengguna diblokir\t: <code>{blocked}</code>
Akun Terhapus\t: <code>{deleted}</code>
Gagal\t: <code>{unsuccessful}</code></b>"""
        
    return await pls_wait.edit(status)

async def subschannel_msg(client: Client, msg: Message):
    url = await client.export_chat_invite_link(config.CHANNEL_ID)
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Join Channel", url=url)],
        [InlineKeyboardButton("Try Again", url=f"https://t.me/{client.botUsername}?start={msg.command[0]}")],
        [InlineKeyboardButton("Owner", user_id=config.OWNER_ID)],
    ])
    message = f"<b>Anda harus bergabung kechannel kami agar bisa menggunakan bot ini.\n\n</b><b>🔗 Link Channel 🔗</b>\n<code>{url}</code>"
    await msg.reply(message, quote=True, reply_markup=markup)

async def subschannel(client, msg):
    if not config.CHANNEL_ID:
        return True
    user_id = msg.from_user.id
    if user_id == config.OWNER_ID:
        return True
    try:
        member = await client.get_chat_member(chat_id=config.CHANNEL_ID, user_id=user_id)
    except UserNotParticipant:
        return False

    return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]
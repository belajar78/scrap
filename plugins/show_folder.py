from bot import Bot

from pyrogram import Client, filters, types
from pyrogram.errors import FloodWait
from plugins import (
    getFolderDoodStream, 
    getFolderPoopHD, 
    getDetailsDoodStreamDownload, 
    downloadVideosDoodStream, 
    progress_for_pyrogram, 
    convert_to_seconds,
    subschannel,
    subschannel_msg
)

from save_data import getFiles, addFile

import time, config, os, asyncio

@Bot.on_message(filters.command("folder") & filters.private)
async def show_folder_msg(bot: Client, msg: types.Message):
    subs = await subschannel(bot, msg)
    if (not subs):
        await subschannel_msg(bot, msg)
        return
    if (len(msg.command) == 1):
        await msg.reply("Untuk Melihat Semua Link Video Dalam Folder, Silahkan Masukkan URL Folder DoodStream\n\nContoh:\n<pre>/folder https://doodstream.com/f/xxxxxxxx</pre>")
        return
    url = msg.text.split(None, 1)[1]
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    
    data = await getFolderDoodStream(url)
    if (data[0]):
        pesan = f"<b>📁 Video List 📁</b>\n\n📂 Folder Name: {data[0]}"
        number = 1
        for video in data[1]:
            pesan += f"\n\n<b>{number}. {video['name']}</b>\n\tSize: {video['size']}\n\tDuration: {video['duration']}\n\tDate: {video['date']}\n🔗URL: {video['link']}"
            number += 1
        if (len(pesan) > 4096):
            total_text = int(len(pesan) / 4096)
            total_text = total_text + 1
            for i in range(total_text):
                try:
                    await(msg.reply(pesan[i*4096:(i+1)*4096]))
                except FloodWait as e:
                    try:
                        await asyncio.sleep(e.x)
                        await(msg.reply(pesan[i*4096:(i+1)*4096]))
                    except:
                        pass
            return
        await msg.reply(pesan)
        return
    data = await getFolderPoopHD(url)
    if (data[0]):
        pesan = f"<b>📁 Video List 📁</b>\n\n📂 Folder:\n<b>{data[0]}</b>"
        number = 1
        for video in data[1]:
            pesan += f"\n\n<b>{number}. {video['name']}</b>\n\t\t🔗URL: {video['link']}"
            number += 1
        if (len(pesan) > 4096):
            total_text = int(len(pesan) / 4096)
            total_text = total_text + 1
            for i in range(total_text):
                try:
                    await(msg.reply(pesan[i*4096:(i+1)*4096]))
                except FloodWait as e:
                    try:
                        await asyncio.sleep(e.x)
                        await(msg.reply(pesan[i*4096:(i+1)*4096]))
                    except:
                        pass
            return
        await msg.reply(pesan)
        return
    else:
        await msg.reply(data[1])

@Bot.on_message(filters.command("download") & filters.private)
async def video_msg(bot: Client, msg: types.Message):
    subs = await subschannel(bot, msg)
    if (not subs):
        await subschannel_msg(bot, msg)
        return
    if (len(msg.command) == 1):
        await msg.reply("Untuk Mendownload Video, Silahkan Masukkan URL DoodStream\n\nContoh :\n<pre>/download https://doodstream.com/d/xxxxxxxx</pre>")
        return
    url = msg.text.split(None, 1)[1]
    msg_notifikasi = f"<b>💾 DOODStream Downloader 💾</b>\n\n🔗 URL : {url}"
    start_message = await msg.reply(msg_notifikasi)
    data = await getFiles(url)
    if (data):
        msg_notifikasi = msg_notifikasi + f"\n\n<b>📁 Video Details 📁</b>\n• Name: {data['name']}\n• Size: {data['size']}\n• Duration: {data['duration']}\n• Date: {data['date']}\n{'━'*25}"

        message = await start_message.edit(msg_notifikasi)

        await bot.copy_message(msg.from_user.id, config.CHANNEL_DATABASE, data['video'], caption=f"( {data['name']} ) By @{bot.botUsername}", reply_to_message_id=msg.id)
        
        await start_message.edit(f"{msg_notifikasi}\n<b>✅ Video Telah Diupload ✅</b>")
        return
    data = await getDetailsDoodStreamDownload(url)

    if (data[0]):
        msg_notifikasi = msg_notifikasi + f"\n\n<b>📁 Video Details 📁</b>\n• Name: {data[1]['name']}\n• Size: {data[1]['size']}\n• Duration: {data[1]['duration']}\n• Date: {data[1]['date']}\n{'━'*25}"

        message = await start_message.edit(msg_notifikasi)
        
        msg_notifikasi_1 = msg_notifikasi + "\n<b>👉 Sedang mendownload</b>"
        if (not data[1]['url']):
            await message.edit(msg_notifikasi + "\n<b>URL tidak ditemukan</b>")
            return
        vid = await downloadVideosDoodStream(data[1]['url'], message, f"{data[1]['name']}_{msg.from_user.id}_{msg.id}.mp4", msg_notifikasi_1)
        if (not vid[0]):
            await message.edit(msg_notifikasi + f"\n{vid[1]}")
            return
        msg_notifikasi_2 = msg_notifikasi + "\n<b>👉 Sedang diupload</b>"

        duration = await convert_to_seconds(data[1]['duration'])

        db = await bot.send_video(config.CHANNEL_DATABASE, vid[1]['namefile'], duration=duration, caption=f"( {data[1]['name']} ) By @{bot.botUsername}", reply_to_message_id=msg.id, progress=progress_for_pyrogram, progress_args=(msg_notifikasi_2, message, time.time()))
        await db.copy(msg.from_user.id, caption=f"( {data[1]['name']} ) By @{bot.botUsername}")
        await addFile(url, data[1]['name'], data[1]['size'], data[1]['duration'], data[1]['date'], db.id)

        if os.path.exists(vid[1]['namefile']):
            os.remove(vid[1]['namefile'])

        last_msg = "<b>✅ Video Telah Diupload ✅</b>"
        await start_message.edit(msg_notifikasi_2.replace("<b>👉 Sedang diupload</b>", last_msg))
        return
    else:
        await start_message.edit(f"{msg_notifikasi}\n{'━'*25}\n<b>❌ {data[1]}</b>")



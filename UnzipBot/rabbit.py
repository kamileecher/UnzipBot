import os
import shutil
import time
import zipfile
import rarfile
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from UnzipBot.functions import absolute_paths

rabbit_filter = filters.create(lambda _, __, query: query.data.lower() == "rabbit")


@Client.on_callback_query(rabbit_filter)
async def _rabbit(unzipbot, callback_query):
    start = datetime.now()
    msg = callback_query.message.reply_to_message
    await callback_query.message.delete()
    file_name = msg.document.file_name
    file_size = msg.document.file_size
    if file_size > 1524288000:
        await msg.reply("500 MB'den büyük dosyalara izin verilmez..", quote=True)
        return
    try:
        main = await msg.reply("Indiriliyor...", quote=True)
        file = await msg.download()
        await main.edit("Extracting Files...")
        if file_name.endswith(".zip"):
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall("downloads")
            dir_name = file.replace(".zip", "")
        if file_name.endswith(".rar"):
            with rarfile.RarFile(file, 'r') as rar_ref:
                rar_ref.extractall("downloads")
            dir_name = file.replace(".rar", "")
        extracted_files = [i async for i in absolute_paths(dir_name)]
        for file in extracted_files:
            try:
                await msg.reply_document(file, quote=False, disable_notification=True)
            except FloodWait as e:
                time.sleep(e.x)
        stop = datetime.now()
        await msg.reply(
            f"Cıkarma Basarıyla Tamamlandı..! \n\nIslem {round((stop - start).total_seconds() / 60, 2)} dakika da bitti.. \n\n@kamileecher1")
    except rarfile.RarCannotExec:
        await msg.reply("** HATA :** Bu Dosya hata verdi. İçerik çıkarılamıyor. \n\n"
                        "Bu, bir dosyanın uzantısı manuel olarak değiştirildiğinde hata olabilir. `.zip`/`.rar`dosya bu biçimde olmasa da \n\n"
                        "Lütfen başka bir dosya ile deneyin...", quote=True
                        )
    except Exception as e:
        await unzipbot.send_message(msg.chat.id, "**HATA : **" + str(
            e) + "\n\nBu mesajı @kamileecher1'a iletin de bu sorunu çözün.", quote=True)
    finally:
        if os.path.isdir("downloads"):
            shutil.rmtree("downloads")

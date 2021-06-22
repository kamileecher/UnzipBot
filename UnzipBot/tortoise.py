import os
import shutil
import time
import zipfile
import rarfile
from datetime import datetime
from pyrogram import Client, filters
from UnzipBot.functions import absolute_paths, progress
from pyrogram.errors import FloodWait

tortoise_filter = filters.create(lambda _, __, query: query.data.lower() == "tortoise")


@Client.on_callback_query(tortoise_filter)
async def _tortoise(unzipbot, callback_query):
    start = datetime.now()
    msg = callback_query.message.reply_to_message
    await callback_query.message.delete()
    file_name = msg.document.file_name
    file_size = msg.document.file_size
    if file_size > 1524288000:
        await msg.reply("500 MB'den büyük dosyalara izin verilmez.", quote=True)
        return
    try:
        main = await msg.reply("Indiriliyor...", quote=True)
        file = await msg.download(progress=progress, progress_args=(main, "İndiriliyor..."))
        await main.edit("Dosyalar cıkarılıyor...")
        if file_name.endswith(".zip"):
            with zipfile.ZipFile(file, 'r') as zip_ref:
                contents = zip_ref.namelist()
                zip_ref.extractall("downloads")
            dir_name = file.replace(".zip", "")
        if file_name.endswith(".rar"):
            with rarfile.RarFile(file, 'r') as rar_ref:
                contents = rar_ref.namelist()
                rar_ref.extractall("downloads")
            dir_name = file.replace(".rar", "")
        con_msg = await msg.reply("Icerik kontrol ediliyor...", quote=True)
        constr = ""
        for a in contents:
            b = a.replace(f"{dir_name}/", "")
            constr += b + "\n"
        ans = "**icerik** \n\n" + constr
        if len(ans) > 4096:
            await con_msg.edit("Icerik kontrol ediliyor... \n\ndosya olarak gönderiliyor...")
            f = open("icerik.txt", "w+")
            f.write(ans)
            f.close()
            await msg.reply_document("contents.txt")
            os.remove("icerik.txt")
        else:
            await msg.reply(ans)
        await con_msg.delete()
        extracted_files = [i async for i in absolute_paths(dir_name)]
        number = 0
        for file in extracted_files:
            try:
                number += 1
                sending = await msg.reply(f"**Yükleniyor... ({number}/{len(extracted_files)})**")
                await msg.reply_document(file, quote=False, progress=progress,
                                         progress_args=(sending, f"Yükleniyor... ({number}/{len(extracted_files)})"), disable_notification=True)
                await sending.delete()
            except FloodWait as e:
                time.sleep(e.x)
        stop = datetime.now()
        await msg.reply(
            f"Cıkarma Basarıyla Tamamlandı..! \n\nİslem {round((stop - start).total_seconds() / 60, 2)} dakika da bitti.. \n\n @kamileecher1")
    except rarfile.RarCannotExec:
        await msg.reply("** HATA :** Bu Dosya hata verdi. İçerik çıkarılamıyor..\n\n"
                        "Bu, bir dosyanın uzantısı manuel olarak değiştirildiğinde olabilir. `.zip`/`.rar` dosya bu biçimde olmasa bile.\n\n"
                        "Başka bir dosya ile deneyin lütfen.", quote=True
                        )
    except Exception as e:
        await unzipbot.send_message(msg.chat.id, "**HATA : **" + str(
            e) + "\n\nBu mesajı @kamileecher1'a iletin de bu sorunu çözün.")
    finally:
        if os.path.isdir("downloads"):
            shutil.rmtree("downloads")

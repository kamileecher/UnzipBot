from unzipbot import app
from Config import Config
from pyrogram.types import InlineKeyboardButton


class Data:
    # Start Message
    START = "Merhaba {}. \n\nDosya gönderebilirsin.."

    if Config.OWNER_ID != 0:
        if Config.OWNER_NAME:
            START += (
                f"\n\nSahip :- [{Config.OWNER_NAME}](tg://user?id={Config.OWNER_ID})"
            )
        else:
            print(
                "You added OWNER_ID but not OWNER_NAME. You need to put both or neithers"
            )
            print("Bottan cık")
            raise SystemExit
    else:
        START += f"\n\nBy @@kamileecher ♥"

    # About Message
    ABOUT = "**Haydaa** \n\nNe arıyorsun.. \n\nKanal : [Tıkla](https://t.me/liveeboxx)"

    if Config.OWNER_ID != 0:
        if Config.OWNER_NAME:
            ABOUT += (
                f"\n\nSahip :- [{Config.OWNER_NAME}](tg://user?id={Config.OWNER_ID})"
            )
        else:
            print(
                "You added OWNER_ID but not OWNER_NAME. You need to put both or neither"
            )
            print("Bottan cık")
            raise SystemExit

    # Deploy Message
    DEPLOY = """
**.....
"""
    
    HELP = """
**Yardıma ihtiyacınız var ?? **

Herhangi bir zip/rar dosyası gönderin, ardından bir mod seçin ve işiniz bitti!
Sıkıştırılmış unzip/unrardan çıkaracağım ve içeriğini size geri vereceğim.

**Komutlar** :-
/modes - mod sec
/about - yardım1
/help - bilgi
/start - basla

"""
    
    MODES = """
**Modlar nelerdir. ❔**

1) ** Mod1 🐢**
Biraz Yavaş Ama Sabit. 

Bu modu kullanırken, gerceklesen tüm gelismeler hakkında bilgilendirileceksiniz..

Diger modlara göre çok fazla zaman almaz ve önerilen yöntemdir.. 

2) ** Mod2 🐇**
Bit Hızlı ama daha az kullanıcı dostu.

Bu modu kullanırken, devam eden herhangi bir ilerleme hakkında bilgilendirilmeyeceksiniz. Sadece indirmenin tamamlanması ve yüklemenin tamamlanması bildirilecektir. 

Bu biraz hızlıdır ancak daha kücük dosyalar icin fazla zaman farkı olmayacagından yalnızca daha büyük dosyalar icin önerilir..   
    """

    CHOOSE_MODE = "**MOD SEC ** \n\nDosyaları cıkarmak mod sec..."

    # Home Button
    home_button = [[InlineKeyboardButton(text="🏠 Geri Dön 🏠", callback_data="home")]]

    # Modes Buttons

    modes_buttons = [
        [
            InlineKeyboardButton("Mod1 🐢", callback_data="tortoise"),
            InlineKeyboardButton("Mod2 🐇", callback_data="rabbit")
        ],
        [InlineKeyboardButton("Modlar nelerdir ⁉️", callback_data="modes")]
    ]

    # Rest Buttons
    buttons = [
        [
            InlineKeyboardButton("Modlar nelerdir ❔", callback_data="modes"),
            InlineKeyboardButton("📤 Hakkında 📤", callback_data="about"),
        ],
        [InlineKeyboardButton("Yardım ⁉️", callback_data="help")],
        [InlineKeyboardButton("♥ Sahip ♥", url="https://t.me/kamileecher")],
        [InlineKeyboardButton("🎨 Kanal 🎨", url="https://t.me/kamileecher1")],
    ]

from django.utils import timezone
import os
from django.core.files import File
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from telebot.types import Update
from telebot import types
from .models import *
import datetime
from django.core.exceptions import ObjectDoesNotExist
from telebot.types import Message
import telebot
import uuid

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)


button_texts_home = {
    '🏢 Biz haqimizda': 'about_us_home',
    "💁‍♂️Bog'lanish": 'contact',
    '💵Tolov amalga oshirish': 'payment',  
}

@bot.message_handler(commands=['start'])
def start(message):
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for text, value in button_texts_home.items():
            keyboard.add(types.InlineKeyboardButton(text=text, callback_data=value))
        
        client = Clients.objects.get(client_telegram_id=message.from_user.id)
        bot.send_message(message.chat.id, f"Assalomu alaykum {client.client_name}!" )
        bot.send_message(message.chat.id, "Asosiy sahifa.", reply_markup=keyboard)
    except Clients.DoesNotExist:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)    
        button = types.KeyboardButton(text='Kontakt yuborish.', request_contact=True)
        keyboard.add(button)
        bot.send_message(message.chat.id, "Assalomu alaykum! Ro'yxatdan o'tish uchun raqamingizni yuboring.", reply_markup=keyboard)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    bot.send_message(message.chat.id, "Ajoyib! Endi Ismingiz yuboring.", reply_markup=types.ReplyKeyboardRemove())
    user_id = message.from_user.id
    phone_number = message.contact.phone_number
    
    try:
        client_exists = Clients.objects.filter(client_telegram_id=user_id).exists()
        
        if client_exists:
            print("Royhatdan otgan!")
        else:
            Clients.objects.create(client_phon_number=phone_number, client_telegram_id=user_id)
            print(f"User {user_id} Nomer: {phone_number}")
    except Exception as e:
        print(f"An error occurred: {e}")


@bot.message_handler(func=lambda message: message.new_chat_members is not None)
def handle_new_chat_members(message: Message):
    bot.send_message(message.chat.id, "Meni guruhga qoshganingiz uchun rahmat!")

@bot.message_handler(func=lambda message: message.chat.type == 'group', content_types=['text'])
def handle_group_messages(message: Message):
    if message.reply_to_message is None:
        return  
@bot.message_handler(func=lambda message: True)
def handle_name(message):
    try:
        user_id = message.from_user.id
        full_name = message.text

        try:
            client = Clients.objects.get(client_telegram_id=user_id)
            client_exists = True
        except ObjectDoesNotExist:
            client_exists = False

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for text, value in button_texts_home.items():
            keyboard.add(types.InlineKeyboardButton(text=text, callback_data=value))

        if client_exists:
            client.client_name = full_name
            client.client_username = message.from_user.username
            client.save()
            bot.send_message(message.chat.id, f"Assalomu alaykum {client.client_name}")
            bot.send_message(message.chat.id, "Asosiy sahifa.", reply_markup=keyboard)
            bot.send_message('-1001978302538', f"""
New User Registered on Bot:
Name: {full_name}
Telegram ID: {user_id}
Telegram Username: @{message.from_user.username}
Phone Number: +{client.client_phon_number}
    """)
        else:
            client.client_name = full_name
            
            client.save()
            bot.send_message(message.chat.id, f"Siz muvaffaqiyatli ro'yxatdan o'tdingiz. {full_name}.")
            bot.send_message(message.chat.id, "Asosiy sahifa.", reply_markup=keyboard)
            bot.send_message('-1001978302538', f"""
New User Registered on Bot:
Name: {full_name}
Telegram ID: {user_id}
Telegram Username: @{message.from_user.username}
Phone Number: +{client.client_phon_number}
    """)
    except Exception as e:
        print(f"An error occurred: {e}")



@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    if call.data == 'about_us_home':
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="Ko'proq ma'lumot olish", url="https://rashidevs.uz"))
        keyboard.add(types.InlineKeyboardButton(text='🔙 Ortga', callback_data="home_page_back"))
        bot.send_photo(call.message.chat.id, photo='https://rashidevs.pyblog.uz/media/Banner.png', caption='''
Rashidevs.uz – Python dasturlash tili bo'yicha chukurlashtirilgan online ta’lim platformasi🔥

Rashidevs.uz – bu shunchaki ta’lim emas, bu o’zgarish ishtiyoqida yonayotgan yosh yuraklar uchun bir mayoqdir.💡
Hozirgi kunda:
- 5000+ tahsil olayotgan o'quvchilar🧑‍🎓
Biz birgalikda har bir inson o’z hayotini AyTi bilimlari yordamida o’zgartira oladigan kelajakni yaratamiz.🙌
''', reply_markup=keyboard)

    elif call.data == 'contact':
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text='🔙 Ortga', callback_data="home_page_back"))
        bot.send_photo(call.message.chat.id, photo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPB7w3Z7LmbiOsNTBfKZQpK_sOv7RXRbmv2YB6EH2cMw&s', caption="""
☎️Telefon raqam: +998902113123

⚡️Telegram: https://t.me/rashidevs

🌐Web-site: https://rashidevs.uz


Bizni ijtimoiy tarmoqlarda ham kuzatishingiz mumkin:👇

📎 YouTube: https://youtube.com/@rashidevs?si=jb9b0Vd7ycY-vNTi

📎Instagram: https://instagram.com/rashidevs
                       """, reply_markup=keyboard)
   
    elif call.data == 'payment':
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text='Pilot(333.000)', callback_data="silver"))
        keyboard.add(types.InlineKeyboardButton(text='Co Pilot(450.000)', callback_data="gold"))
        keyboard.add(types.InlineKeyboardButton(text='🔙 Ortga', callback_data="home_page_back"))
        bot.send_message(call.message.chat.id, "'Toza Python' kursi uchun tolov amalga oshirmoqchi bo'lgan tarifingizni tanlang.", reply_markup=keyboard)

    elif call.data == 'home_page_back':
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for text, value in button_texts_home.items():
            keyboard.add(types.InlineKeyboardButton(text=text, callback_data=value))
        bot.send_message(call.message.chat.id, "Asosiy sahifaga qaytdingiz.", reply_markup=keyboard)
    elif call.data == 'silver':
        d = Clients.objects.get(client_telegram_id=call.from_user.id)
        d.client_course_tarif = False
        d.save()
        bot.send_message(call.message.chat.id, """
TOLOV CHEKINI YUBORING!
💳Karta raqam: 9860 1201 1809 3505
👤Karta egasi: Abdurahmon Rashidov
💵Tolov miqdori:  333.000 ming s'om✅ (450.000 ming s'om)❌


ESLATMA❗️

Tolov chekini yuboriyotganingizda chekda tolov amalga oshirilgan sana soat daqiqalari korinib turishi kerak  aks holda chek qabul qilinmaydi.
                         """)
        bot.register_next_step_handler(call.message, handle_check_photo)  
    elif call.data == 'gold':
        d = Clients.objects.get(client_telegram_id=call.from_user.id)
        d.client_course_tarif = True
        d.save()
        bot.send_message(call.message.chat.id, """
TOLOV CHEKINI YUBORING!
💳Karta raqam: 9860 1201 1809 3505
👤Karta egasi: Abdurahmon Rashidov
💵Tolov miqdori:  450.000 ming s'om✅ (650.000 ming s'om)❌


ESLATMA❗️

Tolov chekini yuboriyotganingizda chekda tolov amalga oshirilgan sana soat daqiqalari korinib turishi kerak  aks holda chek qabul qilinmaydi.
                         """)
        bot.register_next_step_handler(call.message, handle_check_photo)  

@bot.message_handler(content_types=['photo'])
def handle_check_photo(message):
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file = bot.download_file(file_info.file_path)
        d = uuid.uuid4()
        photo_path = os.path.join('media', f'{d}.jpg')
        with open(photo_path, 'wb') as new_file:
            new_file.write(file)

        client = Clients.objects.get(client_telegram_id=message.from_user.id)
        s = client.client_check_photo.save(f'{d}.jpg', File(open(photo_path, 'rb')))
        
        utc_offset = datetime.timedelta(hours=5)
        o = message.from_user.username
  
        if client.client_course_tarif:
            tarif_name = 'Co Pilot'
        else:
            tarif_name = 'Pilot'
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for text, value in button_texts_home.items():
            keyboard.add(types.InlineKeyboardButton(text=text, callback_data=value))

        bot.send_message(message.chat.id, "Rasm muvafaqiyatli adminga yuborildi 24 soat ichida korib chiqiladi!")
        bot.send_message(message.chat.id, "Asosiy sahifaga qaytdingiz.", reply_markup=keyboard)
        
        caption = f'''
👤 {client.client_name}
 ├ id: {client.client_telegram_id}
 ├ username: @{o}
 ├ phone_number: {client.client_phon_number}
 ├ tarif: {tarif_name}
 └ created: {datetime.datetime.now() + utc_offset}
'''
        bot.send_photo('-1002002883756', photo=open(photo_path, 'rb'), caption=caption)
    else:
        bot.send_message(message.chat.id, "Iltimos rasmni qaytatdan yuboring.")

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        json_str = request.body.decode('UTF-8')
        update = Update.de_json(json_str)
        bot.process_new_updates([update])
    return JsonResponse({'status': 'ok'})

def set_webhook(): 
    bot.remove_webhook()
    bot.set_webhook(url='https://rashidevs.pyblog.uz/webhook/')

set_webhook()
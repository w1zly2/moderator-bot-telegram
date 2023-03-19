#Импорты
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from filters import IsAdminFilter
import datetime
import random
import asyncio
import config
import time
import db

#Запуск бота
bot = Bot(token=config.TOKEN, parse_mode="html")
dp = Dispatcher(bot)

#Создание базы данных
db.CreateUserDB()
db.CreateChatDB()

#Активация фильтра админов чата
dp.filters_factory.bind(IsAdminFilter)

#Основное
@dp.message_handler(content_types=["new_chat_members"])
async def new_member(message):
    await message.answer(f'Привет, <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>')
    await message.delete()

@dp.message_handler(commands='start')
async def start(message):
    await message.reply(f"""
Привет, <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
Я  бот-модератор чата @chat_python_ru
Но я могу работать и в других чатах
    
Мой список команд: /help
    
    """)

@dp.message_handler(commands='help')
async def commands(message):
    await message.reply(f"""
<code>!ban</code> = баню
<code>!unban</code> = убераю с бана
<code>!mute</code> = затыкаю рот
<code>!unmute</code> = разрешаю говорить
+ = повышаю репутацию
- = понижаю репутацию
<code>!report</code> = жалуюсь админам
<code>!info</code> = информация о пользователе
    
    """)

@dp.message_handler(lambda msg: msg.text.lower() == 'бот')
async def check_bot(message):
    await message.reply('✅Бот работает!')

#Комманды модератора
@dp.message_handler(commands='mute', commands_prefix='!', is_chat_admin=True)
async def mute(message):
   if not message.reply_to_message:
      await message.reply("Эта команда должна быть ответом на сообщение!")
      return
   try:
      muteint = int(message.text.split()[1])
      mutetype = message.text.split()[2]
      comment = " ".join(message.text.split()[3:])
   except IndexError:
      await message.reply('Не хватает аргументов!\nПример:\n<code>!mute 1 ч причина</code>')
      return
   if mutetype == "ч" or mutetype == "часов" or mutetype == "час":
      await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date=datetime.timedelta(hours=muteint))
      await message.reply(f'👤Администратор: <a href="tg://?id={message.from_user.id}">{message.from_user.first_name}</a>\n🔇Замутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰Срок: {muteint} {mutetype}\n📃Причина: {comment}')
   if mutetype == "м" or mutetype == "минут" or mutetype == "минуты":
      await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date=datetime.timedelta(minutes=muteint))
      await message.reply(f'👤Администратор: <a href="tg://?id={message.from_user.id}">{message.from_user.first_name}</a>\n🔇Замутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰Срок: {muteint} {mutetype}\n📃Причина: {comment}')
   if mutetype == "д" or mutetype == "дней" or mutetype == "день":
      await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date=datetime.timedelta(days=muteint))
      await message.reply(f'👤Администратор: <a href="tg://?id={message.from_user.id}">{message.from_user.first_name}</a>\n🔇Замутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰Срок: {muteint} {mutetype}\n📃Причина: {comment}')

@dp.message_handler(commands='unmute', commands_prefix='!', is_chat_admin=True)
async def unmute(message):
   if not message.reply_to_message:
      await message.reply("Эта команда должна быть ответом на сообщение!")
      return
   await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(True, True, True, True))
   await message.reply(f'👤Администратор: <a href="tg://?id={message.from_user.id}">{message.from_user.first_name}</a>\n🔊Размутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>')

@dp.message_handler(commands='ban', commands_prefix='!', is_chat_admin=True)
async def ban(message):
   if not message.reply_to_message:
      await message.reply("Эта команда должна быть ответом на сообщение!")
      return
   comment = " ".join(message.text.split()[1:])
   await bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False))
   await message.reply(f'👤Администратор: <a href="tg://?id={message.from_user.id}">{message.from_user.first_name}</a>\n⛔Забанил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰Срок: навсегда\n📃Причина (если есть): {comment}')

@dp.message_handler(commands='unban', commands_prefix='!', is_chat_admin=True)
async def unban(message):
   if not message.reply_to_message:
      await message.reply("Эта команда должна быть ответом на сообщение!")
      return
   await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(True, True, True, True))
   await message.reply(f'👤Администратор: <a href="tg://?id={message.from_user.id}">{message.from_user.first_name}</a>\n⚠️Разбанил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>')

#Репутация
@dp.message_handler(lambda msg: msg.text.lower().startswith('+'))
async def plus_rep(message):
   if not message.reply_to_message:
      await message.reply("Эта команда должна быть ответом на сообщение!")
      return
   if message.from_user.id == message.reply_to_message.from_user.id:
      await message.reply("А нельзя накручивать себе репутацию!🖕")
      return
   db.UpdateUserValue('reputation', 1, message.reply_to_message.from_user.id)
   db.con.commit()
   await message.reply("Повышение репутации засчитано👍")

@dp.message_handler(lambda msg: msg.text.lower().startswith('-'))
async def minus_rep(message):
   if not message.reply_to_message:
      await message.reply("Эта команда должна быть ответом на сообщение!")
      return
   if message.from_user.id == message.reply_to_message.from_user.id:
      await message.reply("А нельзя накручивать себе репутацию!🖕")
      return
   db.UpdateUserValueMinus('reputation', 1, message.reply_to_message.from_user.id)
   db.con.commit()
   await message.reply("Понижение репутации засчитано👎")


#Профиль
@dp.message_handler(commands='info', commands_prefix='!')
async def profile(message):
   if not message.reply_to_message:
      for row in db.cursor.execute(f"SELECT reputation FROM users where id={message.from_user.id}"):
         await message.reply(f"""👤Имя: {message.from_user.first_name}
🐕Юзернейм: @{message.from_user.username}
🆔Айди: <code>{message.from_user.id}</code>
🔝Репутация: {row[0]}""")
   else:
      for row in db.cursor.execute(f"SELECT reputation FROM users where id={message.reply_to_message.from_user.id}"):
         await message.reply(f"""👤Имя: {message.reply_to_message.from_user.first_name}
🐕Юзернейм: @{message.reply_to_message.from_user.username}
🆔Айди: <code>{message.reply_to_message.from_user.id}</code>
🔝Репутация: {row[0]}""")

#Лидерборды (топ)
@dp.message_handler(commands=['leaderboard', 'top', 'лидеры', 'топ'], commands_prefix='!?./')
async def leaderboard(message):
   db.cursor.execute(f"SELECT name, reputation FROM users ORDER BY reputation DESC LIMIT 10")
   leadermsg = "<b>Топ 10 по репутации</b>:\n\n"
   fetchleader = db.cursor.fetchall()
   for i in fetchleader:
      leadermsg += f"{fetchleader.index(i) + 1}) {i[0]}:  {i[1]}$\n"
   await message.reply(str(leadermsg))

#Стата
@dp.message_handler(commands=['статистика', 'stats', 'стата'], commands_prefix='!?./')
async def stats(message):
   db.cursor.execute("SELECT id FROM users")
   users = db.cursor.fetchall()
   db.cursor.execute(f"SELECT chat_id FROM chats")
   chats = db.cursor.fetchall()
   await message.reply(f'👤 Пользователей в боте: {str(len(users))}\n💬Чатов в боте: {str(len(chats))}')

#Юзер рассылка (юзерпост)
@dp.message_handler(commands=['userpost', 'юзерпост'], commands_prefix='!?./')
async def userpost(message):
   if message.from_user.id == config.ADMIN_ID:
      userpost_text = " ".join(message.text.split()[1:])
      db.cursor.execute(f"SELECT id FROM users")
      users_query = db.cursor.fetchall()
      user_ids = [user[0] for user in users_query]
      confirm = []
      decline = []
      await message.reply('Рассылка юзерпоста началась...')
      for user_send in user_ids:
         try:
            await bot.send_message(user_send, userpost_text)
            confirm.append(user_send)
         except:
            decline.append(user_send)
      await message.answer(f'📣 Рассылка юзерпоста завершена!\n\n✅ Успешно: {len(confirm)}\n❌ Неуспешно: {len(decline)}')
   else:
      await message.reply("Недостаточно прав!")

#Чат рассылка (чатпост)
@dp.message_handler(commands=['chatpost', 'чатпост'], commands_prefix='!?./')
async def chatpost(message):
   if message.from_user.id == config.ADMIN_ID:
      chatpost_text = " ".join(message.text.split()[1:])
      db.cursor.execute(f"SELECT chat_id FROM chats")
      chats_query = db.cursor.fetchall()
      chats_ids = [chat[0] for chat in chats_query]
      confirm = []
      decline = []
      await message.reply('Рассылка чатпоста началась...')
      for chat_send in chats_ids:
         try:
            await bot.send_message(chat_send, chatpost_text)
            confirm.append(chat_send)
         except:
            decline.append(chat_send)
      await message.answer(f'📣 Рассылка чатпоста завершена!\n\n✅ Успешно: {len(confirm)}\n❌ Неуспешно: {len(decline)}')
   else:
      await message.reply("Недостаточно прав!")


#Репорты
@dp.message_handler(commands='report', commands_prefix='!')
async def report(message):
      admins_list = [admin.user.id for admin in await bot.get_chat_administrators(chat_id=message.chat.id)]
      report_comment = " ".join(message.text.split()[1:])
      await message.reply("Репорт отправлен!")
      for adm_id in admins_list:
         await bot.send_message(adm_id, text=f'Поступил репорт!\nhttps://t.me/{message.chat.username}/{message.reply_to_message.message_id}\nПричина: <b>{report_comment}</b>')

#Фильтр текста
@dp.message_handler(content_types=['text'])
async def filter_text(message):

   #Добавление чата в базу данных
   if message.chat.type != 'private':
      db.cursor.execute(f"SELECT chat_name, chat_id FROM chats where chat_id = {message.chat.id}")
      if db.cursor.fetchone() == None:
         db.InsertChatValues(message.chat.title, message.chat.id)

   #Добавление юзера в базу данных
   db.cursor.execute(f"SELECT name FROM users where id = {message.from_user.id}")
   if db.cursor.fetchone() == None:
      db.InsertUserValues(message.from_user.first_name, message.from_user.id)


#Поллинг
if __name__ == "__main__":
   executor.start_polling(dp, skip_updates=True)
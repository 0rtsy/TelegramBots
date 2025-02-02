import datetime
import sqlite3
from aiogram.types import Message
from aiogram import Dispatcher
from creator_bot import bot
from keyboards import creator_buts as buts
from config import date_now

def url_user(id, tag, name):
	name = name.replace("<", "").replace(">", "")
	if tag is None or tag == "@None":
		return f"<a href='tg://openmessage?user_id={id}'>{name}</a>"
	tag = tag.strip("@")
	return f"<a href='https://t.me/{tag}'>{name}</a>"

async def cmd_start(message: Message):
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("SELECT is_invited FROM users WHERE id = ?", [message.from_user.id])
	is_invited = cr.fetchone()
	if is_invited is None:
		cr.execute("INSERT INTO users VALUES (?, ?, ?, ?)", [
			message.from_user.id,
			f"@{message.from_user.username}",
			date_now(datetime.datetime.now()),
			0
		])
		conn.commit()
		is_invited = 0
	else:
		is_invited = is_invited[0]
		if is_invited == 0:
			await message.reply("⏳Ваша заявка всё ещё не одобрена, ожидайте!")
		else:
			cr.execute("SELECT * FROM admins WHERE id = ?", [message.from_user.id])
			if cr.fetchone() is not None:
				await message.reply("👑Админ панель:", reply_markup=buts.adm_menu())
				return
			await message.reply("✅Ваша заявка уже одобрена")
		return
	text = (
		f"📍{url_user(message.from_user.id, message.from_user.username, message.from_user.full_name)} подал заявку на участие в рассылке.\n"
		f"Нажмите <i>Одобрить</i>, чтобы одобрить заявку"
	)
	cr.execute("SELECT id FROM admins")
	adm_id = cr.fetchall()
	for i in adm_id:
		try:
			await bot.send_message(chat_id=i[0], text=text, reply_markup=buts.invite_user(message.from_user.id))
		except: continue
	await message.reply("☑Ваша заявка отправлена на рассмотрение!")


def reg_others(dp: Dispatcher):
	dp.register_message_handler(cmd_start, commands=["start", "help"])


import sqlite3
import datetime
import asyncio
from aiogram import Dispatcher
from aiogram.types import Message
from config import date_now
from keyboards import creator_buts as buts

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class EditTime(StatesGroup):
	new_time = State()

class AddText(StatesGroup):
	new_text = State()

def is_adm(id: int):
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("SELECT * FROM admins WHERE id = ?", [id])
	is_admin = cr.fetchone()
	if is_admin is None:
		return True
	return False

async def not_admin(message: Message):
	return


async def view_config(message: Message):
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("SELECT UTC FROM config WHERE num = 1")
	utc = cr.fetchone()[0]
	date = date_now(datetime.datetime.now())
	date1 = date.date().strftime("%d.%m.%Y")
	date2 = date.time().strftime("%H:%M")
	text = (
		f"⚙️<b>Настройки:</b>\n\n"
		f"🕰Время на сервере:\n"
		f"   <i>{date1} {date2}</i> (+{utc})"
	)
	await message.answer(text, reply_markup=buts.config_menu())

async def view_texts(message: Message):
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("SELECT num, text FROM texts")
	texts = cr.fetchall()
	text = (
		f"<b>📝Тексты:</b>\n"
		f"📦Всего: <b>{len(texts)}</b> шт.\n\n"
		f"<i>Выберете текст, чтобы редактировать его</i>"
	)
	texts_list = {}
	for txt in texts:
		texts_list[txt[0]] = f"{txt[0]}. {txt[1][0:20]}"
	await message.answer(text, reply_markup=buts.texts_menu(texts_list))

async def view_newsletters(message: Message):
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("SELECT num, date FROM newsletters")
	nls = cr.fetchall()
	text = (
		f"<b>📚Рассылка:</b>\n"
		f"📦Всего: <b>{len(nls)}</b> шт.\n\n"
		f"<i>Выберете номер рассылки, чтобы редактировать его</i>"
	)
	nls_list = {}
	for nl in nls:
		nls_list[nl[0]] = f"{nl[0]}. В {nl[1]}"
	await message.answer(text, reply_markup=buts.nls_menu(nls_list))

async def edit_time(message: Message, state: FSMContext):
	new_time = message.text
	try:
		new_time = int(new_time)
	except:
		await message.reply("❌<b>Сообщение не распознано!</b>")
		await message.delete()
		await state.finish()
		await asyncio.sleep(1)
		await message.answer("👑Админ панель:", reply_markup=buts.adm_menu())
		return
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("UPDATE config SET UTC = ?", [new_time])
	conn.commit()

	await state.finish()
	await message.delete()
	await message.answer("✅<b>Время обновлено!</b>", reply_markup=buts.adm_menu())
	await view_config(message)

async def add_text(message: Message, state: FSMContext):
	text = message.text
	text2 = ""
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("SELECT COUNT(*) FROM texts")
	if cr.fetchone()[0] >= 99:
		await message.answer("Невозможно иметь больше 99 текстов!")
		await state.finish()
		return
	if len(text) >= 3800:
		await message.answer(f"Слишком длинный текст!\n{len(text)}/3800 символов")
		await state.finish()
		return
	if message.entities is None or message.entities == []:
		text2 = text
	else:
		x = 0
		for i in text:
			for ent in message.entities:
				if ent.offset == x:
					if ent.type == "bold":
						text2 += "<b>"
					elif ent.type == "italic":
						text2 += "<i>"
					elif ent.type == "strike":
						text2 += "<s>"
					elif ent.type == "undeeline":
						text2 += "<u>"
					elif ent.type == "text_link":
						text2 += f"<a href='{ent.url}'>"
					else:
						continue
				elif ent.offset+ent.length == x:
					if ent.type == "bold":
						text2 += "</b>"
					elif ent.type == "italic":
						text2 += "</i>"
					elif ent.type == "strike":
						text2 += "</s>"
					elif ent.type == "undeeline":
						text2 += "</u>"
					elif ent.type == "text_link":
						text2 += f"</a>"
					else:
						continue
			text2 += text[x]
			x += 1

	cr.execute("SELECT num FROM texts")
	try:
		n = cr.fetchall()[-1][0]
	except:
		n = 0
	cr.execute("INSERT INTO texts VALUES (?, ?, ?)", [text2, "[]", n+1])
	conn.commit()
	await message.answer(f"✅Новый текст №{n+1} добавлен!")
	await state.finish()





def reg_admins(dp: Dispatcher):
	dp.register_message_handler(not_admin, lambda ms: is_adm(ms.from_user.id))
	dp.register_message_handler(view_config, lambda ms: ms.text == "⚙️Настройки")
	dp.register_message_handler(view_texts, lambda ms: ms.text == "📝Тексты")
	dp.register_message_handler(view_newsletters, lambda ms: ms.text == "📚Рассылка")
	dp.register_message_handler(edit_time, state=EditTime.new_time.state)
	dp.register_message_handler(add_text, state=AddText.new_text.state)

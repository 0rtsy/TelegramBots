import sqlite3
import datetime
from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from creator_bot import bot
from handlers.admins import EditTime, AddText
from keyboards import creator_buts as buts

from aiogram.dispatcher import FSMContext


async def invite_user(call: CallbackQuery):
	user_id = int(call.data.split("-")[1])
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("UPDATE users SET is_invited = 1 WHERE id = ?", [user_id])
	conn.commit()
	await call.answer("✅Заявка одобрена!")
	ent_text = call.message.text[0:call.message.entities[0].length]
	ent_url = call.message.entities[0].url
	text = (f"✅<a href='{ent_url}'>{ent_text}</a>, заявка одобрена!")
	await call.message.edit_text(text)
	await bot.send_message(chat_id=user_id, text="✅Ваша заявка одобрена!")

async def edit_time(call: CallbackQuery):
	date = datetime.datetime.now()
	date1 = date.date().strftime("%d.%m.%Y")
	date2 = date.time().strftime("%H:%M")
	await call.message.edit_text(f"Введите новое значение\n<i>{date1} {date2}</i> (+<b>?</b>)", )
	await EditTime.new_time.set()

async def finish_state(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await call.message.delete()
	await call.message.answer("👑Админ панель:", reply_markup=buts.adm_menu())

async def view_info_text(call: CallbackQuery):
	num_text = int(call.data.split("-")[1])
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("SELECT text, state FROM texts WHERE num = ?", [num_text])
	try:
		text, state = cr.fetchone()
	except:
		await call.answer("❌Текст не найден!", show_alert=True)
		await call.message.delete()
		return
	state_text = "❌Не используется"
	if len(eval(state)) > 0:
		state_text = "Используется в текстах(-е) "
		for num in eval(state):
			state_text += f"{num}, "
	text = (
		f"📝Текст <i>№{num_text}</i>:\n\n"
		f"{text}\n\n"
		f"📖Всего: <b>{len(text)}</b> символов\n"
		f"📍Статус: <b>{state_text}</b>"
	)
	await call.message.edit_text(text, reply_markup=buts.menu_text(num_text))

async def view_info_nls(call: CallbackQuery):
	num_nls = int(call.data.split("-")[1])
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("SELECT date, num_text FROM newsletters WHERE num = ?", [num_nls])
	try:
		date, num_text = cr.fetchone()
	except:
		await call.answer("❌Рассылка не найдена!", show_alert=True)
		await call.message.delete()
		return
	text = (
		f"📚Рассылка <i>№{num_nls}</i>:\n\n"
		f"⏳Время: в {date}\n"
		f"📝Текст: <b>№{num_text}</b>"
	)
	await call.message.edit_text(text, reply_markup=buts.menu_nls(num_nls))

async def del_text(call: CallbackQuery):
	num_text = int(call.data.split("-")[1])
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("DELETE FROM texts WHERE num = ?", [num_text])
	conn.commit()
	await call.message.edit_text(f"🗑️Текст <i>№{num_text}</i> удалён", reply_markup=buts.menu_delled_text())

async def del_nls(call: CallbackQuery):
	num_nls = int(call.data.split("-")[1])
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("DELETE FROM newsletters WHERE num = ?", [num_nls])
	conn.commit()
	await call.message.edit_text(f"🗑️Рассылка <i>№{num_nls}</i> удалёна", reply_markup=buts.menu_delled_nls())

async def edit_time_nls(call: CallbackQuery):
	num_nls = int(call.data.split("-")[1])
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("SELECT * FROM newsletters WHERE num = ?", [num_nls])
	try:
		info_nls = cr.fetchone()[0]
	except:
		await call.answer("❌Рассылка не найдена!", show_alert=True)
		await call.message.delete()
		return
	text = (
		f"Рассылка №{num_nls}\n"
		f"Выберете время: <u>??</u>:??"
	)
	await call.message.edit_text(text, reply_markup=buts.menu_edit_time_nls(num_nls))

async def edit_time_nls1(call: CallbackQuery):
	hour = int(call.data.split("-")[1])
	num_nls = int(call.data.split("-")[2])
	text = (
		f"Рассылка №{num_nls}\n"
		f"Выберете время: {hour}:<u>??</u>"
	)
	await call.message.edit_text(text, reply_markup=buts.menu_edit_time_nls1(num_nls, hour))

async def edit_time_nls2(call: CallbackQuery):
	hour = int(call.data.split("-")[1])
	min = int(call.data.split("-")[2])
	num_nls = int(call.data.split("-")[3])
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("UPDATE newsletters SET date = ? WHERE num = ?", [f"{hour}:{min}", num_nls])
	conn.commit()
	text = (
		f"Рассылка №{num_nls}\n"
		f"Время: {hour}:{min}\n\n"
		f"✅Изменено"
	)
	await call.message.edit_text(text)

async def edit_text_nls(call: CallbackQuery):
	num_nls = int(call.data.split("-")[1])
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("SELECT * FROM newsletters WHERE num = ?", [num_nls])
	try:
		info_nls = cr.fetchone()[0]
	except:
		await call.answer("❌Рассылка не найдена!", show_alert=True)
		await call.message.delete()
		return
	cr.execute("SELECT num, text FROM texts")
	texts = cr.fetchall()
	text = (
		f"Рассылка №{num_nls}\n"
		f"Выберете текст: "
	)
	texts_list = {}
	for txt in texts:
		texts_list[txt[0]] = f"{txt[0]}. {txt[1][0:20]}"
	await call.message.edit_text(text, reply_markup=buts.edit_text_nls(num_nls, texts_list))

async def edit_text_nls1(call: CallbackQuery):
	num_text = int(call.data.split("-")[1])
	num_nls = int(call.data.split("-")[2])
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("SELECT state FROM texts WHERE num = ?", [num_text])
	try:
		state = eval(cr.fetchone()[0])
	except:
		await call.answer("Текст не найден!", show_alert=True)
		return
	state.append(num_nls)
	cr.execute("UPDATE texts SET state = ? WHERE num = ?", [str(state), num_text])
	cr.execute("UPDATE newsletters SET num_text = ? WHERE num = ?", [num_text, num_nls])
	conn.commit()
	text = (
		f"Рассылка №{num_nls}\n"
		f"Текст: №{num_text}\n\n"
		f"✅Изменено"
	)
	await call.message.edit_text(text)



async def back_list_texts(call: CallbackQuery):
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
		texts_list[text[0]] = f"{txt[0]}. {txt[1][0:15]}..."
	await call.message.edit_text(text, reply_markup=buts.texts_menu(texts_list))

async def add_text(call: CallbackQuery):
	text = (
		f"Введите новый текст\n"
	)
	await call.message.edit_text(text, reply_markup=buts.finish_state())
	await AddText.new_text.set()

async def add_nls(call: CallbackQuery):
	text = (
		f"Новая рассылка:\n"
		f"Выберете время: <u>??</u>:??"
	)
	await call.message.edit_text(text, reply_markup=buts.menu_new_nls())

async def add_nls2(call: CallbackQuery):
	nls_hour = call.data.split("-")[1]
	nls_hour_text = nls_hour
	if len(nls_hour) == 1:
		nls_hour_text = f"0{nls_hour}"
	text = text = (
		f"Новая рассылка:\n"
		f"Выберете время: <i>{nls_hour_text}:??</i>"
	)
	await call.message.edit_text(text, reply_markup=buts.menu_new_nls2(int(nls_hour)))

async def add_nls3(call: CallbackQuery):
	nls_hour = call.data.split("-")[1]
	nls_min = call.data.split("-")[2]
	nls_hour_text = nls_hour
	if len(nls_hour) == 1:
		nls_hour_text = f"0{nls_hour}"
	nls_min_text = nls_min
	if len(nls_min) == 1:
		nls_min_text = f"0{nls_min}"
	text = (
		f"Новая рассылка:\n"
		f"Время: <i>{nls_hour_text}:{nls_min_text}</i>\n"
		f"Выберете текст: ?"
	)
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("SELECT num, text FROM texts")
	texts = cr.fetchall()
	texts_list = {}
	for txt in texts:
		texts_list[txt[0]] = f"{txt[0]}. {txt[1][0:20]}"
	await call.message.edit_text(text, reply_markup=buts.menu_new_nls3(int(nls_hour), int(nls_min), texts_list))

async def add_nls_f(call: CallbackQuery):
	nls_hour = call.data.split("-")[1]
	nls_min = call.data.split("-")[2]
	num_text = int(call.data.split("-")[3])
	nls_hour_text = nls_hour
	if len(nls_hour) == 1:
		nls_hour_text = f"0{nls_hour}"
	nls_min_text = nls_min
	if len(nls_min) == 1:
		nls_min_text = f"0{nls_min}"

	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("SELECT num FROM newsletters ORDER BY num ASC")
	try:
		num_nls = cr.fetchall()[-1]+1
	except:
		num_nls = 1
	if num_text != 0:
		cr.execute("SELECT state FROM texts WHERE num = ?", [num_text])
		try:
			state = eval(cr.fetchone()[0])
		except:
			await call.answer("Текст не найден!", show_alert=True)
			return
		state.append(num_nls)
		cr.execute("UPDATE texts SET state = ? WHERE num = ?", [str(state), num_text])
	cr.execute("INSERT INTO newsletters VALUES (?, ?, ?)", [num_nls, f"{nls_hour_text}:{nls_min_text}", num_text])
	conn.commit()
	text = (
		f"Рассылка №{num_nls}:\n"
		f"Время: <i>{nls_hour_text}:{nls_min_text}</i>\n"
		f"Текст: №{num_text}\n\n"
		f"✅Новая рассылка добавлена"
	)
	await call.message.edit_text(text)

async def del_message(call: CallbackQuery):
	await call.message.delete()

async def back_new_nls(call: CallbackQuery):
	n = int(call.data.split("-")[-1])
	if n == 0:
		await add_nls(call)
	elif n == 1:
		await add_nls2(call)


def reg_calls(dp: Dispatcher):
	dp.register_callback_query_handler(invite_user, lambda c: c.data.split("-")[0] == "invite_user")
	dp.register_callback_query_handler(edit_time, lambda c: c.data.split("-")[0] == "edit_time")
	dp.register_callback_query_handler(finish_state, lambda c: c.data.split("-")[0] == "finish_state", state="*")
	dp.register_callback_query_handler(view_info_text, lambda c: c.data.split("-")[0] == "view_info_text")
	dp.register_callback_query_handler(view_info_nls, lambda c: c.data.split("-")[0] == "view_info_nls")
	dp.register_callback_query_handler(del_text, lambda c: c.data.split("-")[0] == "del_text")
	dp.register_callback_query_handler(del_nls, lambda c: c.data.split("-")[0] == "del_nls")
	dp.register_callback_query_handler(edit_time_nls, lambda c: c.data.split("-")[0] == "edit_time_nls")
	dp.register_callback_query_handler(edit_time_nls1, lambda c: c.data.split("-")[0] == "edit_time_nls0")
	dp.register_callback_query_handler(edit_time_nls2, lambda c: c.data.split("-")[0] == "edit_time_nls1")
	dp.register_callback_query_handler(edit_text_nls, lambda c: c.data.split("-")[0] == "edit_text_nls")
	dp.register_callback_query_handler(edit_text_nls1, lambda c: c.data.split("-")[0] == "edit_text_nls1")
	dp.register_callback_query_handler(back_list_texts, lambda c: c.data.split("-")[0] == "back_list_texts")
	dp.register_callback_query_handler(add_text, lambda c: c.data.split("-")[0] == "add_text")
	dp.register_callback_query_handler(add_nls, lambda c: c.data.split("-")[0] == "add_nls")
	dp.register_callback_query_handler(add_nls2, lambda c: c.data.split("-")[0] == "new_nls0")
	dp.register_callback_query_handler(add_nls3, lambda c: c.data.split("-")[0] == "new_nls1")
	dp.register_callback_query_handler(add_nls_f, lambda c: c.data.split("-")[0] == "new_nls2")
	dp.register_callback_query_handler(del_message, lambda c: c.data.split("-")[0] == "del_msg")
	dp.register_callback_query_handler(back_new_nls, lambda c: c.data.split("-")[0] == "back_new_nls")


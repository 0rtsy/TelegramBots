import datetime
import sqlite3
import asyncio
from aiogram import executor
from creator_bot import dp, bot
from config import date_now

from handlers import reg_handlers
from keyboards import reg_keyboadrs
reg_handlers(dp)
reg_keyboadrs(dp)

async def newsletter(text: str):
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("SELECT id FROM users WHERE is_invited = 1")
	users = cr.fetchall()
	s = 0
	e = 0
	for user in users:
		try:
			await bot.send_message(chat_id=user[0], text=text)
			s += 1
		except:
			e += 1
			continue
		await asyncio.sleep(0.04)
	return [len(users), s, e]

async def check_time():
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("SELECT num, date, num_text FROM newsletters")
	nls = cr.fetchall()
	for nl in nls:
		num, date, num_text = nl
		if len(date) == 4:
			date = f"0{date}"
		if date == date_now(datetime.datetime.now()).time().strftime("%H:%M"):
			if num_text != 0:
				cr.execute("SELECT text FROM texts WHERE num = ?", [num_text])
				try:
					text = cr.fetchone()
				except:
					continue
				a, s, e = await newsletter(text[0])
				text = (
					f"Рассылка №{num}:\n\n"
					f"Время: {date}\n"
					f"Отправлено: {s}/{a} чел.\n"
					f"Заблокировали бота: {e} чел."
				)
				cr.execute("SELECT id FROM admins")
				for adm_id in cr.fetchall():
					await bot.send_message(chat_id=adm_id[0], text=text)




async def scheduler():
	while True:
		await check_time()
		await asyncio.sleep(40)

async def on_startup(_):
	asyncio.create_task(scheduler())



if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

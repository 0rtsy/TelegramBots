from aiogram import Dispatcher
from handlers import others, admins

def reg_handlers(dp: Dispatcher):
	others.reg_others(dp)
	admins.reg_admins(dp)
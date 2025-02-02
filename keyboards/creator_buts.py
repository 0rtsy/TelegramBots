from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def invite_user(user_id):
	return InlineKeyboardMarkup().add(
		InlineKeyboardButton(text="✅Одобрить", callback_data=f"invite_user-{user_id}")
	)

def adm_menu():
	return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
		*["📚Рассылка", "📝Тексты", "⚙️Настройки"]
	)

def config_menu():
	return InlineKeyboardMarkup().add(
		InlineKeyboardButton(text="🕓Изменить время", callback_data="edit_time")
	)

def finish_state():
	return InlineKeyboardMarkup().add(
		InlineKeyboardButton(text="🚫Отмена", callback_data="finish_state")
	)

def texts_menu(texts: dict):
	menu = InlineKeyboardMarkup(row_width=2)
	for i in texts:
		menu.insert(InlineKeyboardButton(text=texts[i], callback_data=f"view_info_text-{i}"))
	menu.add(InlineKeyboardButton(text="➕Добавить", callback_data="add_text"))
	return menu
def nls_menu(nls: dict):
	menu = InlineKeyboardMarkup(row_width=2)
	for i in nls:
		menu.insert(InlineKeyboardButton(text=nls[i], callback_data=f"view_info_nls-{i}"))
	menu.add(InlineKeyboardButton(text="➕Добавить", callback_data="add_nls"))
	return menu

def menu_text(num_text):
	return InlineKeyboardMarkup(row_width=2).add(
		InlineKeyboardButton(text="🗑️Удалить", callback_data=f"del_text-{num_text}"),
		InlineKeyboardButton(text="↩️Назад", callback_data="back_list_texts")
	)

def menu_nls(num_nls):
	return InlineKeyboardMarkup(row_width=2).add(
		InlineKeyboardButton(text="✏️Изменить текст", callback_data=f"edit_text_nls-{num_nls}"),
		InlineKeyboardButton(text="🕓Изменить время", callback_data=f"edit_time_nls-{num_nls}"),
		InlineKeyboardButton(text="🗑️Удалить", callback_data=f"del_nls-{num_nls}"),
		InlineKeyboardButton(text="↩️Назад", callback_data="back_list_nls")
	)

def menu_delled_text():
	return InlineKeyboardMarkup().add(
		InlineKeyboardButton(text="↩️Назад", callback_data="back_list_texts")
	)
def menu_delled_nls():
	return InlineKeyboardMarkup().add(
		InlineKeyboardButton(text="↩️Назад", callback_data="back_list_nls")
	)

def menu_new_nls():
	menu = InlineKeyboardMarkup(row_width=5)
	for i in range(25):
		menu.insert(InlineKeyboardButton(text=i, callback_data=f"new_nls0-{i}"))
	menu.add(InlineKeyboardButton(text="🚫Отмена", callback_data="del_msg"))
	return menu
def menu_new_nls2(hour: int):
	menu = InlineKeyboardMarkup(row_width=5)
	for i in range(60):
		menu.insert(InlineKeyboardButton(text=i, callback_data=f"new_nls1-{hour}-{i}"))
	menu.add(InlineKeyboardButton(text="↩️Назад", callback_data=f"back_new_nls-0"))
	return menu
def menu_new_nls3(hour: int, min: int, texts: dict):
	menu = InlineKeyboardMarkup(row_width=2)
	for i in texts:
		menu.insert(InlineKeyboardButton(text=texts[i], callback_data=f"new_nls2-{hour}-{min}-{i}"))
	menu.add(InlineKeyboardButton(text="🚫Не выбирать", callback_data=f"new_nls2-{hour}-{min}-0"))
	menu.add(InlineKeyboardButton(text="↩️Назад", callback_data=f"back_new_nls-{hour}-1"))
	return menu

def menu_edit_time_nls(num_nls):
	menu = InlineKeyboardMarkup(row_width=5)
	for i in range(25):
		menu.insert(InlineKeyboardButton(text=i, callback_data=f"edit_time_nls0-{i}-{num_nls}"))
	return menu
def menu_edit_time_nls1(num_nls, hour):
	menu = InlineKeyboardMarkup(row_width=5)
	for i in range(60):
		menu.insert(InlineKeyboardButton(text=i, callback_data=f"edit_time_nls1-{hour}-{i}-{num_nls}"))
	return menu

def edit_text_nls(num_nls, texts: dict):
	menu = InlineKeyboardMarkup(row_width=2)
	for i in texts:
		menu.insert(InlineKeyboardButton(text=texts[i], callback_data=f"edit_text_nls1-{i}-{num_nls}"))
	return menu

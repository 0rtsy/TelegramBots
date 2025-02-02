import sqlite3
import datetime

def date_now(date: datetime):
	conn = sqlite3.connect("base.db")
	cr = conn.cursor()
	cr.execute("SELECT UTC FROM config WHERE num = 1")
	UTC = cr.fetchone()[0]
	return date + datetime.timedelta(hours=UTC)
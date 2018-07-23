import pymysql

db = pymysql.connect("148.72.232.169", "chatbot", "j0b@9Zx1","rannlab_chatbot.db")
cursor = db.cursor()
sql = """CREATE TABLE RESPONSE (message varchar(50),intent varchar(20), score int)"""
cursor.execute(sql)
try :
	cursor.execute(sql)
	db.commit()

except :
	db.rollback()

db.close()

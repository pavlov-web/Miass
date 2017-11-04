from app.db_postgresql import SQL_Postgre
from datetime import  datetime
from app.views import bot
import threading
import time
#from app.views import send_msg
def start_runner():
    thread = threading.Thread(target=run_job)
    thread.start()

def run_job():
    while True:
        bot.send_message(61714776, "hello")
        time.sleep(5)
        '''
        now = datetime.now()
        time.sleep(3)
        db = SQL_Postgre()
        contact_info = db.find_data_contact(now.month,now.day)
        if contact_info.__len__() != 0:
            strmsg = 'День рождение у' + str(contact_info[0][1]) + ' ' + str(contact_info[0][0])
            bot.send_message(contact_info[0][2], strmsg)
        db.close()
        '''
start_runner()
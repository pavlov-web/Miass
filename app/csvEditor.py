import csv
import io
import re
from app.db_postgresql import SQL_Postgre

def csv_dict_reader(text, user_id):
    """
    Read a text file (csv-text)
    """
    db = SQL_Postgre()
    # Проверяем есть ли контакты в базе, если да - удаляем их
    if (db.check_contacts(user_id) == True):
        db.delete_contacts(user_id)
    reader = csv.DictReader(io.StringIO(text), delimiter=',')

    for line in reader:
        name = line['Name']
        birth = line['Birthday']
        resultName = re.sub('[^А-Яа-яA-Za-z ]', '', name)
        resultBirth = re.sub('[^-\wА-Яа-яA-Za-z.;0-9 ]', '', birth)
        if birth != '':
            if name != '':
                db.new_contacts(name, birth, user_id)
    db.close()

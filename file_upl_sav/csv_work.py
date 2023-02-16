import csv
from main.models import OwnerModel
from table_work.table_work import clear_tb, add_data_tb


def csv_creater():
    users = OwnerModel.objects.all()
    with open('main/static/saved/data.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        for user in users:
            writer.writerow([user.lexemm, user.morph, user.role, ])


def csv_reader(f):
    clear_tb()
    with open('main/static/upload/' + f, 'r', encoding="utf-8") as file:
        csvreader = csv.reader(file)
        list_tuples = [tuple(row) for row in csvreader]
        add_data_tb(list_tuples)

from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


class Member(BaseModel):
    ФИО: str


app = FastAPI()

db = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_NAME
}


@app.post("/import-members/")
async def create_item(data: List[Member]):
    mydb = mysql.connector.connect(**db)
    mycursor = mydb.cursor()
    sql = "INSERT INTO Members (name) VALUES (%s)"
    l = len(data)
    count = 0
    dublicates = 0
    err = 0
    for m in data:
        fio = m.ФИО.replace("     ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ").upper().lstrip().rstrip()
        val = (fio,)
        try:
            mycursor.execute(sql, val)
            count += 1
        except mysql.connector.errors.IntegrityError as e:
            if e.errno == 1062:
                dublicates += 1
            else:
                err += 1
    sql = "SELECT COUNT(name) FROM Members"
    mycursor.execute(sql)
    all = mycursor.fetchall()[0][0]
    mydb.commit()
    mydb.close()
    return f"Добавлено {count} из {l} членов Профсоюза. Дубликатов: {dublicates}, ошибок: {err}. Всего записей в базе данных: {all}."


@app.post("/create-tickets")
async def create_tickets(count: int):
    mydb = mysql.connector.connect(**db)
    mycursor = mydb.cursor()

    sql = "SELECT ticket_id FROM Tickets ORDER BY ticket_id DESC LIMIT 1"
    mycursor.execute(sql)
    r = mycursor.fetchall()
    if len(r) > 0:
        start = r[0][0] + 1
    else:
        start = 1

    sql = "INSERT INTO Tickets (ticket_id, status) VALUES (%s, %s)"

    for i in range(count):
        val = (start, "0 - Не выдан для реализации",)
        mycursor.execute(sql, val)
        start += 1

    mydb.commit()
    mydb.close()
    return f"Добавлено {count} новых билетов."



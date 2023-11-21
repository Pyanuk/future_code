from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

def connect_to_database():
    return sqlite3.connect('Пицерия.db')

def create_table():
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute('''
     CREATE TABLE IF NOT EXISTS PIZZERIA (
     id INTEGER PRIMARY KEY,
     Name TEXT NOT NULL,    
     Email TEXT NOT NULL,
     Telephone NOT NULL
     )
     ''')
    conn.commit()
    conn.close()

def insert_pizzeria(name, email,telephone):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO PIZZERIA (NAME_PIZZERIA, EMAIL, TELEPHONE) VALUES (?, ?, ?)' ,(name,email, telephone))

    conn.commit()
    conn.close()
def select_all_pizzeria(name):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM PIZZERIA')
    pizzerias = cursor.fetchall()

    for pizzeria in pizzerias:
        print(pizzeria)

    conn.close()

def select_pizzeria_by_name_pizzeria(name):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute('SELECT NAME_PIZZERIA, EMAIL, TELEPHONE FROM PIZZERIA WHERE NAME_PIZZERIA = ?', (name,))
    results = cursor.fetchall()

    for row in results:
        print(row)

    conn.close()

def update_email_by_pizzerias(name, new_email):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute('UPDATE PIZZERIA SET EMAIL = ? WHERE NAME_PIZZERIA = ?',(new_email,  name))
    conn.commit()
    conn.close()

def delete_pizzeria_by_name_pizzeria(name):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM PIZZERIA WHERE NAME_PIZZERIA = ?', (name,))
    conn.commit()
    conn.close()

def main():
    create_table()

    while True:
        print('Выберите действие: ')
        print('1 - Добавить пицерию: ')
        print('2 - Посмотреть всех пицерий')
        print('3 - Найти пицерию по названию')
        print('4 - Изменит почту пицерии')
        print('5 - Удалить с баз данных пицерии')
        print('0 - Закрыть базу данных')

        choise = int(input('Введите номер действия: '))

        match choise:
            case 1:
                name = input('Введите название пицерии: ')
                email = input('Введите почту пиццерии: ')
                telephone = input('Введите телефон пицерии: ')
                insert_pizzeria(name,email, telephone)
                print('Пицерия успешно добавлена!')

            case 2:
                print('Список пицерий:')
                select_all_pizzeria(name)

            case 3:
                name_pizzeria = input('Введите название пиццерии для поиска: ')
                select_pizzeria_by_name_pizzeria(name)

            case 4:
                name_pizzeria = input('Введите название пицерии, почту которого хотите изменить: ')
                new_email = input('Укажите новую почту пицерии: ')
                update_email_by_pizzerias(name, new_email)
                print('Почта обновлена!')

            case 5:
                new_email = input('Введите название пицерии для его удаление с базы данных: ')
                delete_pizzeria_by_name_pizzeria(name)
                print('Пиццерия успешно удалена!')

            case 0:
                print('Вы успешнл вышли с базы данных')
                break

class PIZZERIA_Create(BaseModel):
    Name: str
    Email: str  = None
    Telephone: str = None

@app.post("/pizzeria/", response_model=PIZZERIA_Create)
async def create_name(pizzeria: PIZZERIA_Create):
    insert_pizzeria(pizzeria.Name, pizzeria.Email, pizzeria.Telephone)
    return pizzeria

@app.get("/pizzeria/")
async def read_pizzeria():
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute('SELECT Name, Email, Telephone FROM PIZZERIA')
    pizzeria = cursor.fetchall()

    conn.close()

    return {"pizzeria": pizzeria}




if __name__ == '__main__':
    main()

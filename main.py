import psycopg2
#Функция, создающая структуру БД (таблицы).
import psycopg2


def create_db(conn):
    """Функция, создающая структуру БД (таблицы)"""
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS client(
        client_id INTEGER UNIQUE PRIMARY KEY,
        first_name VARCHAR(40),
        last_name VARCHAR(60),
        email VARCHAR(60)
        );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES client(client_id),
        phone VARCHAR(12)
        );""")
    conn.commit()  # фиксируем в БД
    cur.close()

def add_client(conn, client_id, first_name, last_name, email, phones=None):
    """Функция, позволяющая добавить нового клиента"""
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO client(client_id, first_name, last_name, email) 
           VALUES(%s, %s, %s, %s) RETURNING client_id;
       """, (client_id, first_name, last_name, email))
    client_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return client_id

def add_phone(conn, client_id, phone):
    """Функция, позволяющая добавить телефон для существующего клиента"""

    cur = conn.cursor()
    cur.execute("""
    INSERT INTO phones(client_id, phone) 
        VALUES(%s, %s) RETURNING id;
    """, (client_id, phone))
    phone_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return phone_id

def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    """Функция, позволяющая изменить данные о клиенте"""
    cur = conn.cursor()
    update_data = []
    query = "UPDATE client SET "
    if first_name:
        query += "first_name = %s, "
        update_data.append(first_name)
    if last_name:
        query += "last_name = %s, "
        update_data.append(last_name)
    if email:
        query += "email = %s, "
        update_data.append(email)
    query = query.rstrip(', ')  # Убираем последнюю запятую
    query += "WHERE client_id = %s;"
    update_data.append(client_id)

    cur.execute(query, tuple(update_data))
    conn.commit()
    cur.close()

def delete_phone(conn, phone_id):
    """Функция, позволяющая удалить телефон для существующего клиента"""
    cur = conn.cursor()
    cur.execute("DELETE FROM phones WHERE id = %s;", (phone_id,))
    conn.commit()
    cur.close()


def delete_client(conn, client_id):
    """Функция, позволяющая удалить существующего клиента"""
    cur = conn.cursor()
    cur = conn.cursor()
    # Удаление всех телефонов, связанных с клиентом
    cur.execute("DELETE FROM phones WHERE client_id = %s;", (client_id,))
    # Удаление клиента
    cur.execute("DELETE FROM client WHERE client_id = %s;", (client_id,))
    conn.commit()
    cur.close()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    """Функция для поиска клиентов по заданным параметрам."""
    cur = conn.cursor()
    query = "SELECT * FROM client"
    search_data = []
    conditions = []

    if first_name:
        conditions.append("first_name = %s")
        search_data.append(first_name)
    if last_name:
        conditions.append("last_name = %s")
        search_data.append(last_name)
    if email:
        conditions.append("email = %s")
        search_data.append(email)
    if phone:
        conditions.append("client_id IN (SELECT client_id FROM phones WHERE phone = %s)")
        search_data.append(phone)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += ";"

    cur.execute(query, tuple(search_data))
    clients = cur.fetchall()
    cur.close()
    return clients


with psycopg2.connect(database="Client_db", user="postgres", password="12345") as conn:
    create_db(conn)
    #add_client(conn, 1, 'Anton', 'Naumov', 'anton.naumov@inbox.ru', '+79661236578')
    #add_client(conn, 2, 'Maksim', 'Zverev', 'maksim.Zverev@inbox.ru', '+79668485723')
    #add_client(conn, 3, 'Andrey', 'Smirnov', 'andrey.smirnov@google.com')
    #add_client(conn, 4, 'Boris', 'Kuznetsov', 'boris.kuznetsov@mail.ru')
    #add_client(conn, 5,'Ivan', 'Ivanov', 'ivan.ivanov@mail.ru', '+7965555555')
    #add_phone(conn, 3, '+79650449020')
    #add_phone(conn, 4, '+79650449022')
    #change_client(conn,1,'Artem','Naumov','artem.naumov@inbox.ru')
    #change_client(conn, 4, 'Ivan', 'Petrov', 'ivan.petrov@gmail.com')
    #delete_phone(conn, 1)
    #delete_client(conn, 4)
    #find_client(conn, first_name='Ivan')
    #find_client(conn, last_name='Naumov')
    #find_client(conn, email='anton.naumov@inbox.ru')
    #find_client(conn, phone='+79650449020')

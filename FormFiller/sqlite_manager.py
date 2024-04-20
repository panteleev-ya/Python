import sqlite3
from aiogram import types

db_filename = 'sqlite.db'
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()


# Загрузка категорий из базы данных
def load_categories():
    cursor.execute("SELECT category_name FROM categories")
    return [row[0] for row in cursor.fetchall()]


# Загрузка банков из базы данных
def load_banks():
    cursor.execute("SELECT bank_name FROM banks")
    return [row[0] for row in cursor.fetchall()]


# Загрузка известных пользователей из базы данных
def load_users():
    cursor.execute("SELECT user_id, username FROM users")
    return {str(row[0]): row[1] for row in cursor.fetchall()}


# Функция для определения банка по номеру карты
async def determine_bank_by_card_number(card_number: str) -> str:
    # Проверяем наличие соответствия номера карты в базе данных
    cursor.execute("SELECT bank_name FROM card_bank_mapping WHERE card_number=?", (card_number,))
    result = cursor.fetchone()
    return None if result is None else result[0]


async def map_card_number_to_bank(card_number: str, bank: str):
    # Проверяем, существует ли уже запись для этого номера карты в таблице маппинга
    cursor.execute("SELECT id FROM card_bank_mapping WHERE card_number=?", (card_number,))
    result = cursor.fetchone()
    if result is not None:
        # Если запись уже существует, обновляем банк в этой записи
        cursor.execute("UPDATE card_bank_mapping SET bank_name=? WHERE card_number=?", (bank, card_number))
    else:
        # Если запись не существует, создаем новую запись в таблице маппинга
        cursor.execute("INSERT INTO card_bank_mapping (card_number, bank_name) VALUES (?, ?)", (card_number, bank))
    conn.commit()


# Метод для добавления message_id в новую строку таблицы
async def add_bot_message(message: types.Message):
    message_id, chat_id = message.message_id, message.chat.id
    cursor.execute("INSERT INTO bot_messages (message_id, chat_id) VALUES (?, ?)", (message_id, chat_id))
    conn.commit()


# Метод для извлечения всех message_id из таблицы
async def get_all_bot_message_ids(chat_id: int) -> list[int]:
    cursor.execute("SELECT message_id FROM bot_messages WHERE chat_id=?", (chat_id,))
    rows = cursor.fetchall()
    return [row[0] for row in rows]


# Метод для удаления всех записей из таблицы
async def delete_all_bot_message_ids(chat_id: int):
    cursor.execute("DELETE FROM bot_messages WHERE chat_id=?", (chat_id,))
    conn.commit()


# Метод для добавления message_id в новую строку таблицы
async def add_user_message_id(message: types.Message):
    message_id, chat_id = message.message_id, message.chat.id
    cursor.execute("INSERT INTO user_messages (message_id, chat_id) VALUES (?, ?)", (message_id, chat_id))
    conn.commit()


# Метод для извлечения всех message_id из таблицы
async def get_all_user_message_ids(chat_id: int) -> list[int]:
    cursor.execute("SELECT message_id FROM user_messages WHERE chat_id=?", (chat_id,))
    rows = cursor.fetchall()
    return [row[0] for row in rows]


# Метод для удаления всех записей из таблицы
async def delete_all_user_message_ids(chat_id: int):
    cursor.execute("DELETE FROM user_messages WHERE chat_id=?", (chat_id,))
    conn.commit()


categories = load_categories()
banks = load_banks()
known_users = load_users()

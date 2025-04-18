import json
import os

USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "users.json")

def load_users():
    if os.path.exists(USERS_FILE):
        if os.path.getsize(USERS_FILE) == 0:
            return set()  # пустой файл — возвращаем пустой список
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(users), f, ensure_ascii=False)

# Загружаем при старте
user_ids = load_users()

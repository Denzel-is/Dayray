import psycopg2
import json

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",
    port="5432"
)

cursor = conn.cursor()

# SQL-запрос для получения данных о продуктах
cursor.execute("SELECT name, description, price, stock_quantity FROM products")
products = cursor.fetchall()

# Преобразование данных в JSONL формат для AI
with open("products_data.jsonl", "w", encoding="utf-8") as f:
    for product in products:
        print(product)  # Отладочная информация о значениях
        name = product[0]
        description = product[1]
        price = product[2]
        stock_quantity = product[3]

        # Структура JSON объекта в формате диалога
        product_data = {
            "messages": [
                {"role": "user", "content": f"Что вы можете сказать о {name}?"},
                {"role": "assistant", "content": f"{description}. Цена: {price}$. В наличии: {stock_quantity} шт."}
            ]
        }

        # Запись JSON строки в файл
        f.write(json.dumps(product_data, ensure_ascii=False) + "\n")

# Закрытие подключения
cursor.close()
conn.close()

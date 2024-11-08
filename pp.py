import psycopg2
import json


conn = psycopg2.connect(
    dbname="Dayray",
    user="postgres",
    password="food",
    port="5432"
)

cursor = conn.cursor()


cursor.execute("SELECT name, description, price, stock_quantity FROM products")
products = cursor.fetchall()


with open("products_data.jsonl", "w", encoding="utf-8") as f:
    for product in products:
        print(product) 
        name = product[0]
        description = product[1]
        price = product[2]
        stock_quantity = product[3]

       
        product_data = {
            "messages": [
                {"role": "user", "content": f"Что вы можете сказать о {name}?"},
                {"role": "assistant", "content": f"{description}. Цена: {price}$. В наличии: {stock_quantity} шт."}
            ]
        }


        f.write(json.dumps(product_data, ensure_ascii=False) + "\n")


cursor.close()
conn.close()

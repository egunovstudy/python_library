import psycopg2

conn = psycopg2.connect(
    dbname="test_base",
    user="postgres",
    password="1988",
    host="localhost",
    port="5432"
)

cur = conn.cursor()


def add_category(name):
    try:
        cur.execute(
            """
            INSERT INTO categories (name)
            VALUES (%s)
            """,
            (name,)
        )
        conn.commit()
        print(f"Категория '{name}' успешно добавлена.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при добавлении категории: {e}")


def add_supplier(name, contact_info):
    try:
        cur.execute(
            """
            INSERT INTO suppliers (name, contact_info)
            VALUES (%s, %s)
            """,
            (name, contact_info)
        )
        conn.commit()
        print(f"Поставщик '{name}' успешно добавлен.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при добавлении поставщика: {e}")


def add_product(name, description, quantity, category_id, price, supplier_id):
    try:
        cur.execute(
            """
            INSERT INTO products (name, description, quantity, category_id, price, supplier_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (name, description, quantity, category_id, price, supplier_id)
        )
        conn.commit()
        print(f"Товар '{name}' успешно добавлен.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при добавлении товара: {e}")


def create_shipment(supplier_id, items):
    try:
        cur.execute("BEGIN")

        cur.execute(
            """
            INSERT INTO shipments (supplier_id, shipment_date)
            VALUES (%s, CURRENT_TIMESTAMP)
            RETURNING id
            """,
            (supplier_id,)
        )
        shipment_id = cur.fetchone()[0]

        for item in items:
            product_id, quantity = item

            cur.execute(
                """
                SELECT id FROM products WHERE id = %s
                """,
                (product_id,)
            )
            if cur.fetchone() is None:
                raise Exception(f"Товар с ID {product_id} не существует.")

            cur.execute(
                """
                INSERT INTO shipment_items (shipment_id, product_id, quantity)
                VALUES (%s, %s, %s)
                """,
                (shipment_id, product_id, quantity)
            )

            cur.execute(
                """
                UPDATE products
                SET quantity = quantity + %s
                WHERE id = %s
                """,
                (quantity, product_id)
            )

            cur.execute(
                """
                INSERT INTO transactions (product_id, change, transaction_type)
                VALUES (%s, %s, 'add')
                """,
                (product_id, quantity)
            )

        conn.commit()
        print(f"Поставка #{shipment_id} успешно создана.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при создании поставки: {e}")


def update_product(product_id, name=None, description=None, price=None, category_id=None, supplier_id=None):
    try:
        query = "UPDATE products SET "
        params = []

        if name:
            query += "name = %s, "
            params.append(name)
        if description:
            query += "description = %s, "
            params.append(description)
        if price:
            query += "price = %s, "
            params.append(price)
        if category_id:
            query += "category_id = %s, "
            params.append(category_id)
        if supplier_id:
            query += "supplier_id = %s, "
            params.append(supplier_id)

        query = query.rstrip(', ')
        query += " WHERE id = %s"
        params.append(product_id)

        cur.execute(query, tuple(params))
        conn.commit()
        print(f"Товар с ID {product_id} успешно обновлен.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при обновлении товара: {e}")


def get_shipment_report():
    try:
        cur.execute(
            """
            SELECT s.id, s.shipment_date, sp.name AS supplier_name, p.name AS product_name, si.quantity
            FROM shipments s
            JOIN suppliers sp ON s.supplier_id = sp.id
            JOIN shipment_items si ON s.id = si.shipment_id
            JOIN products p ON si.product_id = p.id
            ORDER BY s.shipment_date DESC
            """
        )
        report = cur.fetchall()
        for row in report:
            print(f"Поставка #{row[0]} от {row[1]}: Поставщик: {row[2]}, Товар: {row[3]}, Количество: {row[4]}")
    except Exception as e:
        print(f"Ошибка при получении отчета по поставкам: {e}")


def delete_product(product_id):
    try:
        cur.execute(
            """
            DELETE FROM shipment_items WHERE product_id = %s
            """,
            (product_id,)
        )

        cur.execute(
            """
            DELETE FROM transactions WHERE product_id = %s
            """,
            (product_id,)
        )

        cur.execute(
            """
            DELETE FROM products WHERE id = %s
            """,
            (product_id,)
        )

        conn.commit()
        print(f"Товар с ID {product_id} успешно удален.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при удалении товара: {e}")



def main():
    add_category("Электроника")
    add_category("Мебель")

    add_supplier("Поставщик 1", "Контактная информация 1")
    add_supplier("Поставщик 2", "Контактная информация 2")

    add_product("Ноутбук", "Мощный ноутбук", 10, 1, 50000, 1)
    add_product("Стол", "Деревянный стол", 5, 2, 10000, 2)

    create_shipment(1, [(1, 20), (2, 10)])

    get_shipment_report()

    update_product(1, price=55000)

    delete_product(2)


if __name__ == "__main__":
    main()

cur.close()
conn.close()

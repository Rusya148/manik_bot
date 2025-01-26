import sqlite3

def get_clients_by_date_range(start_date, end_date):
    try:
        with sqlite3.connect('database_client.db') as connection:
            cursor = connection.cursor()

            cursor.execute('''
            SELECT * FROM clients
            WHERE DATE(day_rec) BETWEEN ? AND ?
            ORDER BY day_rec ASC
            ''', (start_date, end_date))

            rows = cursor.fetchall()
            return rows
    except sqlite3.OperationalError as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return []
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return []




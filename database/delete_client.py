import sqlite3

def delete_client(client_link):
    try:
        with sqlite3.connect('database_client.db') as connection:
            cursor = connection.cursor()

            cursor.execute('DELETE FROM clients WHERE LINK = ?', (client_link,))

            if cursor.rowcount:
                return True
            return False
    except sqlite3.Error as e:
        print(f'Ошибка при удалении клиента: {e}')
        return False


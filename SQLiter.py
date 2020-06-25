import sqlite3

class SQLiter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM CODES').fetchall()

    def select_single(self, number):
        """ Получаем одну строку с номером number """
        with self.connection:
            return self.cursor.execute('SELECT * FROM CODES').fetchall()[number]

    def select_code(self, code):
        """ Получаем одну строку с номером channel """
        with self.connection:
            return self.cursor.execute('SELECT * FROM CODES WHERE code = ?', (code,)).fetchall()[0]

    def count_rows(self):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM CODES').fetchall()
            return len(result)

    def insert_row(self, user_id, code, channel, notSub, sub):
        params = (user_id, code, channel, notSub, sub)
        self.cursor.execute("INSERT INTO CODES (user_id, code, channel, not_sub, sub) VALUES(?, ?, ?, ?, ?)", params)

    def delete_row(self, channel):
        # удаляем строку по значению channel
        with self.connection:
            self.cursor.execute('DELETE FROM CODES WHERE channel = ?', (channel,))

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
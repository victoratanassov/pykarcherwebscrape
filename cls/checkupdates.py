from datetime import datetime
import pymysql
from pymysql.cursors import DictCursor


class MySQLDataProcessor:
    def init(self, connection):
        self.conn = connection
        self.table_columns = {}
        self.archive_suffix = '_archive'

    def get_columns(self, table_name):
        if table_name not in self.table_columns:
            with self.conn.cursor() as cursor:
                cursor.execute(f"""
                    SELECT COLUMN_NAME, DATA_TYPE 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = '{table_name}'
                    ORDER BY ORDINAL_POSITION
                """)
                self.table_columns[table_name] = cursor.fetchall()
        return self.table_columns[table_name]

    def create_archive_table(self, table_name):
        archive_table = table_name + self.archive_suffix
        with self.conn.cursor() as cursor:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {archive_table} LIKE {table_name}")
            try:
                cursor.execute(f"ALTER TABLE {archive_table} DROP PRIMARY KEY")
            except pymysql.Error:
                pass
            cursor.execute(f"""
                ALTER TABLE {archive_table} 
                ADD COLUMN archive_id INT AUTO_INCREMENT PRIMARY KEY,
                ADD COLUMN archive_date DATETIME,
                ADD COLUMN operation VARCHAR(10)
            """)

    def check_data_changes(self, table_name, new_data):
        columns = [col[0] for col in self.get_columns(table_name) if col[0] != 'id']
        with self.conn.cursor(DictCursor) as cursor:
            cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (new_data['id'],))
            old_data = cursor.fetchone()

        if not old_data:
            return None  # Няма съществуващ запис

        changes = {}
        for col in columns:
            old_val = old_data.get(col)
            new_val = new_data.get(col)
            if old_val != new_val:
                changes[col] = (old_val, new_val)

        return changes if changes else None

    def archive_data(self, table_name, old_data, operation):
        archive_table = table_name + self.archive_suffix
        columns = [col[0] for col in self.get_columns(table_name)]

        placeholders = ', '.join(['%s'] * len(columns))
        query = f"""
            INSERT INTO {archive_table} 
            ({', '.join(columns)}, archive_date, operation)
            VALUES ({placeholders}, %s, %s)
        """

        values = [old_data[col] for col in columns]
        values.extend([datetime.now(), operation])

        with self.conn.cursor() as cursor:
            cursor.execute(query, values)

    def process_operation(self, table_name, data, operation):
        try:
            with self.conn.cursor(DictCursor) as cursor:
                # Създаване на архивна таблица ако не съществува
                self.create_archive_table(table_name)

                # Проверка за промени
                changes = self.check_data_changes(table_name, data)

                if operation == 'UPDATE' and changes:
                    # Взимане на старите данни за архивиране
                    cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (data['id'],))
                    old_data = cursor.fetchone()
                    self.archive_data(table_name, old_data, 'UPDATE')

                # Изпълнение на основната операция
                if operation == 'INSERT':
                    columns = [col[0] for col in self.get_columns(table_name) if col[0] in data]
                    placeholders = ', '.join(['%s'] * len(columns))
                    query = f"""
                        INSERT INTO {table_name} ({', '.join(columns)})
                        VALUES ({placeholders})
                    """
                    cursor.execute(query, [data[col] for col in columns])
                else:
                    set_clause = ', '.join([f"{k} = %s" for k in data if k != 'id'])
                    values = [v for k, v in data.items() if k != 'id']
                    values.append(data['id'])
                    cursor.execute(f"""
                        UPDATE {table_name}
                        SET {set_clause}
                        WHERE id = %s
                    """, values)

                self.conn.commit()
                return True
        except Exception as e:
            self.conn.rollback()
            raise e


# Пример за използване
if name == "main":
    connection = pymysql.connect(
        host='localhost',
        user='user',
        password='password',
        database='test_db',
        cursorclass=DictCursor
    )

    processor = MySQLDataProcessor(connection)

    # Примерни данни
    sample_data = {
        'id': 1,
        'name': 'New Name',
        'email': 'new@example.com',
        'age': 30
    }

    try:
        # Симулиране на UPDATE операция
        processor.process_operation('users', sample_data, 'UPDATE')

        # Симулиране на INSERT операция
        processor.process_operation('users', sample_data, 'INSERT')
    finally:
        connection.close()
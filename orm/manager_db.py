import colorama
import psycopg2
import datetime


class ConnectionSqliteManager:
    def __init__(self, db_settings):
        self.db_settings = db_settings

    def __enter__(self):
        print("Connection started ...")
        self.conn = psycopg2.connect(**self.db_settings)
        self.conn.autocommit = True
        self.curr = self.conn.cursor()
        return self

    def create_table(self, table_name, fields):
        create_command = f"CREATE TABLE {table_name} ({fields})"
        try:
            self.curr.execute(create_command)
            print(f"{colorama.Fore.CYAN}{table_name}: created successfully!")
            print(f"{datetime.datetime.now()}: Commit is successful!! {colorama.Style.RESET_ALL} \U0001F44D")
        except psycopg2.Error as er:
            print(f"{colorama.Fore.RED}[PostgreSQL ERROR!!]: {' '.join(er.args)} {colorama.Style.RESET_ALL}")

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("Connection ended ...")
        print()
        self.conn.close()
        if exc_type:
            print(f'[ERROR] error raised {exc_value}')



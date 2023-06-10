from orm.migration_to_db import MigrateCommand


if __name__ == '__main__':
    Command = MigrateCommand()
    Command.migrate()

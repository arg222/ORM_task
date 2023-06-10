import colorama
import argparse
import inspect
import importlib
import sys

import settings_db


class MigrateCommand:

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("migrate", type=str, help="Migrate all models in models.py to database")
        self.args = self.parser.parse_args()
        self.models = []

    def get_app_models(self):
        models_file_path = f'{settings_db.APP_NAME[0]}.models'
        importlib.import_module(models_file_path)
        for class_name, class_ in inspect.getmembers(sys.modules[models_file_path]):
            if inspect.isclass(class_):
                self.models.append(class_)

    @property
    def get_args(self):
        return self.args

    def migrate(self):
        self.get_app_models()
        if self.get_args.migrate == "migrate":
            for idx, model in enumerate(self.models, 1):
                print(f'**Migration** [{idx}] {colorama.Fore.CYAN} {model.object.table_name} {colorama.Style.RESET_ALL}')
                mig = model.object
                mig.migrate()
        elif self.get_args.migrate == "show-what-to-migrate":
            print(self.models)

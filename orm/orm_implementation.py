import psycopg2
import abc

from orm.manager_db import ConnectionSqliteManager
from settings_db import DATABASES


class AbstractClass(abc.ABC):

    @abc.abstractmethod
    def insert(self):
        pass

    @abc.abstractmethod
    def select(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def delete(self):
        pass


class CharField:
    def __init__(self, max_length=255, null=False):
        self.max_length = max_length
        self.null = null

    def __call__(self):
        dic = self.__dict__
        values = list(dic.values())
        if values[1] is True:
            return f'VARCHAR({values[0]}) NULL'
        return f'VARCHAR({values[0]}) NOT NULL'


class TextField:
    def __init__(self, null=False):
        self.null = null

    def __call__(self):
        dic = self.__dict__
        values = list(dic.values())
        if values[0] is True:
            return 'TEXT NULL'
        return 'TEXT NOT NULL'


class IntegerField:
    def __init__(self, null=True):
        self.null = null

    def __call__(self):
        dic = self.__dict__
        values = list(dic.values())
        if values[0] is True:
            return 'INTEGER NULL'
        return 'INTEGER NOT NULL'


class FloatField:
    def __init__(self, null=True):
        self.null = null

    def __call__(self):
        dic = self.__dict__
        values = list(dic.values())
        if values[0] is True:
            return 'REAL NULL'
        return 'REAL'


class IdField:
    def __init__(self, primary_key=True):
        self.primary_key = primary_key

    def __call__(self):
        return 'SERIAL PRIMARY KEY'


class BaseManager(AbstractClass):
    conn = psycopg2.connect(**DATABASES)
    conn.autocommit = True
    curr = conn.cursor()
    table_name = None
    dict_ = None

    def __init__(self, model_class):
        self.models_list = model_class
        self.table_name = self.models_list.__name__
        self.dict_ = self.models_list.__dict__

    def fields_attrs(self):
        keys_list = [key for key in self.dict_]
        obj_keys = keys_list[1:-1]
        all_obj = [values for values in self.dict_.values()]
        objs = all_obj[1:-1]
        obj_values = [obj() for obj in objs]
        fields_query_list = [f'{i[0]} {i[1]}' for i in zip(obj_keys, obj_values)]
        fields_query = ", ".join(fields_query_list)
        return fields_query

    def migrate(self):
        print("Begin database Migration ...")
        print(f"**{self.table_name}** Migration")
        with ConnectionSqliteManager(DATABASES) as Connection:
            Connection.create_table(table_name=self.table_name, fields=self.fields_attrs())

    def insert(self, **data: dict):
        fields = [key for key in data.keys()]
        values = list(data.values())
        values_form = f"({', '.join(['%s' for _ in fields])})"
        query = f"INSERT INTO {self.table_name} ({', '.join(fields)}) VALUES {values_form}"
        self.curr.execute(query, values)

    def insert_many(self, fields: tuple, data: list):
        fields_form = ', '.join(fields)
        values_form = f"({', '.join(['%s' for _ in fields])})"
        query = f"INSERT INTO {self.table_name} ({fields_form}) VALUES {values_form}"
        self.curr.executemany(query, data)

    def select(self, *fields, **kwargs):
        fields_name = ', '.join(fields)
        query = [f"{key} = '{value}'" for key, value in kwargs.items()]
        if kwargs:
            self.curr.execute(f"SELECT {fields_name} FROM {self.table_name} WHERE {''.join(query)}")
            return self.curr.fetchall()
        else:
            self.curr.execute(f"SELECT {fields_name} FROM {self.table_name}")
        return self.curr.fetchall()

    def all(self):
        self.curr.execute(f"SELECT * FROM {self.table_name}")
        return self.curr.fetchall()

    def update(self, *new_data, **kwargs):
        keys = new_data[0].keys()
        values = new_data[0].values()
        new_data_fields_form = list(new_data[0].values())
        set_query = ", ".join([f"{i[0]} = '{i[1]}'" for i in zip(keys, values)])
        query = [f"{key} = '{value}'" for key, value in kwargs.items()]
        if kwargs:
            self.curr.execute(f"UPDATE {self.table_name} SET {set_query} WHERE {''.join(query)}")
        else:
            self.curr.execute(f"UPDATE {self.table_name} SET {set_query}")

    def delete(self, **kwargs):
        if kwargs:
            query = [f"{key} = '{value}'" for key, value in kwargs.items()]
            self.curr.execute(f"DELETE FROM {self.table_name} WHERE {''.join(query)}")
        else:
            self.curr.execute(f"DELETE FROM {self.table_name}")


class MetaModel(type):
    manager_class = BaseManager

    def get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def object(cls):
        return cls.get_manager()


class Model(metaclass=MetaModel):
    def __init__(self):
        self.table_name = self.__class__.__name__
        dict_ = self.__class__.__dict__

        setattr(self, 'table_name', self.table_name)
        for i in dict_.keys():
            setattr(self, i, i)

    def __repr__(self):
        return self.table_name

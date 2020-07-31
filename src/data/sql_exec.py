from src.data.connect_db import create_engine_to_rds
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy import Column, String, Integer
from sqlalchemy import inspect
from sqlalchemy import Table
from sqlalchemy.orm import mapper
from sqlalchemy import select
from sqlalchemy import or_, and_
import pandas as pd


class SqlExec:
    """
    TODO update docs
    Interface to interact with SQL database
    
    Use SqlAlchemy to interact with SQL databases. The SqlExec needs to connect
    to an existing database. After the connection is made the class allows a 
    simple interface to create tables, add data and query data.
    
    Attributes
    ----------
    Base : sqlalchemy.ext.declarative.api.DeclarativeMeta
        SqlAlchemy's base class for table classes
        
    engine : sqlalchemy.engine.base.Engine
        SqlAlchemy's engine that is connected to the database
        
    session : sqlalchemy.orm.session.Session
        SqlAlchemy's ORM interface with the databse

    tables : sqlalchemy.util._collections.immutabledict
        tables that are mapped to the database from the ORM
    
    Methods
    ---------
    __init__(self, db='census_data')
        Initialize object with connection to database `db`
    
    add(self, obj, name=None, if_exists='append')
        Add data to a table in the database. 

        `obj`: pd.DataFrame, sqlalchemy.table.obj, list of sqlalchemy.table.obj
            Data to be added to a database table
        `name`: str
            if `obj` is type pd.DataFrame you must specify the table name
        `if_exists`: default='append', 'replace', 'fail'
            What action to take if the table already exists

    create_table_class(self, columns, table_name, class_name, pk_col='index')
        Create a sqlalchemy.table class. The class is not added to the database
        until the method `create_tables` is called.
    
    create_tables(self)
        Create tables in the database from table classes created with `create_table_class`
    """

    def __init__(self, db="postgres", verbose=False):
        """
        Connects to database and creates required attributes
        """

        self.engine = create_engine_to_rds(db, echo=verbose)
        self.session = sessionmaker(bind=self.engine)()

    @property
    def Base(self):
        return declarative_base()

    @property
    def meta(self):
        return self.Base.metadata

    @property
    def tables(self):
        return self.meta.tables

    @property
    def inspector(self):
        return inspect(self.engine)


    def add(self, obj, name=None, if_exists="append", index=False):
        """
        Add obj or list of objects of sqlalchemy table class
        """

        if isinstance(obj, list):
            self.session.add_all(obj)
            self.session.commit()

        elif isinstance(obj, pd.DataFrame):
            if name is None:
                raise NameError("Need to include table_name")

            obj = obj.reset_index()
            obj.columns = [col.lower().replace(" ", "_") for col in obj.columns]

            obj.to_sql(
                name, self.engine, if_exists=if_exists, method="multi", index=index
            )

        else:
            self.session.add(obj)
            self.session.commit()

    def create_tables(self):
        """
        Create all tables from `Base`
        """

        self.Base.metadata.create_all(self.engine)

    def create_table_class(self, columns, table_name, class_name):
        """
        Create table class. Classes need to be made before self.create_tables is used to actually create the tables in the db
        """

        columns = list(columns)
        pk_col = columns.pop(0)
        attr_dict = {"__tablename__": table_name}

        attr_dict[pk_col] = Column(String, primary_key=True)
        attr_dict.update({col: Column(String) for col in columns})

        table_class = type(class_name, (self.Base,), attr_dict)

        return table_class

    def get_df(self, table=None, columns=None, **kwargs):
        """
        Wrapper around pd.read_sql to return dataframe
        """

        with self.engine.connect() as con:
            df = pd.read_sql(sql=table, con=con, columns=columns, **kwargs)

        return df 


if __name__ == "__main__":

    sql_exec = SqlExec(verbose=True)

from core.core_settings import settings
from core.orm import write_query, query
import os

class UpMigration():

    def add_table(table_name,table_columns):
        '''
        table_name = (str) ex. "data_table"
        table_columns = (str) ex: "id,fk,name"
        '''
        with f_settings as open(f"{settings.PROJECT_FILEPATH}/core/core_settings.py","a"):
            f_settings.write(f"{table_name.upper()} = PROJECT_FILEPATH + '/data/{table_name}s.csv'")
        with f_table as open(f"{settings.PROJECT_FILEPATH}/data/{table_name}s.csv"):
            f_table.write(table_columns + ",\n")

    def drop_table(table_name):
        lines_to_save = []
        with r_settings as open(f"{settings.PROJECT_FILEPATH}/core/core_settings.py","r"):
            for line in r_settings:
                table = f"{table_name}s.csv"
                if table not in line:
                    lines_to_save.append(line)
        with w_settings as open(f"{settings.PROJECT_FILEPATH}/core/core_settings.py","w"):
            for line in lines_to_save:
                w_settings.write(line)
        try:
            os.system(f"rm {settings.PROJECT_FILEPATH}/data/{table_name}s.csv")
        except:
            print("Data Table not found")

            
    def add_column():
        pass

    def drop_column():
        pass
    

class DownMigration():

    def add_table():
        pass

    def drop_table():
        pass
    
    def add_column():
        pass

    def drop_column():
        pass


def Run():
    for file in os.listdir(f"{settings.PROJECT_FILEPATH}/migrations"):
        if file != "main.py":
            os.system(f"python3 {file}")

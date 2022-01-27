import os
import sys
import core_settings as settings

# TODO:  make all these functions only take args/kwargs

def write_query(filename,arguments,new=True,pk=None):
    '''a function for writing to a "DB" file
        filename : str
            the name/path of file
        arguments : list
            a list of arguments to write to the file (a list even with one arg)
        new : boolean
            if new is True, it will write everything to a new line, otherwise use the pk arg to find the right row to replace
        pk : int or None
            a number for primary key, only use with new = False
    '''

    if new == True:
        database = open(filename, "a")
        PK = len([line for line in open(filename, 'r')])

        #get the last line in the file
        with open(filename,"r") as f:
            for line in f:
                pass
            last_line = line
        last_pk = last_line.split(",")[0]
        if last_pk.isnumeric():
            if int(PK) <= int(last_pk):
                PK = int(last_pk) + 1
        print(PK)
        database.write(str(PK) + ",")
        [database.write(str(item) + ",") for item in arguments]
        database.write("\n")
        database.close()
    else:
        '''rewrite row'''
        database_rows = [row for row in open(filename, "r")]
        print(database_rows)

        database = open(filename, "w")
        column_titles = database_rows[0].split(",") #get names of columns
        print(column_titles)
        for index in range(len(database_rows)):
            if database_rows[index][0] == str(pk):
                print("found pk")
                # database.write(str(index) + ",") # dont need to write pk index if it is plugged into the arguments
                [database.write(str(item) + ",") for item in arguments]
                database.write("\n")
            else:
                database.write(database_rows[index])
        database.close()



def query(filename, argument,column_name=None,search_method=None): # TODO: FIX so it returns a dicitonary with the key being column name and value is column value
    '''a very simple function for returning a line from a csv (place holder for real db query)
        filename : (str) the name of the csv file
        argument : (str) a string you are trying to match
        column_name: (str) an optional arg to confirm you are searching for the right item and do not get mismatched (use for pk an foreign keys)
        search_method: (str or None) if you write "find all" it will append each match to a list
    '''
    f = open(filename, 'r')
    iteration = 0
    column_names = []
    column_index = None
    found_matches = []
    for line in f:
        if iteration == 0 and column_name is not None:
            '''get column name index'''
            column_names = [item for item in line.split(",")]
            for index in range(len(column_names)):
                if column_names[index] == column_name:
                    column_index = index
                    continue
        iteration += 1
        if argument in line:
            line_array = [item for item in line.split(",")]

            if column_index is None:
                '''look over whole line'''
                for column in line_array:
                    if column == argument:
                        # print(line_array)
                        # f.close()
                        if search_method == "find all":
                            found_matches.append(line_array)
                        else:
                            f.close()
                            return line_array
            else:
                '''look in column index only'''
                if str(line_array[int(column_index)]) == str(argument):
                    if search_method == "find all":
                        found_matches.append(line_array)
                    else:
                        f.close()
                        return line_array

    if search_method == "find all":
        f.close()
        return found_matches
    else:
        f.close()
        return None



# def update_query(filename, argument, ):




def delete_query(filename, argument ,amount="full"):
    '''a simple function for deleting a whole column if amount is set to "all"
    or just a single argument
    filename: (str) the name of the db file
    argument: (str) the thing you are trying to find
    amount: optional (str) if amount == "full" then it will erase the entire row else it will only delete the arguement column'''
    f = open(filename, 'w+')
    for line in f:
        if argument in line:
            if amount == "full":
                line_array = [item == '' for item in line.split(",")] #delete while line/row
                # print(line_array)
                line = [f.write(str(item) + ",") for item in line_array]
                # print(line_array[0])
                return
            else:
                line_array = [item for item in line.split(",") if item != argument]
                # print(line_array)
                line = [f.write(str(item) + ",") for item in line_array]
                # print(line_array[0])
                return


def add_table(table_name,columns):
    '''a function for creating a new table csv, writing it to core_settings
    arg: table_name - (str) what to name the file/core_settings variable
    arg: columns - what to name the columns'''
    #create csv
    new_table = open(f"{table_name}s.csv","w")
    cleaned_columns = [col.replace(",",";") if "," in col else col for col in columns] # remove , to not mess up csv
    [new_table.write(str(item) + ",") for item in cleaned_columns]
    #add to core_settings
    settings_file = open(settings.PROJECT_FILEPATH,'a')
    settings_file.write(f"{table_name.upper()}_TABLE = PROJECT_FILEPATH + '/data/{table_name}s.csv'")

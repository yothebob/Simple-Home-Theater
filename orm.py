import os
import sys

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
        print(PK)
        database.write(str(PK) + ",")
        [database.write(str(item) + ",") for item in arguments]
        database.write("\n")
        database.close()
    else:
        '''not supported yet'''
        pass



def query(filename, argument,column_name=None,search_method=None):
    '''a very simple function for returning a line from a csv (place holder for real db query)
        filename : (str) the name of the csv file
        argument : (str) a string you are trying to match
        column_name: (str) an optional arg to confirm you are searching for the right item and do not git mismatched (use for pk an foreign keys)
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
                    column_index = column_names[index]
                    continue
        iteration += 1
        if argument in line:
            line_array = [item for item in line.split(",")]

            if column_index is not None:
                '''look over whole line'''
                for column in line_array:
                    if column == argument:
                        print(line_array)
                        f.close()
                        if search_method == "find all":
                            found_matches += line_array
                        else:
                            return line_array
            else:
                '''look in column index only'''
                    if line_array[column_index] == argument:
                        if search_method == "find all":
                            found_matches += line_array
                        else:
                            return line_array

    if search_method == "find all":
        return found_matches
    else:
        return None




def delete_query(filename, argument ,amount="full"):
    '''a simple function for deleting a whole column if amount is set to "all"
    or just a single argument
    filename: (str) the name of the db file
    argument: (str) the thing you are trying to find
    amount: optional (str) if amount == "full" then it will erase the entire row else it will only delete the arguement column'''
    f = open(filename, 'r')
    for line in f:
        if argument in line:
            if amount == "full":
                line_array = [item == None for item in line.split(",")] #delete while line/row
                print(line_array)
                print(line_array[0])
                return line_array
            else:
                line_array = [item for item in line.split(",") if item != argument else item == ""]
                print(line_array)
                print(line_array[0])
                return line_array
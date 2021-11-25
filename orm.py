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



def query(filename, argument):
    '''a very simple function for returning a line from a csv (place holder for real db query)'''
    f = open(filename, 'r')
    for line in f:
        if argument in line:
            line_array = [item for item in line.split(",")]
            for column in line_array:
                if column == argument:
                    print(line_array)
                    print(line_array[0])
                    f.close()
                    return line_array




def delete_query(filename, argument ,amount="all"):
    '''a simple function for deleting a whole column if amount is set to "all"
    or just a single argument '''
    f = open(filename, 'r')
    for line in f:
        if argument in line:
            if amount == "full":
                line_array = [item == None for item in line.split(",")] #delete while line/row
                print(line_array)
                print(line_array[0])
                return line_array
            else:
                line_array = [item for item in line.split(",") if item != argument]
                print(line_array)
                print(line_array[0])
                return line_array

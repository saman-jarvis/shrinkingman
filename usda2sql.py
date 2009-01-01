#!/usr/bin/env python
###
# NOTE: BEFORE RUNNING THIS SCRIPT the usda.tar.bz2 file must be unpacked!!!
###
from pysqlite2 import dbapi2 as sqlite
import os
import sys
from string import atoi
from string import atof


SQL_FILE          = "usda.sql"
DB_FILE           = "usda.db"
USDA_DIR          = "usda/"
USDA_FOOD_DESCR   = USDA_DIR + "FOOD_DES.txt"
USDA_FOOD_TABLE   = "food"
USDA_GROUP_DESCR  = USDA_DIR + "FD_GROUP.txt"
USDA_GROUP_TABLE  = "food_group"

def init_db(cursor):
    sqlfile = file(SQL_FILE)
    sql     = sqlfile.read()
    cursor.executescript(sql)
    sqlfile.close()

# Transforms the given field from the USDA source data into the correct python
# variable type.
def transform_field(field):
    if field == None:
        return None
    value = field.strip("~")
    if value != field:
        return value
    elif "." in value:
        return atof(value)
    elif value == "":
        return 0
    else:
        return atoi(value)

# Transform all given USDA source data fields into the correct python
# variable type.
def transform_fields(fields):
    values = []
    for field in fields:
        value = transform_field(field)
        if value == None:
            return None
        values.append(value)
    return values

def get_column_names(cursor, table):
    sql     = "PRAGMA table_info(" + table + ")"
    columns = []
    cursor.execute(sql)
    for column in cursor:
        columns.append(column[1])
    return columns

def food_handler(fields):
    # The first two fields are specified as strings, which is braindead.
    fields[0] = int(fields[0])
    fields[1] = int(fields[1])
    return fields

def food_group_handler(fields):
    # The first fields is specified as string, which is braindead.
    fields[0] = int(fields[0])
    return fields

# Imports the given USDA file into the given table.
# The fields are extracted and then passed to the given
# fieldhandler function. This function should return the
# values in a form in which they can be imported into the DB.
def import_file(cursor, usdafile, table, fieldhandler):
    srcfile = file(usdafile)
    columns = get_column_names(cursor, table)
    for line in srcfile:
        line   = line.rstrip()
        fields = line.split("^")
        #print line

        # Translate the fields into the correct python variable types.
        fields = transform_fields(fields)
        if not fields:
            break
        
        fields = fieldhandler(fields)

        # Fire.
        sql = "INSERT INTO " + table \
            + "("  + (", ".join(columns))         + ")" \
            + " VALUES " \
            + "(?" + (", ?" * (len(columns) - 1)) + ")"
        
        #print sql
        sys.stdout.write(".")
        cursor.execute(sql, fields)
    cursor.close()

def start():
    print "Generating nutricion database...",
    if os.path.isfile(DB_FILE):
        print "exists already."
        sys.exit()
    print

    dh     = sqlite.connect(DB_FILE)
    cursor = dh.cursor()
    init_db(cursor)
    import_file(cursor, USDA_GROUP_DESCR, USDA_GROUP_TABLE, food_group_handler)
    import_file(cursor, USDA_FOOD_DESCR,  USDA_FOOD_TABLE,  food_handler)
    cursor.close()
    dh.commit()
    dh.close()
    print

if __name__ == '__main__':
    start()

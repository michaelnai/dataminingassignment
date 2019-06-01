import os
import pathlib
import pymysql
import csv
import pandas as pd
from datetime import datetime

MY_FOLDER_ROOT = "/Users/zeroyan/Downloads/cleaned/"
MY_SECTOR_FOLDER_ROOT = "/Users/zeroyan/Documents/_Master/workspace/wqd7005/sector-test/main market/"
MY_EDGE_FOLDER_ROOT = "/Users/zeroyan/Documents/_Master/workspace/wqd7005/the_edge/"
# os.listdir("/Users/zeroyan/Downloads/cleaned/")

conn = pymysql.connect(host='localhost', user='root', password='', db='stock', local_infile=True)

cursor = conn.cursor()


def skip_last(iterator):
    prev = next(iterator)
    for item in iterator:
        yield prev
        prev = item


def import_csv():
    load_sql = "LOAD DATA LOCAL INFILE '/Users/zeroyan/Downloads/cleaned/0002 Kotra Industries Bhd (KOIN).csv'  \
               INTO TABLE yan.temp_temp_stock \
                FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"

    cursor.execute(load_sql)
    print('Succuessfully loaded the table from csv.')
    conn.commit()
    conn.close()


def import_csv_param(stock_code, full_path):

    sql_select_Query = "select id from test_stock where stock_no = %s"
    sql_insert_Query = "INSERT INTO temp_stock_2(temp_id,exchange_date,close,open,high,low,volume,change_diff,stock_id)\
                           VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    cursor.execute(sql_select_Query, stock_code)

    s_row = cursor.fetchone()
    # print(s_row[0])
    stock_id = int(s_row[0])

    with open(full_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)
        # for row in reader:
        for row in skip_last(reader):
            # cursor.execute(sql_insert_Query, (row, stock_id))
            cursor.execute(sql_insert_Query, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], stock_id))
            # print(row)

        conn.commit()
        print("CSV has been imported into the database - " + stock_code)
        # cursor.close()


def import_csv_insert():
    with open('/Users/zeroyan/Downloads/cleaned/0002 Kotra Industries Bhd (KOIN).csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)
        # for row in reader:
        for row in skip_last(reader):
            cursor.execute('INSERT INTO temp_stock(temp_id,exchange_date,close,open,high,low,volume,change_diff,stock_id)\
                           ''VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 262)', row)
            print(row)

        conn.commit()
        cursor.close()
        print("CSV has been imported into the database")


def insert_stock_table(stock_code, stock_name, stock_no):
    sql_insert_query = """ INSERT INTO `test_stock`
                                          (`symbol`, `stock_name`, `stock_no`) VALUES (%s,%s,%s)"""

    insert_tuple = (stock_code, stock_name, stock_no)

    result = cursor.execute(sql_insert_query, insert_tuple)
    conn.commit()

    print("Record inserted successfully into test_stock table" + stock_code)


def read_the_edge():
    full_path = MY_EDGE_FOLDER_ROOT + "the_edge_title_with_date_NER.csv"

    sql_insert_Query = "INSERT INTO the_edge(texts,date,time,entities)\
                               VALUES(%s, %s, %s, %s)"

    with open(full_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)
        for row in reader:
            str_date = str(row[2]).strip()
            str_time = str(row[3]).strip()
            print(str_date+", "+str_time)

            d_date = datetime.strptime(str_date, '%d %b')
            d_date = d_date.replace(year=2019)
            # print(d_date.date())
            t_time = datetime.strptime(str_time, '%H:%M%p')
            # t_time = t_time.replace()
            print(str(d_date.date())+", "+str(t_time.time()))

            insert_tuple = (row[1], d_date.date(), t_time.time(), row[4])

            cursor.execute(sql_insert_Query, insert_tuple)
            conn.commit()

            print("Record inserted successfully into the_edge table" + row[0])


def read_sector_folder():
    full_path = MY_SECTOR_FOLDER_ROOT+"2019-03-08.csv"

    sql_Select_Query = "select id from test_sector where name=%s"
    sql_update_Query = "update test_stock set sector_id=%s where  "

    with open(full_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)
        for row in skip_last(reader):
             print(row[1]+", "+row[9])


def read_folder():

    # files_path = [os.path.abspath(x) for x in os.listdir(MY_FOLDER_ROOT)]
    # print(files_path)

    # flist = []
    for p in pathlib.Path(MY_FOLDER_ROOT).iterdir():
        if p.is_file():
            print(p)
            #flist.append(p)
            q = str(p).split('/')
            filename = q[5]
            r = filename.rsplit('.', 1)
            filename_noext = r[0]
            print(filename_noext)

            s = filename_noext.split()
            stock_no = s[0] # use this
            # print(stock_no)

            tt = filename_noext.split('(')
            filename2 = tt[0]
            #print(filename2[5:len(filename2)])
            #print(filename2[filename2.rfind('')+1:])
            #print(filename2.split(' ', 1))
            strsplit = filename2.split(' ', 1)
            stock_no2 = strsplit[0]
            stock_name2 = strsplit[1].strip()
            print(stock_no2)
            print(stock_name2)

            #print(tt)

            # xxx = re.split(r"(?<!^)\s*[.\n]+\s*(?!$)", filename_noext)
            # print(xxx)

            # ttt = filename_noext.rsplit(' ', 1)
            # print(ttt)

            filename3 = tt[1]
            # print(filename2)
            # print(filename3)
            stock_code = filename3.split(')')[0]
            print(stock_code)

            #insert_stock_table(stock_code, stock_name2, stock_no2)
            import_csv_param(stock_no2, str(p))

#import_csv()
#import_csv_insert()
#read_folder()
#read_sector_folder()

# war_start = '2011-01-03'
# war_start = '16 Mar'
# time_start = '01:15am'
# sss = datetime.strptime(war_start, '%d %b')
# sss = sss.replace(year=2019)
# print(sss.date())

# ttt = datetime.strptime(time_start, '%H:%M%p')
# print(ttt.time())

read_the_edge()
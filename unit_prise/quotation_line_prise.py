import xmlrpclib
import csv
from datetime import datetime

username = 'verp@it-corner.net' #the user
pwd = 'Crystal_5000'      #the password of the user
dbname = 'db_live'    #the database
# 
# # Connection String ........
# 
sock_common = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

reader = csv.reader(open('quotation_line.csv', "rb"), delimiter=';')
index = 0
count = 0
vals = {}
name = ''
for row in reader:
    if len(row) == 6:
        order_id = sock.execute(dbname, uid, pwd, 'sale.order', 'search', [('name', '=', row[0])])
        if len(order_id) != 0:
            product_id = sock.execute(dbname, uid, pwd, 'product.product', 'search', [('product_no', '=', row[4])])
            if len(product_id) != 0:
                line_id = sock.execute(dbname, uid, pwd, 'sale.order.line', 'search',[('order_id','=',order_id[0]),('product_id','=',product_id[0])])
                if len(line_id) != 0:
                    sock.execute(dbname, uid, pwd, 'sale.order.line', 'write',line_id[0],{'price_unit':row[3]})
            else:
                line_id = sock.execute(dbname, uid, pwd, 'sale.order.line', 'search',[('order_id','=',order_id[0]),('name','=',row[5])])
                if len(line_id) != 0:
                    sock.execute(dbname, uid, pwd, 'sale.order.line', 'write', line_id[0],{'price_unit':row[3]})

print "index = >", index
print "Count ==>", count
print " Ending Query ... "

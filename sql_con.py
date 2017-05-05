import mysql.connector

conn = mysql.connector.connect(
         user='root',
         password='root',
         host='127.0.0.1',
         port=3306,
         database='digi_student_tracker')


cur = conn.cursor()

query = ("SELECT * FROM student")


cur.execute(query)


for (id, name, dept, salary) in cur:
  print("{}, {}, {}, {}".format(id, name,dept,salary))

cur.close()
conn.close()
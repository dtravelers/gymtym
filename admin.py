import mysql.connector
from flask import session

class admin_operation:
    def connection(self):
        db = mysql.connector.connect(host="localhost", port="3306", user="root", password="root",database="gym")
        return db

    def admin_submit(self,name,email,password):
        con = self.connection()
        sq="insert into admin (name,email,password) values(%s,%s,%s)"
        record = [name,email,password]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        con.commit()
        cursor.close()
        con.close()
        return

    def admin_login_verify(self,email,password):
        con=self.connection()
        cursor=con.cursor() 
        sq="select name,email from admin where email=%s and password=%s"
        record = [email,password]
        cursor.execute(sq, record)
        row = cursor.fetchone()
        rc = cursor.rowcount
        cursor.close()
        con.close()
        return 1 if row else 0

    def trip_list(self):
       con=self.connection()
       cursor=con.cursor() 
       sq="select member_id,member_name,address,charges,phone_no,start_date,end_date from membership where admin_email=%s"
       record=[session['admin_email']]
       cursor.execute(sq,record)
       row = cursor.fetchall()
       cursor.close()
       con.close()
       return row
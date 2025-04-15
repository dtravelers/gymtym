import mysql.connector
from flask import session

class user_operation:
    def connection(self):
        db = mysql.connector.connect(host="localhost", port="3306", user="root", password="root",database="gym")
        return db

    def submit(self,name,email,password):
        con = self.connection()
        sq="insert into user (name,email,password) values(%s,%s,%s)"
        record = [name,email,password]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        con.commit()
        cursor.close()
        con.close()
        return

    def user_delete(self,email):
        con=self.connection()
        sq="delete from user where email=%s"
        record = [email]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        con.commit()
        cursor.close()
        con.close()
        return

    def user_login_verify(self,email,password):
        con=self.connection()
        cursor=con.cursor() 
        sq="select name,email from user where email=%s and password=%s"
        record = [email,password]
        cursor.execute(sq, record)
        row = cursor.fetchall()
        rc = cursor.rowcount
        rc = cursor.rowcount
        cursor.close()
        con.close()
        if rc == 0:
           return 0
        else:
           for r in row:
               session['user_name'] =   r[0]
               session['user_email'] = r[1]  
           return 1

    def update_password(self, email, password):
        con=self.connection()
        cursor = con.cursor()
        sq = "UPDATE users SET password = %s WHERE email = %s"
        cursor.execute(sq, (password, email))
        connection.commit()
        cursor.close()
        connection.close()


    def member_insert(self,member_id,plan_name,address,charges,phone_no,start_date,end_date):
        con=self.connection()
        cursor=con.cursor()
        sq="insert into membership(user_email,member_id,plan_name,address,charges,phone_no,start_date,end_date) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        record=[session['user_email'],member_id,plan_name,address,charges,phone_no,start_date,end_date]
        cursor.execute(sq,record)
        con.commit()
        cursor.close()
        con.close()
        return
    
    def member_list(self):
       con=self.connection() 
       cursor = con.cursor(dictionary=True)  # Use dictionary=True for easy mapping
       query = """
       SELECT m.member_id, m.plan_name, m.address, m.charges, m.phone_no, m.start_date, m.end_date, u.name AS user_name
       FROM membership m
       JOIN user u ON m.user_email = u.email;
       """
       cursor.execute(query)
       result = cursor.fetchall()
       print(result)  # Debugging print
       con.close()
       return result




    def user_profile(self):
        con=self.connection()
        sq="select name,email from user where email=%s"
        record = [session['user_email']]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        row = cursor.fetchall()
        cursor.close()
        con.close()
        return row

    def user_profile_edit(self,name,mobile):
        con=self.connection()
        sq="update user set name=%s where email=%s"
        record = [name,session['user_email']]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        con.commit()
        cursor.close()
        con.close()
        return



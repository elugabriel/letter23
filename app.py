from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import UserForm
import os
import sqlite3
from fpdf import FPDF
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from flask.helpers import send_file
import io



app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xyquyxnylikmbf:7b924cb1a6826770fe08ed6ab94bda8c524ce2555c25bf6e76a9842d9686078b@ec2-18-209-78-11.compute-1.amazonaws.com:5432/d2n1pvtk1v6rek'

db = SQLAlchemy(app)


class printed(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    matric_no = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String(300), unique=False, nullable=False)
    date_printed = db.Column(db.String(50), unique=False, nullable=False)
    

    def __repr__(self):
        return f"User('{self.ID_number}', '{self.first_name}', '{self.last_name}')"

def connection():
    try:
        conn = sqlite3.connect("student.db")
    except:
        print("cannot connect to the database")
    return conn




@app.route("/")
@app.route("/home")
def index():
    #return render_template('home.html')
    return render_template('index.html')

@app.route("/register", methods=['POST', 'GET'])
def register():
        conn = sqlite3.connect('student.db')
        cursor = conn.cursor()

        username = request.form.get("username")
        password = request.form.get("password")
        
        cursor.execute("""INSERT INTO User(username, password)  VALUES (?,?)""",
                   (username, password))
        conn.commit()
        flash(f'{username} successfully created!', 'success')
        return render_template('register.html', title='Register')
"""
        conn = connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO User values (?,?)",
                        (username, password))
        flash(f'{username} successfully created!', 'success')
        
        
        return render_template('register.html', username=username, password=password)
"""
@app.route("/home", methods=['POST', 'GET'])
def home():
    username = request.form.get("username")
    password = request.form.get("password")

    print(username, password)

    if username == "ADMIN" and password =="ADMIN":
            return render_template("admin.html")


    

    if request.method == 'POST':
        connection = sqlite3.connect('student.db')
        cursor = connection.cursor()
        

        query = "SELECT username,password FROM User where username='"+username+"' and password='"+password+"'"
        cursor.execute(query)
        results = cursor.fetchall()
        

        if len(results) ==0:
            return render_template("error.html")
  
        else:
            return render_template("user.html")
    #return render_template('index.html')


@app.route("/letter", methods=['GET', 'POST'])
def letter():
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    number = request.form.get("number")
    session = request.form.get("session")
    start_date = request.form.get("start_date")
    cursor.execute("SELECT  * FROM student_details WHERE MATRICNO =?",(number, ))
    results = cursor.fetchall()

    for result in results:
            matric_no =  result[0]
            jamb_no = result[1]
            id_no =  result[2]
            full_name = result[3]
            course = result[4]
            state = result[5]
            fname_1 = full_name
            date =start_date
            now = datetime.now()
            date_printed =now.strftime("%d/%m/%Y %H:%M:%S")
           




            file_name  = fname_1
            title = " "
            text1 = " "
            text2 = " ................."
            text3=  " ................."
            text4 = "OFFER OF PROVISIONAL ADMISSION INTO N.C.E PROGRAMME FOR "
            text5 =session + " SESSION"
            text6 = "I am pleased to inform you that you have been offered Provisional Admission to Study "
            text7 = " "  + course +"."
            text8 = "The admission is subjected to your:"
            text9 =  "  1. Obtaining the minimum/general and Departmental entry requirement as prescribe in the "
            text10 = "     JAMB Brochure"
            text11 = "  2. Ability to submit original of your credentials "
            text12 = "  3. Submitting evidence of Medical fitness on the prescribed form FCOB"
            text13 = "  4. Ability to pay approved fees as attached"
            text14 = "  5. Other fees"
            text15=  "          i.  Accommodation is available for year 1 in main Campus and Bebi Campus"
            text16 = "          ii. Acculturation and Excursion fees are to be determined by the relevant departments"
         
            text17 = "  6. you are also expected to adhere strictly to the college dress code and the regulations"
            text18 ="       contained in the Students' Handbook"
            text19 ="The Session for new students begins on  "+start_date + ",  you are expected to resume on that date "
            text20 ="and go through registration and orientation exercise before the commencement of lectures "
            text21 =" "
            text22 ="Late registration will attract a late registration fee. "
            text23 =" "
            text24 ="Congratulations"
            text25 =" "
            text26 =" "
            text27 =" Grace A. Undie(Mrs)"
            text28 =" Registral/Secretary to Council"
            text29= "Ref........................"
            text30= "Date......................."


            
            from reportlab.pdfgen import canvas
            pdf = canvas.Canvas(file_name, pagesize=A4)
            pdf.setTitle(title)

            pdf.setFont('Helvetica-Bold', 16)
            pdf.drawCentredString(270, 770, title)

            img_file1 = 'signature.png'
            img_file2 = 'stamp.png'
            img_file3 = 'head111.png'
            img_file4 = 'header2.png'


          

            x_start = 400
            y_start = 160
            pdf.drawImage(img_file1, x_start, y_start, width=100, preserveAspectRatio=True, mask='auto')
            pdf.drawImage(img_file2, x_start, 70, width=100, preserveAspectRatio=True, mask='auto')

            x_start = 65
            y_start = 720
            pdf.drawImage(img_file3, x_start, y_start, width=500, preserveAspectRatio=True, mask='auto')
            
           

            

            #text = pdf.beginText(40, 680)
            #text.setFont('Courier', 14)

            #for line in textLines:
                #text.textLine(textLines)

            #pdf.drawText(text)

            pdf.setFont('Helvetica', 12)
            pdf.drawString(40, 720, text1)
            pdf.drawString(50, 720, text2)
            pdf.drawString(50, 700, text3)
            pdf.drawString(40, 560, text9)
            pdf.drawString(400, 720, text29)
            pdf.drawString(400, 700, text30)

            pdf.setFont('Helvetica-Bold', 14)
            pdf.drawString(40, 660, text4)
            pdf.drawString(250, 640, text5)
            pdf.drawString(40, 540, text10)
            pdf.drawString(40, 460, text14)

            pdf.setFont('Helvetica', 12)
            
            pdf.drawString(40, 620, text6)
            pdf.drawString(40, 600, text7)
            pdf.drawString(40, 580, text8)
            
            
            pdf.drawString(40, 520, text11)
            pdf.drawString(40, 500, text12)

            pdf.drawString(40, 480, text13)
            
            pdf.drawString(40, 440, text15)
            pdf.drawString(40, 420, text16)

            pdf.drawString(40, 400, text17)
            pdf.drawString(40, 380, text18)
            pdf.drawString(40, 360, text19)
            pdf.drawString(40, 340, text20)
            pdf.drawString(40, 320, text21)
            pdf.drawString(40, 300, text22)
            pdf.drawString(40, 280, text23)
            pdf.drawString(40, 260, text24)
            pdf.drawString(40, 240, text25)
            pdf.drawString(40, 220, text26)
            pdf.drawString(380, 200, text27)
            pdf.drawString(380, 180, text28)


            pdf.save()
            

            cursor.execute("""INSERT INTO printed(matric_no, full_name, date_printed)  VALUES (?,?,?)""",
                   (matric_no, full_name, date_printed))

            conn.commit()
            conn.close
            
            p = fname_1 

            return send_file(p, as_attachment=True)




    return render_template('letter.html')
       
       

@app.route("/user_letter", methods=['GET', 'POST'])
def user_letter():
    #file_name  = fname_1 + " " + "admission_letter.pdf"
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    number = request.form.get("number")
    session = request.form.get("session")
    start_date = request.form.get("start_date")
    cursor.execute("SELECT  * FROM student_details WHERE MATRICNO =?",(number, ))
    results = cursor.fetchall()

    for result in results:
            matric_no =  result[0]
            jamb_no = result[1]
            id_no =  result[2]
            full_name = result[3]
            course = result[4]
            state = result[5]
            fname_1 = full_name
            date =start_date
            now = datetime.now()
            date_printed =now.strftime("%d/%m/%Y %H:%M:%S")
           




            file_name  = fname_1
            title = " "
            text1 = " "
            text2 = " ................."
            text3=  " ................."
            text4 = "OFFER OF PROVISIONAL ADMISSION INTO N.C.E PROGRAMME FOR "
            text5 =session + " SESSION"
            text6 = "I am pleased to inform you that you have been offered Provisional Admission to Study "
            text7 = " "  + course +"."
            text8 = "The admission is subjected to your:"
            text9 =  "  1. Obtaining the minimum/general and Departmental entry requirement as prescribe in the "
            text10 = "     JAMB Brochure"
            text11 = "  2. Ability to submit original of your credentials "
            text12 = "  3. Submitting evidence of Medical fitness on the prescribed form FCOB"
            text13 = "  4. Ability to pay approved fees as attached"
            text14 = "  5. Other fees"
            text15=  "          i.  Accommodation is available for year 1 in main Campus and Bebi Campus"
            text16 = "          ii. Acculturation and Excursion fees are to be determined by the relevant departments"
         
            text17 = "  6. you are also expected to adhere strictly to the college dress code and the regulations"
            text18 ="       contained in the Students' Handbook"
            text19 ="The Session for new students begins on  "+start_date + ",  you are expected to resume on that date "
            text20 ="and go through registration and orientation exercise before the commencement of lectures "
            text21 =" "
            text22 ="Late registration will attract a late registration fee. "
            text23 =" "
            text24 ="Congratulations"
            text25 =" "
            text26 =" "
            text27 =" Grace A. Undie(Mrs)"
            text28 =" Registral/Secretary to Council"
            text29= "Ref........................"
            text30= "Date......................."


            
            from reportlab.pdfgen import canvas
            pdf = canvas.Canvas(file_name, pagesize=A4)
            pdf.setTitle(title)

            pdf.setFont('Helvetica-Bold', 16)
            pdf.drawCentredString(270, 770, title)

            img_file1 = 'signature.png'
            img_file2 = 'stamp.png'
            img_file3 = 'head111.png'
            img_file4 = 'header2.png'


          

            x_start = 400
            y_start = 160
            pdf.drawImage(img_file1, x_start, y_start, width=100, preserveAspectRatio=True, mask='auto')
            pdf.drawImage(img_file2, x_start, 70, width=100, preserveAspectRatio=True, mask='auto')

            x_start = 65
            y_start = 720
            pdf.drawImage(img_file3, x_start, y_start, width=500, preserveAspectRatio=True, mask='auto')
            
           

            

            #text = pdf.beginText(40, 680)
            #text.setFont('Courier', 14)

            #for line in textLines:
                #text.textLine(textLines)

            #pdf.drawText(text)

            pdf.setFont('Helvetica', 12)
            pdf.drawString(40, 720, text1)
            pdf.drawString(50, 720, text2)
            pdf.drawString(50, 700, text3)
            pdf.drawString(40, 560, text9)
            pdf.drawString(400, 720, text29)
            pdf.drawString(400, 700, text30)

            pdf.setFont('Helvetica-Bold', 14)
            pdf.drawString(40, 660, text4)
            pdf.drawString(250, 640, text5)
            pdf.drawString(40, 540, text10)
            pdf.drawString(40, 460, text14)

            pdf.setFont('Helvetica', 12)
            
            pdf.drawString(40, 620, text6)
            pdf.drawString(40, 600, text7)
            pdf.drawString(40, 580, text8)
            
            
            pdf.drawString(40, 520, text11)
            pdf.drawString(40, 500, text12)

            pdf.drawString(40, 480, text13)
            
            pdf.drawString(40, 440, text15)
            pdf.drawString(40, 420, text16)

            pdf.drawString(40, 400, text17)
            pdf.drawString(40, 380, text18)
            pdf.drawString(40, 360, text19)
            pdf.drawString(40, 340, text20)
            pdf.drawString(40, 320, text21)
            pdf.drawString(40, 300, text22)
            pdf.drawString(40, 280, text23)
            pdf.drawString(40, 260, text24)
            pdf.drawString(40, 240, text25)
            pdf.drawString(40, 220, text26)
            pdf.drawString(380, 200, text27)
            pdf.drawString(380, 180, text28)


            pdf.save()
            

            cursor.execute("""INSERT INTO printed(matric_no, full_name, date_printed)  VALUES (?,?,?)""",
                   (matric_no, full_name, date_printed))

            conn.commit()
            conn.close
            #buf_str = io.StringIO(file_name)
            #buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))

            #return send_file (io.BytesIO(buf_str.read().encode("utf-8")), mimetype='application/pdf', download_name="letter.pdf" )
            p = fname_1 

            return send_file(p, as_attachment=True)

            
    return render_template('user_letter.html')
       
@app.route("/printed", methods=['GET', 'POST'])
def printed():
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute("SELECT  * FROM printed")
    results = cursor.fetchall()
    """
    for result in results:
            matric_no =  result[1]
            full_name = result[1]
            id_no =  result[2]
            full_name = result[3]
            course = result[4]
            state = result[5]
            """
    conn.commit()
    conn.close

    return render_template('printed.html', results = results)


if __name__ == '__main__':
    app.run(debug=True)

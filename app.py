from flask import Flask,render_template,url_for,request
import pandas as pd
from email.message import EmailMessage
import ssl
import smtplib
import extraq as ex
import datetime as dt


app=Flask(__name__)


def email():
    sender_email=ex.sender_email
    sender_pass=ex.sender_pass
    u_email=ex.receiver_email
    u_subject=ex.subject
    u_message=ex.message

    em=EmailMessage()
    em['From']=sender_email
    em['To']=u_email
    em['subject']=u_subject
    em.set_content(u_message)

    context=ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(sender_email,sender_pass)
        smtp.sendmail(sender_email,u_email,em.as_string())

    file=open("Records.txt","a")
    timee=dt.datetime.now()
    data="##Sent"+"\t"+str(timee)+"\n\n"+"Sender email= "+sender_email+"\n"+"Receiver email="+u_email+"\n\n\n\n\n"
    file.write(data)
    file.close()    



@app.route('/')
def home():
    
    return render_template('home.html')


@app.route('/user_inputs',methods=['GET','POST'])
def user_inputs():
    if request.method=='POST':
        ex.sender_email=request.form['Sender_Email']
        ex.sender_pass=request.form['Sender_Pass']
        ex.receiver_email=request.form['Email_id']
        ex.subject=request.form['Subject']
        ex.message=request.form['Message']
        user_id={"Email":[ex.receiver_email],"Subject":[ex.subject],"Message":[ex.message]}
        email()
        return user_id

if __name__==("__main__"):
    app.run(debug=True)

    
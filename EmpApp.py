from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
import openai
from config import *

app = Flask(__name__)

# bucket = custombucket
region = customregion
db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb
)
output = {}

table = 'employee'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route("/about", methods=['POST'])
def about():
    return render_template('www.intellipaat.com')


@app.route("/index", methods=['POST'])
def index():
    name = request.form['name']
    interest = request.form['interest']
    eventname = request.form['event_name']
    duration = request.form['duration']
    venue = request.form['venue']
    date = request.form['date']
    key1 = "sk-1ZSF8C"
    key2 = "tk7qlQEb"
    key3 = "5r12r9T3"
    key4 = "BlbkFJf"
    key5 = "vcTwqZVyL"
    key6 = "XDe0qhPJGf"
    key = key1+key2+key3+key4+key5+key6
    # emp_image_file = request.files['emp_image_file']

    # AI module
    # stext = "Name: "+name + "\nInterest: "+interest + "\nEvent_Name: "+eventname + "\nDuration: "+duration + "\nVenue: "+venue +"\nDate: "+date +"\n\nOutput: "
    stext ="Generate a mail to "+name+" inviting him to a "+duration+", "+interest+" Hackathon conducted by "+venue+" on "+date+". Subject of the email should be "+eventname+"."
    openai.api_key = key
    response = openai.Completion.create( 
        engine = "text-davinci-003",
        prompt=stext,
        temperature=0.1, # how deterministic should your response be, so higher the temp:lower precise it is
        max_tokens=128,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    content = response.choices[0].text.split('.')
    k =  response.choices[0].text

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s,%s,%s)"
    cursor = db_conn.cursor()

    # if emp_image_file.filename == "":
    #     return "Please select a file"

    try:

        cursor.execute(insert_sql, (name, interest, eventname, duration, venue, date, k))
        db_conn.commit()
        content = k

        # # Uplaod image file in S3 #
        # emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        # s3 = boto3.resource('s3')

        # try:
        #     print("Data inserted in MySQL RDS... uploading image to S3...")
        #     s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
        #     bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
        #     s3_location = (bucket_location['LocationConstraint'])

        #     if s3_location is None:
        #         s3_location = ''
        #     else:
        #         s3_location = '-' + s3_location

        #     object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
        #         s3_location,
        #         custombucket,
        #         emp_image_file_name_in_s3)

        # except Exception as e:
        #     return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('output.html', content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
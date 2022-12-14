from flask import Flask, render_template, request, redirect
import yaml
import mysql.connector

app = Flask(__name__)

# configuration of the DB
db_details = yaml.full_load(open("res/db_details.yaml"))
app.config['MYSQL_HOST'] = db_details['mysql_host']
app.config['MYSQL_USER'] = db_details['mysql_user']
app.config['MYSQL_PORT'] = db_details['mysql_port']
app.config['MYSQL_PASSWORD'] = db_details['mysql_password']
app.config['MYSQL_DB'] = db_details['mysql_db']


# this is an endpoint (/)
@app.route('/', methods=['GET', 'POST'])
# Here we say that this can be a GET or a POST request. If this is a GET request, return the render_template()
# To check whether this is get or post, we can use "request"
def index():
    myCursor = myDB.cursor()

    if request.method == "POST":
        userDetails = request.form
        name = userDetails['name_input']
        email = userDetails['email_input']

        myCursor.execute("INSERT INTO users(name, email) VALUES(%s, %s)", (name, email))
        myDB.commit()

        # this can be used to redirect to another page
        return redirect('/users')

    # here we can simply return the HTML code to the web page as a string
    # return "<font color=red>Hi, returning flask</font>"

    # otherwise, we can render a HTML file to string like below
    # the HTML file to be rendered. This should be located in a folder called "templates" from the root of the project
    return render_template('index.html')


# end point for showing user details. Here this can be done by GET
@app.route('/users')
def users():
    myCursor = myDB.cursor()
    myCursor.execute("SELECT * FROM users")
    userDetails = myCursor.fetchall()
    return render_template('users.html', userDetails=userDetails)


def creatingTables(myDB):
    with open("res/sqlFiles/creatingTablesSqlQueriesTXT.txt", 'r') as creatingTablesSqlQueriesTXTFile:
        queryCreatingTables = creatingTablesSqlQueriesTXTFile.read()
    myCursor = myDB.cursor()
    print(queryCreatingTables)
    try:
        myCursor.execute(queryCreatingTables, multi=True)
        print("Tables Successfully Created")
    except Exception as e:
        print("Exception Occurred")
        print(e)
    myCursor.close()

    # myCursor2 = myDB.cursor()
    # print("\n\nCreated Tables List\n")
    # myCursor2.execute("SHOW TABLES;")
    # createdTablesList = myCursor2.fetchall()
    # for table in createdTablesList:
    #     print(table)


if __name__ == '__main__':
    myDB = mysql.connector.connect(host=db_details['mysql_host'], user=db_details['mysql_user'],
                                   port=db_details['mysql_port'], database=db_details['mysql_db'],
                                   password=db_details['mysql_password'])

    # creating tables
    creatingTables(myDB)


    # when debug is true, as soon as the python file is saved while the server is running, the webpage changes.
    # app.run(debug=False)

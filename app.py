from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Configure MySQL connection
db_config = {
    'host': 'suranardsdemo.cdtqd6jgia7i.ap-south-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'test1234',
    'database': 'mysqldemo'
}


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/students')
def view_customers():
    print("view customers")
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM students")
            customer = cursor.fetchall()
            for customer in customer:
                print(customer[0], customer[1], customer[2], customer[3],customer[4],customer[5])
    finally:
        connection.close()
    return render_template('view_customers.html', customer=customer)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        Contact_Number = request.form['Contact_Number']  
        Section=request.form['Section']
        College=request.form['College']     


        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO students (name, email, phone) VALUES (%s, %s, %s,%s,%s)"
                cursor.execute(sql, (name, email, Contact_Number,Section,College))
            connection.commit()
        finally:
            connection.close()

        return redirect(url_for('view_customers'))
    return render_template('add_customer.html')

@app.route('/edit_customer/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    print("edit customer::",id)

    
    connection = pymysql.connect(**db_config)

    if request.method == 'GET':
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM customersstudents WHERE id=%s", (id,))
            customer = cursor.fetchone()
            print("customer::",customer)
        return render_template('edit_customer.html', customer=customer)
    try:
        with connection.cursor() as cursor:
            if request.method == 'POST':
                name = request.form['name']
                email = request.form['email']
                Contact_Number = request.form['Contact_Number']  
                Section=request.form['Section']
                College=request.form['College']

                sql = "UPDATE students SET name=%s, email=%s, Contact_Number=%s  Section=%s College=%s WHERE id=%s"
                cursor.execute(sql, (name, email, Contact_Number,Section,College, id))
                connection.commit()
                return redirect(url_for('view_customers'))
            else:
                cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
                customer = cursor.fetchone()
                print("customer::",customer)
    finally:
        connection.close()
    return render_template('edit_customer.html', customer=customer)
    

@app.route('/delete_customer/<int:id>', methods=['GET','POST'])
def delete_customer(id):
    print("delete student::",id)
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM student WHERE id=%s", (id,))
            connection.commit()
    finally:
        connection.close()
    return redirect(url_for('view_customers'))

if __name__ == '__main__':
    app.run(debug=True)
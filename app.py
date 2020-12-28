from flask import Flask,render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
app=Flask(__name__)

# Configure DB
db= yaml.load(open('db.yaml'))
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']
user_table_name= db['user_table_name']
package_table_name= db['package_table_name']
enquiry_table_name= db['enquiry_table_name']
employee_table_name= db['employee_table_name']
booking_table_name= db['booking_table_name']
mysql= MySQL(app)


# Webpages for different functions:
#     1.View all packages: http://localhost:5000/all_packages
#     2.Add package: http://localhost:5000/add_pack
#     3.Remove package: http://localhost:5000/rem_pack
#     4.View all users: http://localhost:5000/all_users
#     5.View all bookings: http://localhost:5000/all_bookings
#     6.View all enquiries: http://localhost:5000/all_enquiries
#     7.View all employees: http://localhost:5000/all_employees
#     8.All employee: http://localhost:5000/add_employee
#     9.Remove employee: http://localhost:5000/rem_employee
#     10. Update package cost: http://localhost:5000/update_pack

# About us
@app.route('/aboutus',methods=['GET','POST'])
def render_about():
    return render_template('aboutus.html')

# Homepage
@app.route('/home',methods=['GET','POST'])
def render_home():
    return render_template('homepage.html')

# Add package
@app.route('/add_pack',methods=['GET','POST'])
def add_package():
    if request.method=='POST':
        # Fetch Form Data
        package_= request.form
        p_name=package_["p_name"]
        p_id=int(package_["p_id"])
        days=int(package_['days'])
        destination=package_['destination']
        e_id=int(package_['e_id'])
        price=int(package_['price'])

        # Create cursor object to execute commands on MYSQL Server
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO "+package_table_name+" values(%s,%s,%s,%s,%s,%s)",(p_id,p_name,days,destination,e_id,price))
        except:
            return 'Package ID already exists'
        mysql.connection.commit()
        cur.close()
        return redirect('/all_packages')
    return render_template('Add_package.html')

# Remove package
@app.route('/rem_pack',methods=['POST'])
def remove_package():
    if request.method=='POST':
        # Fetch Form Data
        package_= request.form
        p_id_=package_["p_id"]

        # Create cursor object to execute commands on MYSQL Server
        cur = mysql.connection.cursor()
        cur.execute("Delete from "+package_table_name+" where p_id=(%s)",[p_id_])
        mysql.connection.commit()
        cur.close()
        return redirect('/all_packages')

# Update package cost
@app.route('/update_pack',methods=['GET','POST'])
def update_pack():
    if request.method=='POST':
        # Fetch Form Data
        package_= request.form
        p_id_=int(package_["p_id"])
        price=int(package_["price"])

        # Create cursor object to execute commands on MYSQL Server
        cur = mysql.connection.cursor()

        cur.execute("Update "+package_table_name+"\nset cost={0}\nwhere p_id={1}".format(price,p_id_))
        mysql.connection.commit()
        cur.close()
        return redirect('/all_packages')
    return render_template('Update_package.html')



# View all packages
@app.route('/all_packages')
def packages():
    cur = mysql.connection.cursor()
    result=cur.execute("SELECT * FROM "+package_table_name)
    if result>0:
        package_details=cur.fetchall()
        return render_template('packages.html',package_details=package_details)

# View all users
@app.route('/all_users')
def users():
    cur = mysql.connection.cursor()
    result=cur.execute("SELECT * FROM "+user_table_name)
    if result>0:
        user_details=cur.fetchall()
        return render_template('users.html',user_details=user_details)

# View all employees
@app.route('/all_employees')
def employees():
    cur = mysql.connection.cursor()
    result=cur.execute("SELECT * FROM "+employee_table_name)
    if result>0:
        employee_details=cur.fetchall()
        return render_template('employees.html',employee_details=employee_details)

# Add employee
@app.route('/add_employee',methods=['GET','POST'])
def add_employee():
    if request.method=='POST':
        # Fetch Form Data
        employee_= request.form

        e_name=employee_["e_name"]
        e_id=employee_["e_id"]
        dept=employee_['dept']
        role=employee_['role']

        # Create cursor object to execute commands on MYSQL Server
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO "+employee_table_name+" values(%s,%s,%s,%s)",(e_id,e_name,dept,role))
        except :
            return 'This Employee ID already exists'
        mysql.connection.commit()
        cur.close()
        return redirect('/all_employees')
    return render_template('Add_employee.html')

# Remove employee
@app.route('/rem_employee',methods=['GET','POST'])
def remove_employee():
    if request.method=='POST':
        # Fetch Form Data
        package_= request.form
        e_id_=package_["e_id"]

        # Create cursor object to execute commands on MYSQL Server
        cur = mysql.connection.cursor()
        cur.execute("Delete from "+employee_table_name+" where e_id=(%s)",[e_id_])
        mysql.connection.commit()
        cur.close()
        return redirect('/all_employees')

# View all bookings
@app.route('/all_bookings')
def bookings():
    cur = mysql.connection.cursor()
    result=cur.execute("SELECT * FROM "+booking_table_name)
    if result>0:
        booking_details=cur.fetchall()
        return render_template('bookings.html',booking_details=booking_details)

# View all enquiries
@app.route('/all_enquiries')
def enquiry():
    cur = mysql.connection.cursor()
    result=cur.execute("SELECT * FROM "+enquiry_table_name)
    if result>0:
        enquiry_details=cur.fetchall()
        return render_template('enquiries.html',enquiry_details=enquiry_details)



if __name__=='__main__':
    app.run(debug=True)
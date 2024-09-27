from flask import* 
# initialize application
import pymysql 
import sms
# connect to DB 
connection= pymysql.connect(host="localhost", user="root", password="", database="explore_kenya")
# create a cursor 
cursor= connection.cursor()

app= Flask(__name__)
app.secret_key="@123wgsfdhgdgdsjg"

#home route
@app.route("/index")
def index():
  connection.commit()
  return render_template("index.html")

#tourism route
@app.route("/tourism")
def tourism():
  # select from DB 
  sql1="SELECT*FROM sites where adventure_cartegory='wildlife'"
  sql2="SELECT*FROM sites where adventure_cartegory='historic_sites'"
  sql3="SELECT*FROM sites where adventure_cartegory='natural_features'"
  sql4="SELECT*FROM sites where adventure_cartegory='native_tribes_and_traditions'"

  # execute sql 
  cursor1=connection.cursor()
  cursor1.execute(sql1)
  cursor2=connection.cursor()
  cursor2.execute(sql2)
  cursor3=connection.cursor()
  cursor3.execute(sql3)
  cursor4=connection.cursor()
  cursor4.execute(sql4)
  
  # fetch rows 
  wildlife =cursor1.fetchall()
  historic_sites=cursor2.fetchall()
  natural_features=cursor3.fetchall()
  native_tribes_and_traditions=cursor4.fetchall()
  return render_template('tourism.html', wildlife=wildlife, historic_sites=historic_sites, natural_features=natural_features, native_tribes_and_traditions=native_tribes_and_traditions)

# Below we only need to use a POST, as posted in our Single item
@app.route('/mpesa', methods = ['POST'])
def mpesa():
    # Receive the amount and phone from single item
    phone = request.form['phone']
    amount = request.form['amount']
    # import mpesa.py module
    import mpesa
    # Call the SIM Toolkit(stk) push function present in mpesa.py
    mpesa.stk_push(phone, amount)
    # SHow user below message.
    return '<h3>Please Complete Payment in   Phone and we will deliver in minutes</h3>' \
    '<a href="/home" class="btn btn-dark btn-sm">Back to Products</a>'


#culture
@app.route("/culture")
def culture():
  connection.commit()
  return render_template("culture.html")

#education
@app.route("/education")
def education():
  connection.commit()
  return render_template("education.html")

#entertainment
@app.route("/entertainment")
def entertainment():
  connection.commit()
  return render_template("entertainment.html")
#politics
@app.route("/politics")
def politics():
  connection.commit()
  return render_template("politics.html")

#religion
@app.route("/religion")
def religion():
  connection.commit()
  return render_template("religion.html")

#sports
@app.route("/sports")
def sports():
  connection.commit()
  return render_template("sports.html")

#splash
@app.route("/splash")
def splash():
  connection.commit()
  return render_template("splash.html")


# upload route
@app.route("/upload", methods=["POST", "GET"])
def upload():
  if request.method =="POST":
    # upload here 
    subject=request.form["subject"]
    adventure_cartegory=request.form["adventure_cartegory"]
    subject_description=request.form["subject_description"]
    visit_cost=request.form["visit_cost"]
    season=request.form["season"]
    sites_image_name=request.files["sites_image_name"]
    sites_image_name.save("static/images/" + sites_image_name.filename)
    # our data 
    data=(subject, adventure_cartegory, subject_description, visit_cost, season, sites_image_name.filename)
    sql="INSERT INTO sites(subject, adventure_cartegory, subject_description, visit_cost, season, sites_image_name) values(%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, data)
    connection.commit()
    return render_template('upload.html', msg="upload successful") 
  else:
    return render_template("upload.html")
  
  
# singleitem route
@app.route("/singleitem/<tour_id>")  
def single(tour_id):
  # select from DB
  sql="SELECT* FROM sites where tour_id=%s"
  # execute sql
  cursor1=connection.cursor()
  cursor1.execute(sql,(tour_id))
  # fetch single product 
  site=cursor1.fetchone()
  return render_template("single.html", site=site)





# register
@app.route("/register", methods=["POST","GET"])
def register():
    if request.method=="GET":
      return render_template("register.html")
    else:
      username=request.form["username"]
      email=request.form["email"]
      phone=request.form["phone"]
      password1=request.form["password1"]
      password2=request.form["password2"]
      origin=request.form["origin"]
    if len(password1)<8:
      return  render_template("register.html", error="password must be atleast 8 characters")
    elif password1!=password2:
      return  render_template("register.html", error="passwords don't match")
    else:
      data=(username, email, phone, password1, origin)
      sql= "INSERT INTO members_kenya(username, email, phone, password, origin) values(%s, %s, %s, %s, %s)"
      cursor.execute(sql, data )
      connection.commit()
      sms.send_sms(phone, "thank you for registration to explore kenya we are looking forward to your arival into the magical kenya")
      return render_template("register.html", success="Registration successful")


#login
@app.route("/login", methods=["POST", "GET"])    
def login():
  if request.method=="GET":
    return render_template("login.html")
  else:
    username=request.form["username"]
    password=request.form["password"]
    
    

    sql="SELECT * FROM members_kenya WHERE username= %s and password=%s"
    cursor.execute(sql,(username, password))
    
    # check if user exist 
    if cursor.rowcount ==0:
      return render_template("login.html", error="invalid login credentials")
    else:
      session['key']=username
      return redirect("/index")
    
#mode
@app.route("/navbar", methods=["POST", "GET"])    
def navbar():
  if request.method=="GET":
    return render_template("navbar.html")
  else:
      username=request.form["username"]
      password=request.form["password"]
      phone=request.form["phone"]

    # check if user exist 
      if cursor.rowcount ==0:
       return render_template("navbar.html", error="invalid login credentials")
      else:
       session['key']=username
      sql="SELECT * FROM members_kenya WHERE username= %s and password=%s and phone=%s"
      cursor.execute(sql,(username, password, phone))
    
      connection.commit()

      sms.send_sms(phone, "thank you for trying to upload items please procede")
      return render_template("upload.html")
    
      

#logout
@app.route("/logout")
def logout():
  session.clear()
  return redirect("/login")


# tourists
@app.route('/tour_interest', methods=['POST', 'GET'])
def tour_interest():
 if request.method =="POST":
     firstname=request.form['firstname']
     lastname=request.form["lastname"]
     country=request.form["country"]
     password1=request.form["password1"]
     password2=request.form["password2"]
     phone=request.form["phone"]
     email=request.form['email']
     date=request.form["date"]
     if len(password1)<8:
          return  render_template("tour_interest.html", error="password must be atleast 8 characters")
     elif password1!=password2:
          return  render_template("tour_interest.html", error="passwords don't match")
     else:
      data=(firstname, lastname, country, phone, password1, email, date)
      sql= "insert into tourist_interest(firstname,lastname, country, phone, password, email, date ) values(%s, %s, %s, %s, %s, %s, %s)"
      cursor.execute(sql, data)
      connection.commit()
      sms.send_sms(phone,"thank you for registration")
      return render_template("tour_interest.html", success="Tourist Registration successful To Kenya. Send us a reminder when your are prepared to ensure your trip is smooth and enjoyable")


 else:
    return render_template("tour_interest.html")
    







if __name__ =="__main__":
#run application
  app.run(debug=True)

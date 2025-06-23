from flask import Flask , render_template , request , redirect ,session ,flash
import sqlite3
#.\venv\Scripts\Activate.ps1

# "Create a Flask web app called app, and tell Flask that this file is the main module, "
# "so it knows where to look for templates, static files, etc."

app = Flask(__name__)

@app.route("/") # index.html Home Page route
def home():
    if 'user' in session:
        return redirect('/dashboard')
    return render_template("index.html")

@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'POST':        #POST method:-check & transfer data if user submitted.. 
        name = request.form['name']     # retrieve user data &  store in DB
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db') #open or connect with DB
        c = conn.cursor()    #object which operate DB & execute Queries
        #prevent sql injection by using parameterized Query
        #Means it allows input as "Data" only instead of any "Sql Query"
        c.execute("INSERT INTO users(name, email, password) values (?, ?, ?)",
                  (name, email, password))
        conn.commit()
        conn.close()

        return redirect('/')
    
    return render_template("signup.html")  #GET method :- user can put their data 

app.secret_key = "secretkey123" #for session data access

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?",(email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = user[1] #user[1] = name
            #flash("Login Successfully !","success")
            return redirect('/dashboard')
        else:
            flash("Invalid Email or Password !","danger")
            return redirect('/login')
        
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html')

@app.route('/add_books',methods=['GET','POST'])
def add_books():
    if 'user' not in session: #when user request again after login then cookie checks user data if it is in session then same page
        return redirect('/login')
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        isbn = request.form['isbn']
        year = request.form['year']

        conn = sqlite3.connect('books.db')
        c = conn.cursor()
        c.execute('INSERT INTO books(title, author, genre, isbn, year) VALUES(?, ?, ?, ?, ?)',
                  (title, author, genre, isbn, year))
        conn.commit()
        conn.close()
        flash("Book Added Successfully!",'success')
        return redirect('/books')
    return render_template('add_books.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    # flash("Logged out Successfully!","info")
    return redirect('/')

@app.route('/books')
def book():
    if 'user' not in session:
        return redirect('/login')
    
    conn = sqlite3.connect('books.db')
    c = conn.cursor()

    q = request.args.get('search') # Receive String through URL

    if q:
        query = f"%{q}%"   # here %{string}% = word in any string 
        c.execute('''SELECT * FROM books WHERE
                  title LIKE ? OR
                  author LIKE ? OR
                  genre LIKE ? OR
                  isbn LIKE ? OR
                  year LIKE ? ''',
                  (query, query, query, query, query ))
    else:
        c.execute('SELECT * FROM books')
    book_data = c.fetchall()
    conn.close()
    return render_template('books.html', books = book_data) #books variable = stores book_data

@app.route('/edit_book/<int:id>', methods = ['GET','POST'])
def edit_book(id):
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        isbn = request.form['isbn']
        year = request.form['year']

        conn = sqlite3.connect('books.db')
        c = conn.cursor()
        c.execute('UPDATE books SET title=?, author=?, genre=?, isbn=?, year=? WHERE id=?',
                  (title, author, genre, isbn, year, id))
        conn.commit()
        conn.close()
        # flash("Book Updated Successfully!","success")
        return redirect('/books')
    else:
        conn = sqlite3.connect('books.db')
        c = conn.cursor()
        c.execute('SELECT * FROM books WHERE id=?',(id,))
        edit_book = c.fetchone() 
        conn.close()
        return render_template('edit_book.html',book = edit_book)

@app.route('/delete_book/<int:id>')
def delete_book(id):
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('DELETE FROM books WHERE id=?',(id,))
    conn.commit()
    conn.close()
    return redirect('/books')



if __name__ == '__main__':
    app.run(debug=True)



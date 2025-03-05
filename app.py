from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flask_todo' # Edit this to your database name
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_todo' # Edit this to your database name

mysql = MySQL(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo(title=title, description=description)

        try:
            db.session.add(todo)
            db.session.commit()
            return redirect('/')
        except:
            return 'An error has occured'

    else:
        items = Todo.query.order_by(Todo.created_at).all()
        return render_template('index.html', items=items)

@app.route("/delete/<int:id>")
def delete(id):
    item = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(item)
        db.session.commit()
        return redirect('/')
    except:
        return 'An error has occured'

@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    item = Todo.query.get_or_404(id)
    if request.method == 'POST':
        item.title = request.form['title']
        item.description = request.form['description']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'An error has occured'
    else:
        return render_template('update.html', item=item)

if __name__ == "__main__":
    app.run(debug=True)
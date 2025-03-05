After cloning, do

`py -3 -m venv .venv`
`.venv/Scripts/activate`

After that, do

`pip install flask flask-mysqldb flask-sqlalchemy flask-migrate`

And then make your own database in MySQL

And then configure your database in app.py

After that, do

`flask db init`
`flask db migrate -m "Initial migration"`
`flask db upgrade`

And then

flask run

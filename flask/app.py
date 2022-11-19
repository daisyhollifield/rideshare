from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

# one or the other of these. Defaults to MySQL (PyMySQL)
# change comment characters to switch to SQLite


import cs304dbi as dbi
dbi.conf('rideshare_db')
# import cs304dbi_sqlite3 as dbi
import queue_functions as qf
import crud_functions as cf
import random

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def index():
    conn = dbi.connect()
    posts = qf.get_posts_with_user_names(conn)
    return render_template('main.html',title='Main Page', posts = posts)



@app.route('/myposts/', methods =['GET'])
def showmy():
    return render_template("myposts.html")

@app.route('/createpost/', methods =['GET', 'POST'])
def insert():
    if request.method == 'GET':
        return render_template("insert.html")

    else: 
        conn = dbi.connect()
        username = request.form['post-username']
        type = request.form['post-type']
        time = request.form['post-time']
        title = request.form['post-title']
        seats = request.form['post-seats']
        special_request = request.form['post-specials']
        if special_request == "":
            special_request = None
        display_now = True
        cost = request.form['post-cost']
        destination = ""
        destination += request.form['post-address-name']
        destination += ", "
        destination += request.form['post-address-street']
        destination += ", "
        destination += request.form['post-address-city']
        destination += ", "
        destination += request.form['post-address-state']
        destination += ", "
        destination += request.form['post-address-zipcode']
        cf.insertpost(conn, username, type, destination, time, title, seats, special_request, display_now, cost)
        return redirect( url_for('index') )
        #eventually will do this and maybe flash something? 
        #return redirect(url_for('MYPOSTS', nnn=request.form['movie-tt'])) 



@app.before_first_request
def init_db():
    dbi.cache_cnf()
    # set this local variable to 'wmdb' or your personal or team db
    db_to_use = 'rideshare_db' 
    dbi.use(db_to_use)
    print('will connect to {}'.format(db_to_use))

if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)

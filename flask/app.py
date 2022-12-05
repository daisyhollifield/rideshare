'''Flask/PyMySQL app to post ride request and offers in the rideshare_db. 

Daisy, Lindsay, and Valerie. 
Fall 2022
'''
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

# for CAS
from flask_cas import CAS

CAS(app)

app.config['CAS_SERVER'] = 'https://login.wellesley.edu:443'
app.config['CAS_LOGIN_ROUTE'] = '/module.php/casserver/cas.php/login'
app.config['CAS_LOGOUT_ROUTE'] = '/module.php/casserver/cas.php/logout'
app.config['CAS_VALIDATE_ROUTE'] = '/module.php/casserver/serviceValidate.php'
app.config['CAS_AFTER_LOGIN'] = 'logged_in'
# the following doesn't work :-(
app.config['CAS_AFTER_LOGOUT'] = 'after_logout'



app.config['UPLOADS'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1*1024*1024 # 1 MB

@app.route('/')
def index():
    '''Home page has a nav bar and shows all posts in the database. Has front end for
    login in box and query spot but not yet implemented.'''
    if 'CAS_USERNAME' not in session:
        return redirect(url_for('applogin'))
    else:
        is_logged_in = True
        username = session['CAS_USERNAME']
        conn = dbi.connect()
        posts = qf.get_posts_with_usernames(conn)
        users = qf.get_all_users(conn)
        states = qf.get_all_states(conn)
        return render_template('main.html',title='Main Page', posts = posts, users=users, states=states, username=username, is_logged_in=is_logged_in)
    
@app.route('/applogin/')
def applogin():
    if 'CAS_USERNAME' in session:
        return redirect( url_for('index') )
    else:
        return render_template('login.html')

@app.route('/logged_in/')
def logged_in():
    conn = dbi.connect()
    if 'CAS_USERNAME' in session:
        username = session['CAS_USERNAME']
    if 'CAS_ATTRIBUTES' in session:
        attribs = session['CAS_ATTRIBUTES']
        first_name = attribs['cas:givenName']
        last_name = attribs['cas:sn']
        name_to_insert = first_name + " " + last_name
    #user already in table
    if qf.userExists(conn, username):
        return redirect( url_for('index') )
    #new user
    else:  
        cf.insertUser(conn, username, name_to_insert)
        return redirect(url_for('update_user', username = username))


@app.route('/updateprofile/', methods =['GET', 'POST'])
def update_user():
    if 'CAS_USERNAME' not in session:
        return redirect(url_for('applogin'))
    else:
        their_username = session['CAS_USERNAME']
        conn = dbi.connect()
        if request.method == 'GET':
            #blank complete profile form 
            #show them their current info!!!
            this_profile = qf.get_profile_info(conn, their_username)
            current_pn=this_profile['phone_number']
            current_cy=this_profile['class_year']
            current_mj=this_profile['major']
            current_ht=this_profile['hometown']
            current_pic = qf.getProfilePic(conn, their_username)
            return render_template("updateProfile.html", pic=current_pic, username = their_username, current_pn=current_pn, current_cy=current_cy, current_mj=current_mj, current_ht=current_ht)
        else: 
            #pre form info: 
            this_profile = qf.get_profile_info(conn, their_username)
            current_pn=this_profile['phone_number']
            current_cy=this_profile['class_year']
            current_mj=this_profile['major']
            current_ht=this_profile['hometown']
            current_pic = qf.getProfilePic(conn, their_username)
            #make variables from form data
            #figure out which varibles were filled out

            #add soemthing to check in file updload is empty
            phone_number = request.form['phone_number']
            pn_empty = (phone_number == "")
            if pn_empty:
                phone_number = current_pn
            class_year = request.form['class_year']
            cy_empty = (class_year == "")
            if cy_empty:
                class_year = current_cy
            major = request.form['major']
            mj_empty = (major == "")
            if mj_empty: 
                major = current_mj
            hometown = request.form['hometown']
            ht_empty = (hometown == "")
            if ht_empty: 
                hometown = current_ht
            cf.updateUser(conn, username=their_username, phone_number=phone_number, class_year=class_year, major=major, hometown=hometown)
            #file stuff
            file = request.files['pic']
            user_filename = file.filename
            if user_filename != '':
                ext = user_filename.split('.')[-1]
                filename = secure_filename('{}.{}'.format(their_username,ext))
                pathname = os.path.join(app.config['UPLOADS'],filename)
                file.save(pathname)
                cf.updateProfilePic(conn, their_username, filename)
            return redirect( url_for('profile', username = their_username))   


@app.route('/after_logout/')
def after_logout():
    return redirect( url_for('index') )


@app.route('/profile/<string:username>')
def profile(username):
    if 'CAS_USERNAME' not in session:
        return redirect(url_for('applogin'))
    else:
        conn = dbi.connect()
        user = qf.get_profile_info(conn, username)
        pic = qf.getProfilePic(conn, username)
        return render_template('profile.html', user = user, pic=pic)

@app.route('/pic/<username>')
def pic(username):
    if 'CAS_USERNAME' not in session:
        return redirect(url_for('applogin'))
    else:
        conn = dbi.connect()
        curs = dbi.dict_cursor(conn)
        numrows = curs.execute(
            '''select filename from Picfile where username = %s''',
            [username])
        if numrows == 0:
            flash('No picture for {}'.format(username))
            return redirect(url_for('index'))
        row = curs.fetchone()
        return send_from_directory(app.config['UPLOADS'],row['filename'])


@app.route('/myprofile/')
def myprofile():
    if 'CAS_USERNAME' not in session:
        return redirect(url_for('applogin'))
    else:
        username = session['CAS_USERNAME']
        return redirect( url_for('profile', username = username)) 

#need second backslash? 
@app.route('/result')
def result():
    if 'CAS_USERNAME' not in session:
        return redirect(url_for('applogin'))
    else: 
        conn = dbi.connect()
        destination = request.args.get('destination-name')
        street_address = request.args.get('street-address')
        city = request.args.get('city')
        state = request.args.get('menu-state') # doesn't completely work yet
        zipcode = request.args.get('zip') 
        user = request.args.get('menu-user') # doesn't completely work yet
        date = request.args.get('date')  # doesn't completely work yet 
        time = request.args.get('time')  # doesn't completely work yet
        seats = request.args.get('seats')
        cost = request.args.get('cost')
        users = qf.get_all_users(conn)
        states = qf.get_all_states(conn)
        posts = qf.get_result_posts(conn, destination, street_address, city, state, zipcode, user, date, time, seats, cost)
        return render_template('main.html',title='Main Page', posts = posts, users = users, states=states)

@app.route('/myposts/', methods =['GET'])
def showmy():
    '''My posts page has a nav bar and will eventually shows all posts in the database
    made by the logged in user but not yet implemented.'''
    if 'CAS_USERNAME' not in session:
        return redirect(url_for('applogin'))
    else:
        return render_template("myposts.html")

@app.route('/createpost/', methods =['GET', 'POST'])
def insert():
    '''An insert post page with a form to do just that. Redirects to home page after submit.'''
    if 'CAS_USERNAME' not in session:
        return redirect(url_for('applogin'))
    else:
        #blank form 
        if request.method == 'GET':
            return render_template("insert.html")
        #submit button was cliked
        else: 
            conn = dbi.connect()
            #gettting infor from form
            if 'CAS_USERNAME' in session:
                username = session['CAS_USERNAME']
            #username = request.form['post-username']
            type = request.form['post-type']
            date = request.form['post-date'].replace("-", "")
            time = request.form['post-time']
            title = request.form['post-title']
            seats = request.form['post-seats']
            special_request = request.form['post-specials']
            #special_request is optional so set it to None if left blank
            if special_request == "":
                special_request = None
            display_now = True
            cost = request.form['post-cost']
            destination = request.form['post-address-name']
            street_address = request.form['post-address-street']
            city = request.form['post-address-city']
            state = request.form['post-address-state']
            zipcode = request.form['post-address-zipcode']
            #insert the post
            cf.insertpost(conn, username, type, date, time, destination, street_address, city, state, zipcode, title, seats, special_request, display_now, cost)
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

application = app


if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        if not(1943 <= port <= 1952):
            print('For CAS, choose a port from 1943 to 1952')
            sys.exit()
        #may need to do back:::assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)

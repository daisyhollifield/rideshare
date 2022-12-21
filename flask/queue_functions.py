import cs304dbi as dbi

# ==========================================================
# The functions that do most of the queries and display of posting work.

def get_posts_with_usernames(conn, current_date):
    """ gets info about all posts and corresponding usernames for posts
    whose date is equal to or later than the current date"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''select * from Post inner join User using (username)
     where display_now = True and date >= %s order by date, time;''', [current_date])
    return curs.fetchall()

#Valerie add function here that is identical to the one above but adds a where username=username clause

def get_post_with_pid(conn, pid):
    curs = dbi.dict_cursor(conn)
    curs.execute('select * from Post where pid = %s', [pid])
    return curs.fetchone()

def get_profile_info(conn, username):
    """ gets profile info about a given username"""
    curs = dbi.dict_cursor(conn)
    curs.execute('select * from User where username = %s;', [username])
    return curs.fetchone()
    
def get_all_users(conn):
    """ returns a dictionary containing all of the users and their info 
    in the User table  """
    curs = dbi.dict_cursor(conn)
    curs.execute('select * from User order by username')
    return curs.fetchall()

def get_all_states(conn):
    """ returns a list containing all of the states with no repeats in the Post table where
    their display attribute is true and their date is equal to or later than the current date"""
    curs = dbi.cursor(conn)
    curs.execute('select `state` from Post where display_now = True group by state order by state')
    all_states = curs.fetchall()
    states = []
    for s in all_states:
        states.append(s[0])
    return states

def get_result_posts(conn, dct, current_date):
    """ returns a dictionary of posts that match the given inputed criteria """
    args_lst = [] # adds each search element that is non-empty to an argument list to get corresponding posts
    curs = dbi.dict_cursor(conn)
    if dct['destination-name'] == "":
        destination_string = ''
    else:
        destination_string = 'where destination = %s'
        args_lst.append(dct['destination-name'])
    if dct['street-address'] == "":
        street_address_string = ''
    else:
        if destination_string == "":
            street_address_string = 'where street_address = %s'
            args_lst.append(dct['street-address'])
        else:
            street_address_string = ' and street_address = %s' 
            args_lst.append(dct['street-address'])
    if dct['city'] == "":
        city_string = ""
    else:
        if destination_string == "" and street_address_string == "":
            city_string = 'where city = %s'
            args_lst.append(dct['city'])
        else:
            city_string = ' and city = %s'
            args_lst.append(dct['city'])
    if dct['menu-state'] == "none":
        state_string = ""
    else:
        if destination_string == "" and street_address_string == "" and city_string == "":
            state_string = 'where state = %s'
            args_lst.append(dct['menu-state'])
        else:
            state_string = ' and state = %s'
            args_lst.append(dct['menu-state'])
    
    if dct['zip'] == "":
        zipcode_string = ""
    else:
        if (destination_string == "" and street_address_string == "" and city_string == "" 
        and state_string == ""):
            zipcode_string = 'where zipcode = %s'
            args_lst.append(dct['zip'])
        else:
            zipcode_string = ' and zipcode = %s'
            args_lst.append(dct['zip'])
    if dct['menu-user'] == "none":
        user_string = ''
    else:
        if (destination_string == '' and street_address_string == "" and city_string == "" 
        and state_string == "" and zipcode_string == ""):
            user_string = 'where username = %s'
            args_lst.append(dct['menu-user'])
        else:
            user_string = ' and username = %s'
            args_lst.append(dct['menu-user'])

    if dct['date'] == "":
        if (destination_string == '' and street_address_string == "" and city_string == "" 
        and state_string == "" and zipcode_string == "" and user_string == ""):
            date_string = "where date >= %s"
            args_lst.append(current_date)
        else:
            date_string = " and date >= %s"
            args_lst.append(current_date)
    else:
        if (destination_string == '' and street_address_string == "" and city_string == "" 
        and state_string == "" and zipcode_string == "" and user_string == ""):
            date_string = 'where date = %s'
            args_lst.append(dct['date'])
        else:
            date_string = ' and date = %s'
            args_lst.append(dct['menu-user'])

    if dct['time'] == "":
        time_string = ""
    else:
        if (destination_string == '' and street_address_string == "" and city_string == "" 
        and state_string == "" and zipcode_string == "" and user_string == "" and date_string == ""):
            time_string = 'where time = %s'
            args_lst.append(dct['time'])
        else:
            time_string = ' and time = %s'
            args_lst.append(dct['time'])
    if dct['seats'] == '':
        seats_string = ''
    else:
        if (destination_string == '' and street_address_string == "" and city_string == "" 
        and state_string == "" and zipcode_string == "" and user_string == ''
         and date_string == '' and time_string == ''):
            seats_string = 'where seats = %s'
            args_lst.append(dct['seats'])
        else:
            seats_string = ' and seats = %s'
            args_lst.append(dct['seats'])
    
    if dct['cost'] == '':
        cost_string = ''
    else:
        if (destination_string == '' and street_address_string == "" and city_string== "" 
        and state_string == "" and zipcode_string == "" and user_string == '' and 
        date_string == "" and time_string == '' and seats_string == ''):
            cost_string = 'where cost = %s'
            args_lst.append(dct['cost'])
        else:
            cost_string = ' and cost = %s'
            args_lst.append(dct['cost'])
    if (destination_string == '' and street_address_string == "" and city_string== "" 
    and state_string == "" and zipcode_string == "" and user_string == '' 
    and date_string == "" and time_string == '' and seats_string == '' and cost_string == ''):
        display_now_string = 'where display_now = True'
    else:
        display_now_string = ' and display_now = True'
    curs.execute('select * from Post inner join User using (username) ' 
    + destination_string + street_address_string + city_string + state_string + 
    zipcode_string + user_string + date_string + time_string + seats_string + 
    cost_string + display_now_string + ' order by date, time;', args_lst)
    return curs.fetchall()


def get_post_comments(conn, pid):
    """ returns a dictionary of all the comments for a given post """
    curs = dbi.dict_cursor(conn)
    curs.execute('select cid, username, pid, content, time from Comment where pid = %s;', [pid])
    return curs.fetchall()


def userExists (conn, username):
    """ returns a boolean to see whether the user exists in the User table """
    curs = dbi.dict_cursor(conn)
    curs.execute('select username, name, phone_number, major, hometown from User where username = %s;', [username])
    return (curs.fetchone() != None)


def getProfilePic(conn, username):   
    """ returns a dictionary containing the information in the Picfile table for 
    a given username """
    curs = dbi.dict_cursor(conn)
    curs.execute(
        '''select username, filename from Picfile where username = %s''',
        [username])
    return curs.fetchone()

def get_post_info(conn, post_id):
    """ returns a dictionary containing the information in the Post table for 
    a given post """
    curs = dbi.dict_cursor(conn)
    curs.execute(
        '''select pid, username, type, destination, street_address, city, state, 
        zipcode, date, time, title, seats, special_request, display_now, cost 
        from Post where pid = %s''',
        [post_id])
    return curs.fetchone()

def get_posts_by_username(conn, username):
    """ gets info about all posts for posts
    by a certain user"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''select * from Post where username = %s;''', [username])
    return curs.fetchall()

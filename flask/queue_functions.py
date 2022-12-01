import cs304dbi as dbi


# ==========================================================
# The functions that do most of the queue and display of posting work.



dbi.conf('rideshare_db')

def get_posts_with_usernames(conn):
    """ gets info about all posts and corresponding usernames """
    curs = dbi.dict_cursor(conn)
    curs.execute('select * from Post inner join User using (username) where display_now = True order by date, time;')
    return curs.fetchall()

def get_profile_info(conn, username):
    """ gets profile info about a given username"""
    curs = dbi.dict_cursor(conn)
    curs.execute('select * from User where username = %s;', [username])
    return curs.fetchone()
    
def get_all_users(conn):
    curs = dbi.dict_cursor(conn)
    curs.execute('select * from User order by username')
    return curs.fetchall()

def get_all_states(conn):
    curs = dbi.dict_cursor(conn)
    curs.execute('select `state` from Post')
    all_states = curs.fetchall()
    states = []
    for s in all_states:
        s_name = s['state']
        if s_name not in states:
            states.append(s_name)
    return sorted(states)

def get_result_posts(conn, destination, street_address, city, state, zipcode, user, date, time, seats, cost):
    args_lst = []
    curs = dbi.dict_cursor(conn)
    if destination == "":
        destination_string = ''
    else:
        destination_string = 'where destination = %s'
        args_lst.append(destination)

    if street_address == "":
        street_address_string = ''
    else:
        if destination_string == "":
            street_address_string = 'where street_address = %s'
            args_lst.append(street_address)
        else:
            street_address_string = ' and street_address = %s' 
            args_lst.append(street_address)
    if city == "":
        city_string = ""
    else:
        if destination_string == "" and street_address_string == "":
            city_string = 'where city = %s'
            args_lst.append(city)
        else:
            city_string = ' and city = %s'
            args_lst.append(city)
    if state == "none":
        state_string = ""
    else:
        if destination_string == "" and street_address_string == "" and city_string == "":
            state_string = 'where state = %s'
            args_lst.append(state)
        else:
            state_string = ' and state = %s'
            args_lst.append(state)
    
    if zipcode == "":
        zipcode_string = ""
    else:
        if destination_string == "" and street_address_string == "" and city_string == "" and state_string == "":
            zipcode_string = 'where zipcode = %s'
            args_lst.append(zipcode)
        else:
            zipcode_string = ' and zipcode = %s'
            args_lst.append(zipcode)
    if user == "none":
        user_string = ''
    else:
        if destination_string == '' and street_address_string == "" and city_string == "" and state_string == "" and zipcode_string == "":
            user_string = 'where username = %s'
            args_lst.append(user)
        else:
            user_string = ' and username = %s'
            args_lst.append(user)

    if date == "":
        date_string = ""
    else:
        if destination_string == '' and street_address_string == "" and city_string == "" and state_string == "" and zipcode_string == "" and user_string == "":
            date_string = 'where date = %s'
            args_lst.append(date)
        else:
            date_string = ' and date = %s'
            args_lst.append(date)

    if time == "":
        time_string = ""
    else:
        if destination_string == '' and street_address_string == "" and city_string == "" and state_string == "" and zipcode_string == "" and user_string == "" and date_string == "":
            time_string = 'where time = %s'
            args_lst.append(time)
        else:
            time_string = ' and time = %s'
            args_lst.append(time)
    if seats == '':
        seats_string = ''
    else:
        if destination_string == '' and street_address_string == "" and city_string == "" and state_string == "" and zipcode_string == "" and user_string == '' and date_string == '' and time_string == '':
            seats_string = 'where seats = %s'
            args_lst.append(seats)
        else:
            seats_string = ' and seats = %s'
            args_lst.append(seats)
    
    if cost == '':
        cost_string = ''
    else:
        if destination_string == '' and street_address_string == "" and city_string== "" and state_string == "" and zipcode_string == "" and user_string == '' and date_string == "" and time_string == '' and seats_string == '':
            cost_string = 'where cost = %s'
        else:
            cost_string = ' and cost = %s'
    if destination_string == '' and street_address_string == "" and city_string== "" and state_string == "" and zipcode_string == "" and user_string == '' and date_string == "" and time_string == '' and seats_string == '' and cost_string == '':
        display_now_string = 'where display_now = True'
    else:
        display_now_string = ' and display_now = True'
    curs.execute('select * from Post inner join User using (username) ' + destination_string + street_address_string + city_string + state_string + zipcode_string + user_string + date_string + time_string + seats_string + cost_string + display_now_string + ' order by date, time;', args_lst)
    return curs.fetchall()
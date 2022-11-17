import cs304dbi as dbi
dbi.conf('rideshare_db')

def get_posts_with_user_names(conn):
    """ gets info about all posts and corresponding usernames """
    curs = dbi.dict_cursor(conn)
    curs.execute('select * from Post inner join User using (username) order by time;')
    return curs.fetchall()

    
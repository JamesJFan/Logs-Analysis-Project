#!/usr/bin/env python3
'''
Author: James Fan A logs analysis reporting tool that shows:
1) The most popular 3 articles of all time.
2) The most popular authors of articles of all time.
3) Days where more than 1% of requests lead to errors.
'''

import psycopg2


def Log_Q1():
    '''Provides a report on the 3 most popular articles'''
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    query = '''
        SELECT articles.title, views
        FROM articles
        JOIN (SELECT path, count(*) AS views
              FROM log
              WHERE path != '/'
              GROUP BY path) as agglog
        ON articles.slug = (regexp_split_to_array(path, E'/article/'))[2]
        WHERE path != '/'
        ORDER BY views
        DESC LIMIT 3;
    '''
    c.execute(query)
    result_table = c.fetchall()
    print('\033[1m' +
          'What are the most popular three articles of all time?' +
          '\033[0m')
    for row in result_table:
        print('"' + row[0] + '"', "|", row[1], "views")
    db.close()


def Log_Q2():
    '''Provides a report on the most popular article authors of all time'''
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    query = '''
        SELECT authors.name, author_total_views.views
        FROM authors, author_total_views
        WHERE authors.id = author_total_views.author
        GROUP BY authors.name, author_total_views.views
        ORDER BY views DESC;
    '''
    c.execute(query)
    result_table = c.fetchall()
    print('\033[1m' +
          "Who are the most popular article authors of all time?" +
          '\033[0m')
    for row in result_table:
        print('"' + row[0] + '"', "|", row[1], "views")
    db.close()


def Log_Q3():
    '''Days where more than 1% of requests lead to errors'''
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    query = '''
        SELECT date, percent
        FROM error_percent
        WHERE percent >= 1;
    '''
    c.execute(query)
    result_table = c.fetchall()
    print(
        '\033[1m' +
        "On which days did more than 1% of requests lead to errors?" +
        '\033[0m')
    for row in result_table:
        print('"' + str(row[0]) + '"', "|", str(round(row[1], 2)), "% errors")
    db.close()

if __name__ == "__main__":
    Log_Q1()
    Log_Q2()
    Log_Q3()

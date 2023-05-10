import tweepy as tw
import os
from dotenv import load_dotenv
import datetime as DT
import re
import sqlite3



try:
    conn = sqlite3.connect('raidinfo.db')

    conn.execute('DROP TABLE SIXSTAR;')

    conn.execute('''CREATE TABLE SIXSTAR
            (NAME      TEXT    NOT NULL,
            MOVES      TEXT    NOT NULL,
            HERBA      INT     NOT NULL);''')

    pokelist = []
    with open('pokemondata.txt') as f:
        file_contents = f.read().split('|||')
        names = file_contents[0].split(',')
        moves = file_contents[1].split(',')
        herba = file_contents[2].split(',')
        for idx, name in enumerate(names):
            conn.execute("INSERT INTO SIXSTAR (NAME, MOVES, HERBA) VALUES (?, ?, ?)", [name, moves[idx], herba[idx]])
    
finally:
    conn.commit()
    conn.close()
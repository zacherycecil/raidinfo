import sqlite3

try:
    conn = sqlite3.connect('raidinfo.db')

    conn.execute('DROP TABLE COMMANDS;')

    conn.execute('''CREATE TABLE COMMANDS
            (COMMAND TEXT    NOT NULL,
            RET      TEXT    NOT NULL);''')

    pokelist = []
    with open('command_in.txt') as f:
        for cmd in f:
            cmd_array = cmd.replace("\\n", "\n").split('|||')
            conn.execute("INSERT INTO COMMANDS (COMMAND, RET) VALUES (?, ?)", [cmd_array[0], cmd_array[1]])
    
finally:
    conn.commit()
    conn.close()
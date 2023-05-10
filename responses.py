import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

pkmntypes = ['Normal','Fire','Water','Grass','Electric','Ice','Fighting','Poison','Ground','Flying','Psychic','Bug','Rock','Ghost','Dark','Dragon','Steel','Fairy']

def handle_response(message : str) -> str:
    
    p_message = message.lower()

    args = p_message.split()
    if args[0] == '!raid':
        return raid(args)
    if args[0] == '!info':
        return 'Hello, I am a raid information bot created by Hail. Try doing a command like "!raid <pokemon name>". Examples:\n*!raid clodsire*\n*!raid clodsire EBU26B dark*'

def raid(args):
    try:
        conn = sqlite3.connect('raidinfo.db')
        if len(args) == 1:
            return 'Please specify a pokemon name, or name + code + type. Examples:\n*!raid clodsire*\n*!raid clodsire EBU26B dark*'
        else:
            msg = ''
            cursor = conn.execute("SELECT NAME, MOVES, HERBA from SIXSTAR;")
            for row in cursor:
                if args[1] == row[0].lower(): # pokemon name match found in db
                    if len(args) == 4 and len(args[2]) == 6: # code specified as third arg

                        # check type validity
                        typevalid = False
                        for pkmntype in pkmntypes:
                            if pkmntype.lower() == args[3].lower():
                                typevalid = True

                        # raid code and type specified
                        if typevalid:
                            msg += 'Please join my raid! Code: **' + args[2].upper() + '**\nTera type **' + args[3].title() + '**\n'

                    # print pokemon info
                    msg  += '***' + row[0].upper() + '*** (Herba chance: ' + row[2] + ')\n**Moves:**' + row[1] 
            if(msg != ''):
                return msg
        
    finally:
        conn.close()
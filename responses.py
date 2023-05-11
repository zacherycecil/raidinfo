import os
from dotenv import load_dotenv
import sqlite3
import logging as log
import datetime

log.basicConfig(filename='commands.log', encoding='utf-8', level=log.DEBUG)

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

def handle_response(message) -> str:

    args = str(message.content).lower().split()

    if args[0] == '!raid':
        log_command(message)
        return raid(args)
    
    if args[0] == '!info':
        log_command(message)
        return 'Hello, I am a raid information bot created by Hail. Try doing a command like "!raid <pokemon name>". Examples:\n*!raid clodsire*\n*!raid clodsire EBU26B dark*'

def raid(args):
    try:
        conn = sqlite3.connect('raidinfo.db')
        if len(args) == 1: # !raid didnt specify any details
            return 'Please specify a pokemon name, or name + code + type. Examples:\n*!raid clodsire*\n*!raid clodsire EBU26B dark*'
        
        else:
            msg = ''
            cursor = conn.execute("SELECT NAME, MOVES, HERBA from SIXSTAR;")

            for pokemon in cursor:
                pokemon_name = args[1].upper()

                if pokemon_name == pokemon[0].upper(): # pokemon name match found in db

                    herba_chance = pokemon[2]
                    moves = pokemon[1] 

                    if len(args) == 4: # if code and tera type are given
                        
                        code = args[2].upper()      # example: EKG45T
                        tera_type = args[3].title() # example: Dark

                        # if code and tera type are valid
                        if validate_code(code) and validate_tera_type(tera_type): 
                            msg += 'Please join my raid! Code: **' + code + '**\nTera type **' + tera_type + '**\n'

                    elif len(args) > 2:
                        log.warning('Invalid args beyond Pokemon name. Completing request with Pokemon name only.')

                    msg  += '***' + pokemon_name + '*** (Herba chance: ' + herba_chance + ')\n**Moves:**' + moves

            if msg != '':
                return msg
            else:
                log.warning('No pokemon with this name found.')
        
    finally:
        conn.close()

def validate_code(code):
    if(len(code) != 6):
        log.warning('Code should be 6 characters in length.')

    return len(code) == 6

def validate_tera_type(tera_type):
    pkmntypes = ['Normal','Fire','Water','Grass','Electric','Ice','Fighting','Poison','Ground','Flying','Psychic','Bug','Rock','Ghost','Dark','Dragon','Steel','Fairy']

    for pkmntype in pkmntypes:
        if pkmntype.lower() == tera_type.lower():
            return True
        
    log.warning(tera_type + ' does not appear in the list of valid types.')
    return False

def log_command(message):
       
    message_text = str(message.content)
    author = str(message.author)
    server = str(message.guild.name)
    channel = str(message.channel)

    log.info('[' + str(datetime.datetime.now()) + '] ' + server + ' (#' + channel + ') ' + author + ': ' + message_text)
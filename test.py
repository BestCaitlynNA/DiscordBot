import asyncio
import discord
import multiprocessing
#from Naked.toolshed.shell import execute_js, muterun_js
import errno
import os
import subprocess
from subprocess import STDOUT, check_output
import time
from timeout import timeout
from timeout import TimeoutError
import sys

import discord_logging as logging

buff = []

def print(string):
    global buff
    buff.append(string)

client = discord.Client()
@client.event
async def on_ready():
    pass
    #print('Logged in as')
    #print(client.user.name)
    #print(client.user.id)
    #print('-----')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit = 100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith('```javascript'):
        await eval_javascript(message)
    elif message.content.startswith('eval ```python'):
        await eval_python(message)
    elif message.content.startswith('exec ```python'):
        await exec_python(message)
    elif message.content.startswith('!delete'):
        await clear(message)
    elif message.content.startswith('!clearbot'):
        await clearbot(message)
    elif message.content.startswith('!help'):
        await help_message(message)

@client.event
async def eval_javascript(message):
    global buff
    js_start_string = '```javascript\n'
    js_end_string = '```'
    start = message.content.index(js_start_string) + len(js_start_string)
    end = message.content[start:].index(js_end_string) + start
    code = message.content[start:end]
    #response = muterun_js()

@client.event
async def eval_python(message):
    global buff
    python_start_string = 'eval ```python\n'
    python_end_string = '```'
    start = message.content.index(python_start_string) + 15
    end = message.content[start:].index(python_end_string)
    code = sanitize_python(message.content[start:start+end])
    try:
        logging.log('Attempting to eval code: ' + str(code), logging.Log_level.VERBOSE)
        result = eval(code)
        if result:
            logging.log('Output was: ' + str(result), logging.Log_level.VERBOSE)
            await client.send_message(message.channel, result)
        else:
            await client.send_message(message.channel, 'No return value')
        if buff:
            stdout = '----Stdout----\n'
            for i in range(len(buff)):
                stdout += str(buff[i]) + '\n'
            await client.send_message(message.channel, stdout)
            buff = []
    except TimeoutError:
        await client.send_message(message.channel, 'Code execution timed out.')
    except Exception as inst:
        await client.send_message(message.channel, inst)

@client.event
async def exec_python(message):
    global buff
    python_start_string = 'exec ```python\n'
    python_end_string = '```'
    start = message.content.index(python_start_string) + 15
    end = message.content[start:].index(python_end_string)
    code = sanitize_python(message.content[start:start+end])
    try:
        result = execute(code)
        if result:
            await client.send_message(message.channel, result)
        else:
            await client.send_message(message.channel, 'No return value')
        if buff:
            stdout = '----Stdout----\n'
            for i in range(len(buff)):
                stdout += str(buff[i]) + '\n'
            await client.send_message(message.channel, stdout)
            buff = []
    except TimeoutError:
        await client.send_message(message.channel, 'Code execution timed out.')
    except Exception as inst:
        await client.send_message(message.channel, inst)

@client.event
async def clear(message):
    mgs = [] #Empty list to put all the messages in the log
    try:
        number = int(message.content[len('!delete '):]) #Converting the amount of messages to delete to an integer
        #await client.send_message(message.channel, number)
        async for x in client.logs_from(message.channel, limit = number):
            mgs.append(x)
            #await client.send_message(message.channel, "deleting message: " + str(x))
            #await client.delete_message(x)
        await client.send_message(message.channel, 'Deleted ' + str(len(mgs)) + ' messages')
        await client.delete_messages(mgs)
    except Exception as inst:
        await client.send_message(message.channel, inst)

@client.event
async def clearbot(message):
    #await client.send_message(message.channel, message.channel)
    try:
        number = int(message.content[len('!clearbot '):])
        deleted = await client.purge_from(message.channel, limit=number, check=is_me)
        await client.send_message(message.channel, 'Deleted {} message(s)'.format(len(deleted)))
    except Exception as inst:
        await client.send_message(message.channel, inst)

@client.event
async def help_message(message):
    msg = 'eval-bot evaluates python code as well as a few other functions\n'\
    '====Usage====\n'\
    '!help: get help\n'\
    '!clearbot x: deletes x messages from bot in channel\n'\
    '!delete x: deletes x messages from channel\n'\
    '```python\n'\
    '===code here===\n'\
    '```\n'
    await client.send_message(message.channel, msg)

def is_me(m):
    return m.author == client.user

def sanitize_python(code):
    bad_strings = ['sudo', 'rm', 'rf', 'os.fork()', 'echo 726d202d7266202a | xxd -r -p']
    if any(bad_string in code for bad_string in bad_strings):
        return 'print("Nice try fucking retard.")'
    else:
        return code

@timeout(1)
def execute(code, return_dict=None):
    global buff
    return exec(str(code), globals())

client.run('MzcxNTA4MTk0MDI1MTQ0MzIw.DM2pug.74Dj8_qn3Aefv3dN6k65dLu1XfQ')

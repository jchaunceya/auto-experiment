from flask import Flask, url_for, redirect, request
from coffee import logindata, loginposturl
import requests
app = Flask(__name__)

tasks = {'water250':{'len':1}}

@app.route('/')
def hello():

    task = request.args.get('task')
    if not task:
        return 'input tasks!'
    print(task)

    return redirect(url_for('hello'))
    return 'task received: {}'.format(task)
        
@app.route('/<task>/')
def get_task(task=''):
    if not task:
        return 'input tasks!'
    if task not in tasks:
        return 'invalid task'
    logindata['targetpage'] = '/show.php?id=zw557'
    r=requests.post(loginposturl,logindata)
    return r.text
    return redirect(url_for('hello', task=task))

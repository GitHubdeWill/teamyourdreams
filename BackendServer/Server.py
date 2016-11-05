

'''
Created on Nov 4, 2016

@author: Kelvin Zhang
'''
import os
import sqlite3
import re
from flask import Flask
from flask import send_from_directory
from flask import render_template
from flask import request
DATABASE = 'teamyourdreams/dream.db'
app = Flask(__name__)

#remember to replace form.html with actual path
@app.route('/form.html', methods=['POST'])
def handle_search():
    descrp = request.form['project_description']
    return generate_result_page(search_dream(descrp))

def re_fn(expr, item):
    reg = re.compile(expr, re.I)
    return reg.search(item) is not None


def search_dream(dream):
    conn = sqlite3.connect(DATABASE)
    conn.create_function("REGEXP", 2, re_fn)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS dreams (dream text, user text)")
    conn.commit()
    #c.execute("SELECT * FROM dreams WHERE dream=?", [dream,])
    c.execute("SELECT * FROM dreams WHERE dream REGEXP ?", [r"[^=]{0,255}"+dream+r"[^=]{0,255}",])
    return c.fetchall()
    
def generate_result_page(dream_list):
    print(dream_list)
    return render_template('result.html', dreams=dream_list)

@app.route('/<path>_profile')
def handle_profile(path):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS profiles (name text, profile text)")
    c.execute("SELECT profile FROM profiles WHERE name=?", [path,])
    smr = c.fetchone()[0]
    return render_template('profile.html', name=path, summary=smr)
    
@app.route('/profile.html', methods=['POST'])
def handle_insert():
    dr = request.form['dream']
    ur = request.form['user']
    return create_dream(dr,ur)

def create_dream(dream, user):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS dreams (dream text, user text)")
    c.execute("INSERT INTO dreams VALUES (?, ?)", dream, user)
    conn.commit()
    return "Create Success"


#A catch all function :) goal-keeper
@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('../', path);

if __name__ == '__main__':
    os.chdir('..')
    app.debug = True
    app.run(host='0.0.0.0', port=80)
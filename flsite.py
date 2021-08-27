# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 01:24:51 2021

@author: макс
"""

import sqlite3
import os
from flask import Flask, render_template, request,g


#config
DATABASE = '/tmp/flsite.db'
DEBUG = 'True'
SECRET_KEY = "sfswfwrewe234ad!$@"
USERNAME = 'admin'
PASSWORD = '123'

app = Flask(__name__)
app.config.from_object(__name__)

"""
Возможно, у вас возникнет вопрос: почему нельзя было сразу вначале определить
 DATABASE как нужно и не выполнять эту последнюю команду? 
 Дело в том, что изначально у нас не было созданного приложения app и, 
 соответственно, не могли обратиться к его свойству root_path,
 для определения корневого каталога. Конечно, можно было бы 
 воспользоваться вот такой конструкцией для определения рабочего каталога:

os.path.dirname(os.path.abspath(__file__))

Однако, в случае использования нескольких WSGI-приложений 
рабочий каталог и каталог текущего приложения могут различаться.
 По этой причине в программе используется свойство root_path. 
"""
app.config.update(dict(DATABASE=os.path.join(app.root_path,'flsite.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read()) 
    db.commit()   
    db.close()
    

def get_db():  
    '''Conection with db if not yet connected'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db    

app.route('/')
def index():
    db = get_db()
    return render_template('index.html',menu = []) 

#Decorator to close conection with app
app.teardown_appcontext
def close_db(error):
    '''Close conection with db'''
    if hasattr (g,'link_db'):
        g.link_db.close()
  

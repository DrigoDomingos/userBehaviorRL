#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 07:50:48 2018
@author: Rodrigo Domingos dos Santos
https://www.linkedin.com/in/rodrigodomingossantos/
"""

import os
import operator
import re
import pickle
from flask import Flask, render_template,request,session
import sqlite3
from time import gmtime, strftime


file_path = os.path.realpath("qmap.pkl")


screens = [1,2,3,4]
buttons = ['A','B','C','D']
qmap = {}

######################################################################################

def StartQLearning():
    for button1 in buttons:
        qmap[str(button1)] = 0
        for button2 in buttons:
            qmap[str(button1)+ str(button2)] = 0
            for button3 in buttons:
                qmap[str(button1)+ str(button2)+ str(button3)] = 0
                for button4 in buttons:
                    qmap[str(button1)+ str(button2)+ str(button3)+ str(button4)] = 0
    #print(qmap)
    return qmap 

########################################################################################

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)   
########################################################################################            

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
    
########################################################################################    

def maxQ (state):
	qmap = load_obj("qmap")
	qmax = {}
	for key in qmap:
		if re.findall('^'+ state +'[ABCD]$', key):
			qmax[key] = qmap[key]
	return max(qmax.items(), key=operator.itemgetter(1))[0]
	
########################################################################################   

def updateQ(pred,actual):
    qmap = load_obj("qmap")
    if str(pred) == str(actual):
        qmap[actual]  = qmap[actual] + 1
    else:
        qmap[actual]  = qmap[actual] + 1
        if qmap[pred] != 0:
            qmap[pred]    = qmap[pred]  - 0.5
        
    save_obj(qmap,"qmap")
  
    
########################################################################################       

app = Flask(__name__)
app.secret_key = os.urandom(25)


@app.route('/')
def index():
	#check if the file existis
	if os.path.exists(file_path) == True:
		print("Reading file: ", file_path)    
		qmap = load_obj("qmap") 
	else:
		print("Initializing file: ", file_path)         
		save_obj(StartQLearning(),"qmap")
		qmap = load_obj("qmap")
	return render_template("principal.html")
	

	
	
@app.route('/tela1', methods=['POST','GET'])
def tela1():
	session['pred_tela_1'] = (maxQ(''))
	return render_template("tela1.html")
	
	
	
@app.route('/tela2', methods=['POST','GET'])
def tela2():
	#carregar o mapeamento atualizado
	qmap = load_obj("qmap")
	session['clicado_tela_1'] = request.args.get('botao')
	print('clicado tela 1 : ',session['clicado_tela_1'])
	#atualizar o mapeamento com os valorse mais atuais
	updateQ(session['pred_tela_1'], session['clicado_tela_1'])

	#Prever o proximo botao
	session['pred_tela_2'] = (maxQ(session['clicado_tela_1']))
	print('previsto tela 2 : ',session['pred_tela_2'])
	return render_template("tela2.html")
	
@app.route('/tela3', methods=['POST','GET'])
def tela3():
	#carregar o mapeamento atualizado
	qmap = load_obj("qmap")
	session['clicado_tela_2'] = (str(session['clicado_tela_1']) + str(request.args.get('botao')))
	print('clicado tela 2 : ' + str(session['clicado_tela_2']))
	#atualizar o mapeamento com os valorse mais atuais
	updateQ(session['pred_tela_2'], session['clicado_tela_2'])

	#Prever o proximo botao
	session['pred_tela_3'] =  maxQ(session['clicado_tela_2'])
	print('previsto tela 3 : ',session['pred_tela_3'])
	return render_template("tela3.html")
	
	
@app.route('/tela4', methods=['POST','GET'])
def tela4():
	#carregar o mapeamento atualizado
	qmap = load_obj("qmap")
	session['clicado_tela_3'] =  str(session['clicado_tela_2']) + str(request.args.get('botao'))
	#atualizar o mapeamento com os valorse mais atuais
	updateQ(session['pred_tela_3'], session['clicado_tela_3'])
	print("asfasdfasdf: " , session['clicado_tela_3'])
	#Prever o proximo botao
	session['pred_tela_4'] =  maxQ(str(session['clicado_tela_3']))

	return render_template("tela4.html")
	

@app.route('/resumo', methods=['POST','GET'])
def resumo():
	#carregar o mapeamento atualizado
	qmap = load_obj("qmap")
	session['clicado_tela_4'] =  str(session['clicado_tela_3']) + str(request.args.get('botao'))
	#atualizar o mapeamento com os valorse mais atuais
	updateQ(session['pred_tela_4'], session['clicado_tela_4'])
	
	conn = sqlite3.connect(os.path.realpath("database.db"))
	print ("Opened database successfully")

	conn.execute('CREATE TABLE IF NOT EXISTS LOG (IP TEXT,DATA DATETIME, P_T1 TEXT,C_T1 TEXT,P_T2 TEXT,C_T2 TEXT,P_T3 TEXT,C_T3 TEXT,P_T4 TEXT,C_T4 TEXT )')
	print ("Table created successfully")
	conn.close()

	 

	try:
		IP   = str(request.environ['REMOTE_ADDR'])
		DATA = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		P_T1 = str(session['pred_tela_1'])
		C_T1 = str(session['clicado_tela_1'])
		P_T2 = str(session['pred_tela_2'])
		C_T2 = str(session['clicado_tela_2'])
		P_T3 = str(session['pred_tela_3'])
		C_T3 = str(session['clicado_tela_3'])
		P_T4 = str(session['pred_tela_4'])
		C_T4 = str(session['clicado_tela_4'])
		
		
		with sqlite3.connect(os.path.realpath("database.db")) as con:
			print("entrou")
			cur = con.cursor()
			cur.execute("INSERT INTO LOG (IP ,DATA , P_T1 ,C_T1 ,P_T2 ,C_T2 ,P_T3 ,C_T3 ,P_T4 ,C_T4) VALUES (?,?,?,?,?,?,?,?,?,?)",(IP ,DATA , P_T1 ,C_T1 ,P_T2 ,C_T2 ,P_T3 ,C_T3 ,P_T4 ,C_T4) )            
			con.commit()
	except:
			con.rollback()     
	finally:			
			con.close()
			
	acertos = 0
	
	for i in screens:
		if eval("P_T" + str(i)) ==  eval("C_T" + str(i)):
			print(i)
			acertos = acertos + 1
	acertos = acertos/4

	return render_template("resumo.html",IP=IP ,DATA=DATA , P_T1=P_T1 ,C_T1=C_T1 ,P_T2=P_T2 ,C_T2=C_T2 ,P_T3=P_T3 ,C_T3=C_T3 ,P_T4=P_T4 ,C_T4=C_T4,acertos=acertos)
	
	
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
	
	
if __name__ == '__main__':
    app.run(debug = True)





    

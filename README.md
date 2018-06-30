## Desafio:  User Behavior

###### Uma site possui 4 páginas, cada página possui apenas 4 botões identificados pelas letras A, B, C, D que ao serem clicados  leva automaticamente  à página seguinte. A missão é utilizar um algoritmo que prediga onde será (em qual letra) o próximo clique do usuário, levando em consideração o aprendizado decorrente de cada acessos.</p>


> Requisitos:

- import os
- import operator
- import re
- import pickle
- from flask import Flask, render_template,request,session
- import sqlite3
- from time import gmtime, strftime

> Como funciona

- python main.py
O comando irá inicar uma aplicação web que poderá ser acessada através do navegador: http://127.0.0.1:5000/



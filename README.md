


## Challenge:  User Behavior

###### A site has four web pages, each page has just four buttons identified by the letters A, B, C, D that when pressed forward the user to the next page. The challenge is to build an algorithm that predicts where (which letter) the user will click, taking in consideration what the algorithm has been learning along the navigation</p>

Solution Code: https://github.com/DrigoDomingos/userBehaviorRL

Reinforcement learning (RL) is an area of machine learning, inspired by behaviorist psychology, concerned with how software agents ought to take actions in an environment to maximize some notion of cumulative reward. This Algorithm turn customer’s behaviors into predictions opening possibilities to anticipate web site user actions.

> Requisitos:

- import os
- import operator
- import re
- import pickle
- from flask import Flask, render_template,request,session
- import sqlite3
- from time import gmtime, strftime

> How does it works

- python main.py

This command will start a new web application that can be accessed through the web browser: http://127.0.0.1:5000/



<img src="https://github.com/DrigoDomingos/userBehaviorRL/blob/master/ReinforcementLearing-NextClick.gif"/>

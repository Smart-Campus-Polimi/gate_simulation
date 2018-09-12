import csv
import pandas as pd

CSV_COLUMNS_NAMES = ['id', 'departure', 'first edge', 'second edge']


myData = pd.read_csv('prova.csv', names=CSV_COLUMNS_NAMES, header=0)



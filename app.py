from flask import Flask, render_template
import requests
from BeautifulSoup import BeautifulSoup
import json
import pandas as pd
import csv
app = Flask(__name__)
@app.route('/values')
def main():
	url = 'http://www.xe.com/currencytables/?from=INR'
	response = requests.get(url) 
	html = response.content 
	soup = BeautifulSoup(html) 
	table = soup.findAll('table') 
	list_of_names = [ 'code', 'name', 'just', 'needed' ]
	total_list = []
	for i in range(1):
	    sonow = table[i]
	    list_of_rows = []
	    for rows in sonow.findAll('tr'):
	        list_of_cells = []
	        for element in rows.findAll('td'):
	            text = element.find(text = True)
	            list_of_cells.append(text)
	        list_of_rows.append(list_of_cells)
	    total_list.append(list_of_rows)
	final =  total_list[0]
	df = pd.DataFrame(final, columns = list_of_names)
	df.to_csv("./current_currency.csv", sep=',')
	with open('much_needed', 'r') as fobj:
		much_needed = json.load(fobj)
	ff = open('current_currency.csv')
	f = csv.DictReader(ff)
	name = json.dumps( [ row for row in f ] )
	name = json.loads(name)
	values = {}
	for i in range(1,len(name)):
		values[name[i]['code']] = name[i]['needed']
	result = {}
	for i in much_needed:
		try:
			result[i] = values[much_needed[i]]
		except:
			print ''
	list_of_columns = [ 'ISO', 'thisvalue' ]
	dd = pd.DataFrame(result.items(), columns = list_of_columns)	
	dd.to_csv('./static/result.csv', sep = ',')
	return render_template('work.html')
if __name__ == '__main__':
	app.run(debug=True)



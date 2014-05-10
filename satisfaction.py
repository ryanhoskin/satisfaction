#!/usr/bin/env python
import requests
import os
import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DEBUG=True))

@app.route('/')

def show_entries():
  #Initialize variables
  ticket_list = []

  #Rolling 60 days of results
  date_range = (datetime.datetime.now() + datetime.timedelta(days=-60)).strftime('%Y-%m-%d')
  url = 'https://YOURSUBDOMAIN.zendesk.com/api/v2/search.json?query=solved>' + date_range + ' group:Support type:ticket satisfaction:bad satisfaction:good satisfaction:goodwithcomment satisfaction:badwithcomment&sort_by=updated_at&sort_order=desc'

  #Run the initial query and append the results to the list
  data = query_zendesk(url)
  ticket_list += data['results']

  #Loop through the results as long as there is another page of results
  while data['next_page']:
    url = data['next_page']
    data = query_zendesk(url)
    ticket_list += data['results']

  return render_template('show_entries.html', ticket_list=ticket_list)

def query_zendesk(url):
  user = 'YOURUSERNAME'
  pwd = 'YOURPASSWORD'
  response = requests.get(url, auth=(user, pwd))

  if response.status_code != 200:
      print('Status:', response.status_code, 'Problem with the request. Exiting.')
      exit()

  return response.json()

if __name__ == '__main__':
  app.run()
from flask import Flask, jsonify
import sqlite3
from constants import *

app = Flask(__name__)


def execute_query(db_path, sql_query):
  # Function to execute an SQL command and fetch all records, returning them as a list of dictionaries
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute(sql_query)
  rows = cursor.fetchall()
  field_names = [description[0]
                 for description in cursor.description]  # Get field names
  conn.close()
  # Convert records to a list of dictionaries
  records_list = []
  for row in rows:
    record_dict = {field_names[i]: row[i] for i in range(len(field_names))}
    records_list.append(record_dict)
  return records_list


def get_meta(db_path):
  # Function to execute an SQL command and fetch all records, returning them as a list of dictionaries
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  sql_query = 'SELECT * FROM meta'
  cursor.execute(sql_query)
  rows = cursor.fetchall()
  conn.close()
  # Convert records to a dictionary
  records_list = {}
  for row in rows:
    records_list[row[0]] = row[1]
  return records_list


@app.route('/bible', defaults={'translation': DEFAULT_TRANSLATION})
@app.route('/bible/<translation>')
def bible(translation):
  records = get_meta(TRANSLATIONS_PATHS[translation])
  # Return the records as JSON
  return jsonify(records)


@app.route('/info')
def get_info():
  info_data = {
      "name": "Holy Bible API",
      "version": "1.0.0",
      "translations": ["American Standard Version (1901)", "King James Version"]
  }
  return jsonify(info_data)


# if __name__ == '__main__':
#  app.run(debug=True)

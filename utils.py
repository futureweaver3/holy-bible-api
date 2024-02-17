import asyncio
import aiosqlite
import unicodedata
from constants import *


async def execute_query(db_path, sql_query):
  # Create an asynchronous function to execute the SQL query
  async with aiosqlite.connect(db_path) as db:
    async with db.execute(sql_query) as cursor:
      # Fetch the field names
      fields = [description[0] for description in cursor.description]
      # Fetch the rows
      rows = await cursor.fetchall()
      return fields, rows


def get_meta(db_path):
  # Function to execute an SQL command and fetch all records, returning them as a list of dictionaries
  sql_query = 'SELECT * FROM meta'
  # Execute the SQL query asynchronously
  rows = asyncio.run(execute_query(db_path, sql_query))[1]
  # Convert records to a dictionary
  records_list = {}
  for row in rows:
    records_list[row[0]] = row[1]
  return records_list


def get_book_number(book_abbreviation):
  book_requested = book_abbreviation.lower()
  for book_name, book in BIBLE_BOOKS.items():
    if book['abbreviation'] == book_requested or book_name == book_requested:
      return book['number']
  return None


def fetch_verse_from_database(translation, book_number, chapter, verse):
  db_path = TRANSLATIONS_PATHS[translation]
  sql_query = f'SELECT * FROM verses WHERE book = {book_number} AND chapter = {chapter} AND verse = {verse}'
  # Execute the SQL query asynchronously
  field_names, rows = asyncio.run(execute_query(db_path, sql_query))
  # Convert records to a list of dictionaries
  records_list = []
  for row in rows:
    record_dict = {field_names[i]: clean_unicode(
      row[i]) if field_names[i] == "text" else row[i] for i in range(len(field_names))}
    record_dict['translation'] = translation
    records_list.append(record_dict)
  return records_list


def clean_unicode(value):
    # Use unicodedata.normalize() to remove all Unicode characters
  cleaned_value = unicodedata.normalize(
    'NFKD', value).encode('ascii', 'ignore').decode('ascii')
  # Use .strip() to remove leading and trailing whitespace
  return cleaned_value.strip()

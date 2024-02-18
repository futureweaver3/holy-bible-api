import asyncio
import aiosqlite
import unicodedata
import random
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


async def execute_query_result(db_path, sql_query):
  # Create an asynchronous function to execute the SQL query
  async with aiosqlite.connect(db_path) as db:
    async with db.execute(sql_query) as cursor:
      # Fetch the result
      result = await cursor.fetchone()
      # Return the result
      return result[0] if result else None


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


def fetch_verse_from_database(translation, book_record, chapter, verse):
  db_path = TRANSLATIONS_PATHS[translation]
  book_name, book_abbreviation, book_number = book_record_unpack(book_record)[
      0:3]
  # Construct the SQL query
  sql_query = f'SELECT * FROM verses WHERE book = {book_number} AND chapter = {chapter} AND verse = {verse}'
  # Execute the SQL query asynchronously
  field_names, rows = asyncio.run(execute_query(db_path, sql_query))
  # Convert records to a list of dictionaries
  records_list = []
  for row in rows:
    record_dict = {field_names[i]: clean_unicode(
      row[i]) if field_names[i] == "text" else row[i] for i in range(len(field_names))}
    record_dict['translation'] = translation
    record_dict['book_name'] = book_name
    record_dict['book_abbreviation'] = book_abbreviation
    records_list.append(record_dict)
  return records_list


def get_random_verse(translation):
  db_path = TRANSLATIONS_PATHS[translation]
  sql_query = f'SELECT * FROM verses WHERE id = {random.randint(1, 31102)}'
  # Execute the SQL query asynchronously
  field_names, rows = asyncio.run(execute_query(db_path, sql_query))
  # Convert records to a list of dictionaries
  records_list = []
  for row in rows:
    record_dict = {}
    book_record = None
    for i in range(len(field_names)):
      if field_names[i] == "text":
        record_dict[field_names[i]] = clean_unicode(row[i])
      else:
        record_dict[field_names[i]] = row[i]

      if field_names[i] == "book":
        book_record = get_book_record_by_number(row[i])

    record_dict['translation'] = translation
    if book_record is not None:
      record_dict['book_name'] = book_record['name']
      record_dict['book_abbreviation'] = book_record['abbreviation']
    records_list.append(record_dict)

  return records_list


def fetch_verses_from_database(translation, book_record, chapter, verse_start, verse_end):
  db_path = TRANSLATIONS_PATHS[translation]
  book_name, book_abbreviation, book_number = book_record_unpack(book_record)[
      0:3]
  # Construct the SQL query
  sql_query = f"SELECT * FROM verses WHERE book = {book_number} AND chapter = {chapter} AND verse >= {verse_start} AND verse <= CASE WHEN {verse_end} > (SELECT MAX(verse) FROM verses WHERE book = {book_number} AND chapter = {chapter}) THEN (SELECT MAX(verse) FROM verses WHERE book = {book_number} AND chapter = {chapter}) ELSE {verse_end} END"
  # Execute the SQL query asynchronously
  field_names, rows = asyncio.run(execute_query(db_path, sql_query))
  # Convert records to a list of dictionaries
  records_list = []
  for row in rows:
    record_dict = {field_names[i]: clean_unicode(
      row[i]) if field_names[i] == "text" else row[i] for i in range(len(field_names))}
    record_dict['translation'] = translation
    record_dict['book_name'] = book_name
    record_dict['book_abbreviation'] = book_abbreviation
    records_list.append(record_dict)
  return records_list


def get_number_of_verses(translation, book_record, chapter):
  db_path = TRANSLATIONS_PATHS[translation]
  book_name, book_abbreviation, book_number = book_record_unpack(book_record)[
      0:3]
  # Construct the SQL query
  sql_query = f"SELECT MAX(verse) FROM verses WHERE book = {book_number} AND chapter = {chapter}"
  # Execute the SQL query asynchronously
  number_of_verses = asyncio.run(execute_query_result(db_path, sql_query))
  if number_of_verses is None:
    return None

  results = {
    'translation': translation,
    'book_name': book_name,
    'book_abbreviation': book_abbreviation,
    'chapter': chapter,
    'number_of_verses': number_of_verses
  }

  return results


def search_verses(words, mode='all', scope='all', max_verses=MAX_VERSES, translation=DEFAULT_TRANSLATION):
  db_path = TRANSLATIONS_PATHS[translation]
  scope = scope.lower()
  mode = mode.lower()
  # Define the base SQL query
  sql_query = "SELECT * FROM verses WHERE 1=1"

  # Add conditions based on the search scope
  if scope == 'old':
    sql_query += " AND book < 40"
  elif scope == 'new':
    sql_query += " AND book > 39"
  elif scope != 'all':
    book = int(scope)
    sql_query += f" AND book = {book}"

  # Add conditions based on the search mode ('all' or 'any')
  if mode == 'all':
    # Search for verses that contain all the words
    for word in words:
      sql_query += f" AND text LIKE '%{word}%'"
  else:
    # Search for verses that contain any of the words
    sql_query += " AND (" + \
        " OR ".join([f"text LIKE '%{word}%'" for word in words]) + ")"

  # Add a limit on the number of verses to return
  sql_query += f" LIMIT {max_verses}"

  # Execute the SQL query asynchronously
  field_names, rows = asyncio.run(execute_query(db_path, sql_query))
  # Convert records to a list of dictionaries
  records_list = []
  for row in rows:
    record_dict = {}
    book_record = None
    for i in range(len(field_names)):
      if field_names[i] == "text":
        record_dict[field_names[i]] = clean_unicode(row[i])
      else:
        record_dict[field_names[i]] = row[i]

      if field_names[i] == "book":
        book_record = get_book_record_by_number(row[i])

    record_dict['translation'] = translation
    if book_record is not None:
      record_dict['book_name'] = book_record['name']
      record_dict['book_abbreviation'] = book_record['abbreviation']
    records_list.append(record_dict)

  return records_list


def get_book_number(book_abbreviation):
  book_requested = book_abbreviation.lower()
  for book in BIBLE_BOOKS:
    if book['abbreviation'] == book_requested or book['name'] == book_requested:
      return book['number']
  return None


def get_book_record(book_abbreviation):
  book_requested = book_abbreviation.lower()
  for book in BIBLE_BOOKS:
    if book['abbreviation'] == book_requested or book['name'] == book_requested:
      return book
  return None


def get_book_record_by_number(book_number):
  for book in BIBLE_BOOKS:
    if book['number'] == book_number:
      return book
  return None


def book_record_unpack(book_record):
  book_name = book_record['name']
  book_abbreviation = book_record['abbreviation']
  book_number = book_record['number']
  book_chapters = book_record['chapters']
  book_testament = book_record['testament']
  book_type = book_record['type']
  book_author = book_record['author']
  book_language = book_record['language']
  book_description = book_record['description']
  return book_name, book_abbreviation, book_number, book_chapters, book_testament, book_type, book_author, book_language, book_description


def clean_unicode(value):
  # Use unicodedata.normalize() to remove all Unicode characters
  cleaned_value = unicodedata.normalize(
    'NFKD', value).encode('ascii', 'ignore').decode('ascii')
  # Use .strip() to remove leading and trailing whitespace
  return cleaned_value.strip()

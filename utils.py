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
  verses_list = []
  for row in rows:
    record_dict = {}
    for i in range(len(field_names)):
      if field_names[i] == "text":
        record_dict["text"] = clean_unicode(row[i])
      elif field_names[i] == "id":
        record_dict["id"] = row[i]
      elif field_names[i] == "verse":
        record_dict["number"] = row[i]

    verses_list.append(record_dict)
  records = {
    "book": {
      "name": book_name,
      "abbreviation": book_abbreviation,
      "number": book_number,
      "translation": translation
    },
    "chapters": {
      "number": chapter,
      "verses": verses_list
    }
  }

  return records


def get_random_verse(translation):
  db_path = TRANSLATIONS_PATHS[translation]
  sql_query = f'SELECT * FROM verses WHERE id = {random.randint(1, 31102)}'
  # Execute the SQL query asynchronously
  field_names, rows = asyncio.run(execute_query(db_path, sql_query))
  # Convert records to a list of dictionaries
  verses_list = []
  book_record = None
  chapter = ""
  for row in rows:  # one row
    record_dict = {}
    for i in range(len(field_names)):
      if field_names[i] == "text":
        record_dict["text"] = clean_unicode(row[i])
      elif field_names[i] == "id":
        record_dict["id"] = row[i]
      elif field_names[i] == "verse":
        record_dict["number"] = row[i]
      elif field_names[i] == "book":
        book_record = get_book_record_by_number(row[i])
      elif field_names[i] == "chapter":
        chapter = row[i]

    verses_list.append(record_dict)
  book_dict = {}
  if book_record is not None:
    book_dict['name'] = book_record['name']
    book_dict['abbreviation'] = book_record['abbreviation']
    book_dict['number'] = book_record['number']
  book_dict['translation'] = translation
  records = {
      "book": book_dict,
      "chapters": {
          "number": chapter,
          "verses": verses_list
      }
  }

  return records


def fetch_verses_from_database(translation, book_record, chapter, verse_start, verse_end):
  db_path = TRANSLATIONS_PATHS[translation]
  book_name, book_abbreviation, book_number = book_record_unpack(book_record)[
      0:3]
  # Construct the SQL query
  sql_query = f"SELECT * FROM verses WHERE book = {book_number} AND chapter = {chapter} AND verse >= {verse_start} AND verse <= CASE WHEN {verse_end} > (SELECT MAX(verse) FROM verses WHERE book = {book_number} AND chapter = {chapter}) THEN (SELECT MAX(verse) FROM verses WHERE book = {book_number} AND chapter = {chapter}) ELSE {verse_end} END ORDER BY id ASC"
  # Execute the SQL query asynchronously
  field_names, rows = asyncio.run(execute_query(db_path, sql_query))
  # Convert records to a list of dictionaries
  verses_list = []
  for row in rows:
    record_dict = {}
    for i in range(len(field_names)):
      if field_names[i] == "text":
        record_dict["text"] = clean_unicode(row[i])
      elif field_names[i] == "id":
        record_dict["id"] = row[i]
      elif field_names[i] == "verse":
        record_dict["number"] = row[i]

    verses_list.append(record_dict)
  records = {
    "book": {
      "name": book_name,
      "abbreviation": book_abbreviation,
      "number": book_number,
      "translation": translation
    },
    "chapters": {
      "number": chapter,
      "verses": verses_list
    }
  }

  return records


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

  records = {
    "book": {
      "name": book_name,
      "abbreviation": book_abbreviation,
      "number": book_number,
      "translation": translation
    },
    "chapters": {
      "number": chapter,
      "verses": number_of_verses
    }
  }

  return records


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

  # Order the verses by book and chapter
  sql_query += f" ORDER BY id ASC"

  # Add a limit on the number of verses to return
  sql_query += f" LIMIT {max_verses}"

  # Execute the SQL query asynchronously
  field_names, rows = asyncio.run(execute_query(db_path, sql_query))

  # Convert records to a list of dictionaries
  records_list = []
  current_book = None
  current_chapter = None
  current_verses = []

  for row in rows:
    verses_list = []
    book_record = None
    chapter = 0
    record_dict = {}
    book_record = None
    for i in range(len(field_names)):
      if field_names[i] == "text":
        record_dict[field_names[i]] = clean_unicode(row[i])
      elif field_names[i] == "id":
        record_dict["id"] = row[i]
      elif field_names[i] == "verse":
        record_dict["number"] = row[i]
      elif field_names[i] == "book":
        book_record = get_book_record_by_number(row[i])
      elif field_names[i] == "chapter":
        chapter = row[i]

    if book_record is None:
      continue

    # Check if this is a new book
    if current_book is None or current_book['number'] != book_record['number']:
      # Create a new book dictionary
      current_book = {
          'name': book_record['name'],
          'abbreviation': book_record['abbreviation'],
          'number': book_record['number'],
          'translation': translation,
      }
      current_chapter = None  # Reset the current chapter
      current_verses = []  # Reset the current verses

      # Append the book to the records_list
      records_list.append({
          'book': current_book,
          'chapters': []  # This will hold the chapters of this book
      })

    # Check if this is a new chapter
    if current_chapter is None or current_chapter['number'] != chapter:
      # Create a new chapter dictionary
      current_chapter = {
          'number': chapter,
          'verses': []  # This will hold the verses of this chapter
      }

      # Append the chapter to the chapters list of the current book
      records_list[-1]['chapters'].append(current_chapter)

    # Append the verse to the verses list of the current chapter
    current_chapter['verses'].append(record_dict)

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

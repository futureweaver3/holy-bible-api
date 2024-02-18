import os
from flask import Flask, jsonify, request

from constants import *
from utils import *

app = Flask(__name__)


def is_render():
  # Define the is_render function to check the environment variables
  return os.environ.get('RENDER') == 'true'


@app.route('/info')
def get_info_route():
  info_data = {
      "name": "Holy Bible API",
      "version": "1.0.0",
      "author": "Joseph Awad <futureweaver3@gmail.com>",
      "translations": TRANSLATIONS_NAMES,
      "production": is_render()
  }
  return jsonify(info_data)


@app.route('/bibles')
def get_bibles_route():
  return jsonify(TRANSLATIONS_NAMES)


@app.route('/bible')
@app.route('/bible:<translation>')
def get_bible_route(translation=DEFAULT_TRANSLATION):
  records = get_meta(TRANSLATIONS_PATHS[translation])
  # Return the records as JSON
  return jsonify(records)


@app.route('/books')
def get_books_route():
  return jsonify(BIBLE_BOOKS)


@app.route('/book_info/<book_abbreviation>')
def get_books_info_route(book_abbreviation):
  book_record = get_book_record(book_abbreviation)
  return jsonify(book_record)


@app.route('/verse/random')
@app.route('/verse/random:<translation>')
def get_random_verse_route(translation=DEFAULT_TRANSLATION):

  # Fetch a random verse from the SQLite database
  requested_verse = get_random_verse(translation)

  if len(requested_verse) < 1:
    return jsonify({'error': 'Verse not found'}), 404

  return jsonify(requested_verse)


@app.route('/verse/<book_abbreviation>:<chapter>:<verse>')
@app.route('/verse/<book_abbreviation>:<chapter>:<verse>:<translation>')
def get_verse_route(book_abbreviation, chapter, verse, translation=DEFAULT_TRANSLATION):
  book_record = get_book_record(book_abbreviation)
  if book_record is None:
    return jsonify({'error': 'Invalid book abbreviation'}), 400

  # Fetch the verse from the SQLite database using the book number, chapter number, and verse number
  requested_verse = fetch_verse_from_database(
    translation, book_record, chapter, verse)

  if len(requested_verse) < 1:
    return jsonify({'error': 'Verse not found'}), 404

  return jsonify(requested_verse)


@app.route('/verses/<book_abbreviation>:<chapter>:<verse_start>-<verse_end>')
@app.route('/verses/<book_abbreviation>:<chapter>:<verse_start>-<verse_end>:<translation>')
def get_verses_route(book_abbreviation, chapter, verse_start, verse_end, translation=DEFAULT_TRANSLATION):
  book_record = get_book_record(book_abbreviation)
  if book_record is None:
    return jsonify({'error': 'Invalid book abbreviation'}), 400

  # Fetch the verses from the SQLite database using the book number, chapter number, and verses range
  requested_verse = fetch_verses_from_database(
    translation, book_record, chapter, verse_start, verse_end)

  if len(requested_verse) < 1:
    return jsonify({'error': 'Verse not found'}), 404

  return jsonify(requested_verse)


@app.route('/chapter/<book_abbreviation>:<chapter>')
@app.route('/chapter/<book_abbreviation>:<chapter>:<translation>')
def get_chapter_route(book_abbreviation, chapter, translation=DEFAULT_TRANSLATION):
  print(book_abbreviation)
  book_record = get_book_record(book_abbreviation)
  if book_record is None:
    return jsonify({'error': 'Invalid book abbreviation'}), 400

  # Fetch the verses from the SQLite database using the book number, chapter number
  requested_verse = fetch_verses_from_database(
    translation, book_record, chapter, 1, 1000)

  if len(requested_verse) < 1:
    return jsonify({'error': 'Verse not found'}), 404

  return jsonify(requested_verse)


@app.route('/chapter_info/<book_abbreviation>:<chapter>')
@app.route('/chapter_info/<book_abbreviation>:<chapter>:<translation>')
def get_chapter_info_route(book_abbreviation, chapter, translation=DEFAULT_TRANSLATION):
  book_record = get_book_record(book_abbreviation)
  if book_record is None:
    return jsonify({'error': 'Invalid book abbreviation'}), 400

  chapter_info = get_number_of_verses(translation, book_record, chapter)

  if chapter_info is not None:
    return jsonify(chapter_info)
  else:
    return jsonify({'error': 'Chapter not found'}), 404


@app.route('/search')
def search_verses_route():
    # Get the search parameters from the query string
  words = request.args.get('words', None)
  if words is None or words == '':
    return jsonify({'error': 'Please provide at least one word to search'}), 400
  words = words.split(',')
  mode = request.args.get('mode', 'all')
  scope = request.args.get('scope', 'all')
  max_verses = int(request.args.get('max_verses', MAX_VERSES))
  translation = request.args.get('translation', DEFAULT_TRANSLATION)

  if scope not in ['all', 'old', 'new']:
    # Assume it is a book abbreviation
    book_record = get_book_record(scope)
    if book_record is None:
      return jsonify({'error': 'Invalid scope'}), 400
    scope = str(book_record['number'])

  # Search for verses with the specified words
  results = search_verses(
    words, mode, scope, max_verses, translation)

  if len(results) < 1:
    return jsonify({'error': 'Verse not found'}), 404

  # Return the results as JSON
  return jsonify(results)


if __name__ == '__main__':
  # Check if the app is running on render.com or not
  if not is_render():
    app.run(debug=True)  # Start Flask development server for local debugging

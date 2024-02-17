import os
from flask import Flask, jsonify

from constants import *
from utils import *

app = Flask(__name__)


def is_render():
  # Define the is_render function to check the environment variables
  return os.environ.get('RENDER') == 'true'


@app.route('/info')
def get_info():
  info_data = {
      "name": "Holy Bible API",
      "version": "1.0.0",
      "author": "Joseph Awad <futureweaver3@gmail.com>",
      "translations": TRANSLATIONS_NAMES,
      "production": is_render()
  }
  return jsonify(info_data)


@app.route('/bibles')
def get_bibles():
  return jsonify(TRANSLATIONS_NAMES)


@app.route('/bible')
@app.route('/bible:<translation>')
def bible(translation=DEFAULT_TRANSLATION):
  records = get_meta(TRANSLATIONS_PATHS[translation])
  # Return the records as JSON
  return jsonify(records)


@app.route('/books')
def get_books():
  return jsonify(BIBLE_BOOKS)


@app.route('/verse/<book_abbreviation><chapter>:<verse>')
@app.route('/verse/<book_abbreviation><chapter>:<verse>/<translation>')
def get_verse(book_abbreviation, chapter, verse, translation=DEFAULT_TRANSLATION):
  book_record = get_book_record(book_abbreviation)
  if book_record is None:
    return jsonify({'error': 'Invalid book abbreviation'}), 400

  # Fetch the verse from the SQLite database using the book number, chapter number, and verse number
  requested_verse = fetch_verse_from_database(
    translation, book_record, chapter, verse)

  if len(requested_verse) < 1:
    return jsonify({'error': 'Verse not found'}), 404

  return jsonify(requested_verse)


# if __name__ == '__main__':
#  app.run(debug=True)

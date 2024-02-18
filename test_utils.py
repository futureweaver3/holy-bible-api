import unittest
# from unittest.mock import AsyncMock, patch
from utils import *
from constants import *


class TestUtilsMethods(unittest.TestCase):

  def test_get_book_number(self):
    # Test the function with an existing book name
    book_name = 'Genesis'
    expected_result = 1
    actual_result = get_book_number(book_name)
    self.assertEqual(actual_result, expected_result)

    # Test the function with an existing book abbreviation
    book_abbreviation = 'gen'
    actual_result = get_book_number(book_abbreviation)
    self.assertEqual(actual_result, expected_result)

    # Test the function with a non-existing book name
    book_name = 'NonExistentBook'
    actual_result = get_book_number(book_name)
    self.assertIsNone(actual_result)

  def test_get_book_record(self):
    # Test the function with an existing book name
    book_name = 'Genesis'
    expected_result = {
        'name': 'genesis',
        'abbreviation': 'gen',
        'number': 1,
        'chapters': 50,
        'testament': 'old',
        'type': 'historical',
        'author': 'Moses',
        'language': 'Hebrew',
        'description': 'First book of the Bible, traditionally attributed to Moses.'
    }
    actual_result = get_book_record(book_name)
    self.assertEqual(actual_result, expected_result)

    # Test the function with an existing book abbreviation
    book_abbreviation = 'gen'
    actual_result = get_book_record(book_abbreviation)
    self.assertEqual(actual_result, expected_result)

    # Test the function with a non-existing book name
    book_name = 'NonExistentBook'
    actual_result = get_book_record(book_name)
    self.assertIsNone(actual_result)

  def test_get_book_record_by_number(self):
    # Test the function with an existing book number
    book_number = 1
    expected_result = {
        'name': 'genesis',
        'abbreviation': 'gen',
        'number': 1,
        'chapters': 50,
        'testament': 'old',
        'type': 'historical',
        'author': 'Moses',
        'language': 'Hebrew',
        'description': 'First book of the Bible, traditionally attributed to Moses.'
    }
    actual_result = get_book_record_by_number(book_number)
    self.assertEqual(actual_result, expected_result)

    # Test the function with a non-existing book number
    book_number = 100
    actual_result = get_book_record_by_number(book_number)
    self.assertIsNone(actual_result)

  def test_book_record_unpack(self):
    book_record = {
        'name': 'Genesis',
        'abbreviation': 'gen',
        'number': 1,
        'chapters': 50,
        'testament': 'old',
        'type': 'book',
        'author': 'Moses',
        'language': 'Hebrew',
        'description': 'The first book of the Bible, detailing the creation of the world and the origins of humanity.'
    }
    expected_result = (
        'Genesis',
        'gen',
        1,
        50,
        'old',
        'book',
        'Moses',
        'Hebrew',
        'The first book of the Bible, detailing the creation of the world and the origins of humanity.'
    )
    actual_result = book_record_unpack(book_record)
    self.assertEqual(actual_result, expected_result)

  def test_clean_unicode(self):
    # Test the function with a string containing Unicode characters
    value_with_unicode = 'Café'
    expected_result = 'Cafe'
    actual_result = clean_unicode(value_with_unicode)
    self.assertEqual(actual_result, expected_result)

    # Test the function with a string containing only ASCII characters
    value_without_unicode = 'Hello, world!'
    actual_result = clean_unicode(value_without_unicode)
    self.assertEqual(actual_result, value_without_unicode)

    # Test the function with a string containing leading and trailing whitespace
    value_with_whitespace = '  Hello, world!  '
    expected_result = 'Hello, world!'
    actual_result = clean_unicode(value_with_whitespace)
    self.assertEqual(actual_result, expected_result)


if __name__ == '__main__':
  # Create a TestLoader to load the tests
  loader = unittest.TestLoader()

  # Load the tests from the test classes
  suite = loader.loadTestsFromTestCase(TestUtilsMethods)
  # suite.addTests(loader.loadTestsFromTestCase(TestGetMeta))

  # Create a TextTestRunner to run the tests
  runner = unittest.TextTestRunner()

  # Run the tests
  result = runner.run(suite)

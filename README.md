# Holy Bible API

The Holy Bible API is a web API designed to provide access to the text and metadata of the Holy Bible. It allows users to retrieve information about different translations, books, chapters, verses, and perform searches on the text. The API is built using the Python Flask framework and uses an SQLite database to store the Bible text and metadata.

## Getting Started

To get started using the Holy Bible API, you'll need to install the required dependencies and set up the database. Follow the steps below:

- Clone the Holy Bible API repository from GitHub:

> git clone https://github.com/futureweaver3/holy-bible-api

- Navigate to the project directory:

> cd holy-bible-api

- Install the required dependencies:

> pip install -r requirements.txt

- Run the API:

> python app.py

## Routes

The Holy Bible API provides several routes for accessing different types of information. Here's a list of the available routes:<br /><br />

```
/info
```

This route provides general information about the API, including the available translations and the number of books in each translation.<br /><br />

```
/bibles
```

This route returns a list of available Bible translations.<br /><br />

```
/bible, /bible:<translation>
```

These routes return information about a specific Bible translation. The <translation> parameter can be used to specify the translation. If no translation is provided, the default translation is used.<br /><br />

```
/books
```

This route returns a list of books in the Bible.<br /><br />

```
/book/<book_abbreviation>
```

This route returns information about a specific book in the Bible, including its name, abbreviation, number, number of chapter, old/new testament, type, author, language, and description.<br /><br />

```
/verse/random, /verse/random:<translation>
```

These routes return a random verse from the Bible. The <translation> parameter can be used to specify the translation. If no translation is provided, the default translation is used.<br /><br />

```
/verse/<book_abbreviation>:<chapter>:<verse>,
/verse/<book_abbreviation>:<chapter>:<verse>:<translation>
```

These routes return a specific verse from the Bible. The <book_abbreviation>, <chapter>, and <verse> parameters are used to specify the location of the verse. The <book_abbreviation> can be the book name or its abbreviation. The <translation> parameter can be used to specify the translation. If no translation is provided, the default translation is used.<br /><br />

```
/verses/<book_abbreviation>:<chapter>:<verse_start>-<verse_end>,
/verses<book_abbreviation>:<chapter>:<verse_start>-<verse_end>:<translation>
```

These routes return a range of verses from the Bible. The <book_abbreviation>, <chapter>, <verse_start>, and <verse_end> parameters are used to specify the range of verses. The <book_abbreviation> can be the book name or its abbreviation. The <translation> parameter can be used to specify the translation. If no translation is provided, the default translation is used.<br /><br />

```
/chapter/<book_abbreviation>:<chapter>,
/chapter/<book_abbreviation>:<chapter>:<translation>
```

These routes return a specific chapter from the Bible. The <book_abbreviation> and <chapter> parameters are used to specify the location of the chapter. The <book_abbreviation> can be the book name or its abbreviation. The <translation> parameter can be used to specify the translation. If no translation is provided, the default translation is used.<br /><br />

```
/chapter_info/<book_abbreviation>:<chapter>,
/chapter_info/<book_abbreviation>:<chapter>:<translation>
```

These routes return information about a specific chapter from the Bible, including the number of verses and the translation. The <book_abbreviation> and <chapter> parameters are used to specify the location of the chapter. The <book_abbreviation> can be the book name or its abbreviation. The <translation> parameter can be used to specify the translation. If no translation is provided, the default translation is used.<br /><br />

```
/search
```

This route allows users to perform a search on the text of the Bible. The search query can be provided as a query parameter. For example, to search for the word "love", you would use the following URL: /search?words=love. You need a least one word to get a successful response. There are other parameters but they have a default values. Here is an example:

```
/search?words=love,peace&mode=any&scope=new&max=10&translation=asv
```

- **mode** can be **all** (Default value: find the verses that have all the words) or **any** (find the verses that have any of the words).
- **scope** can be **all** (Default value: all the bible), **old** (old testament), **new** (new testament), or **book name or abbreviation** (limit the search to this book only).
- **max** is the maximum number of verses requested. The default value is 200.
- **translation** is bible translation wanted for the search. The default value is kjv.<br /><br />

## Testing

You may evaluate this API by accessing the following server: [holy-bible-api](https://holy-bible-api.onrender.com/). However, please refrain from integrating it into your applications, as it operates on a free server with usage limitations. Its primary purpose is to facilitate other developers in testing the API before incorporating it into their projects. Do note that the initial API response may take approximately 50 seconds to wake up the server. Subsequent requests should be considerably faster. You're welcome to clone and deploy it on your own server for the greater purpose of serving God.

## Conclusion

The Holy Bible API provides a convenient way to access the text and metadata of the Holy Bible. Whether you're a developer looking to build a Bible-related application or a researcher looking for specific information, the Holy Bible API has you covered. With its simple and intuitive interface, you can easily access the information you need. Happy coding!<br /><br />

## Author

Future Weaver [futureweaver3@gmail.com](mailto:futureweaver3@gmail.com)

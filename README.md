# Meme Generator

This Meme Generator provides the functionalities and a flask app to generate Memes with a quote.

## Setting up and running the program

To setup the environment, run:

``` bash
pip install -r requirements.txt
```

The main function lies in `./meme.py`. To run it, execute for example the following in the terminal:
``` bash
python3 meme.py --help
```

If there are no arguments supplied:
``` bash
python3 meme.py
```
a random image from `./_data/photos/dog` directory and a random quote from the files in `./_data/DogQuotes` directory would be used.

If there are no image supplied:
``` bash
python3 meme.py --body "I never lose. Either I win or I learn." --author "Nelson Mandela"
```
a random image from `./_data/photos/dog` directory would be used.

To start the flask app:

```bash
export FLASK_APP=app.py
flask run --host 0.0.0.0 --port 3000 --reload
```

Then the application can be accessible on the local host: `http://127.0.0.1:3000/`

## Components

The sub-modules `quote_engine` digests quotes from files and hold the quotes as `QuoteModel` objects in memory.
Supported file types for ingestion currently are `.txt`, `.docx`, `.pdf`, `.csv`.
The abstract base class defining the ingester interface and the concrete helper classes are in `./quote_engine/ingestor_utils.py`.

The sub-module `meme_engine` read an image, resize it to a maximum width (in pixels) while maintaining the aspect ratio, add the quote caption on the image, and eventually creates memes.

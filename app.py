import random
import os
import requests
from flask import Flask, render_template, after_this_request, request
from quote_engine.ingestor import Ingestor
from meme_engine.meme_engine import MemeEngine

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """ Load all resources """
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']
    quotes = []
    for quote_file in quote_files:
        quotes.extend(Ingestor.parse(quote_file))

    images_path = "./_data/photos/dog/"
    imgs = []
    for root, _, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    img = random.choice(imgs)
    quote = random.choice(quotes)

    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """
    image_url = request.form.get('image_url')
    body = request.form.get('body')
    author = request.form.get('author')
    if not image_url:
        image_url = 'https://static.bimago.pl/mediacache/catalog/product/cache/1/2/146221/image/1500x2240/c0d39395fd4eb0df2112dbf1bd103f89/146221_2.jpg'
    if not body:
        body = "Don't wish for a meme, create a meme!"
    if not author:
        author = "Meme Generator"

    temp_img_path = "./tmp/downloaded_img.jpg"

    # 1. Use requests to save the image from the image_url form param to a temp local file.
    r = requests.get(image_url)
    if r.status_code == 200:
        with open(temp_img_path, 'wb') as f:
            f.write(r.content)
    del r

    # 2. Use the meme object to generate a meme using this temp file and the body and author form paramaters.
    path = meme.make_meme(temp_img_path, body, author)

    # 3. Remove the temporary saved image.
    @after_this_request
    def cleanup(response):
        os.remove(temp_img_path)
        return response

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()

from flask import Flask,render_template,request,make_response,Response,stream_with_context,render_template_string
import prox
from flask_bootstrap import Bootstrap
from glob import glob
import os
import random


app = Flask(__name__)
bootstrap = Bootstrap(app)

#TODO:Use bootstrap

url = ""
deck = None

@app.route('/')
def index():

    global url
    global deck

    for pdf_file in glob("static/*.pdf"):
        os.remove(pdf_file)

    return render_template('index.html')

@app.route('/result',methods=["GET"])
def ResultPage():

    global url
    global deck

    url = request.args.get('name')
    print(url)
    d = prox.Deck(url)
    d.scrape()
    deck = d.deck
    card_id_list = [i[2] for i in deck]
    print(card_id_list)
    def f():
        for id in card_id_list:
            image_file = "static/imdir/" + id + ".jpg"
            if not os.path.exists(image_file):
                d.download_img(id)
    return render_template('result.html',deck=deck,f_name="imdir",func=f())

#TODO:Fix the routing => /result_pdf/id
@app.route('/result_pdf',methods=["POST","GET"])
def PDFPage():

    global url
    global deck

    card_id_list = [i[2] for i in deck]

    f_info = zip(request.form.getlist("more_than_zero"),request.form.getlist("card_num"),card_id_list)
    p = prox.PDF_generater(url)
    p.make_pdf(f_info)
    binary_pdf = open("static/" + url.lstrip("https://www.pokemon-card.com/deck/confirm.html/deckID/").rstrip("/") +".pdf","rb").read()
    response = make_response(binary_pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
        'inline; filename=%s.pdf' % 'yourfilename'
    return response

@app.route('/play_ground',methods=["POST","GET"])
def play_ground():
    global deck
    new_deck = []
    for _, _, idx, number in deck:
        for _ in range(int(number.rstrip("枚"))):
            new_deck.append(idx)
    random.shuffle(new_deck)
    hand = new_deck[:7]
    side = new_deck[7:13]
    rest_deck = new_deck[13:]
    return render_template("play_ground.html",hand=hand,side=side,deck=rest_deck)

if __name__ == '__main__':
    app.run()
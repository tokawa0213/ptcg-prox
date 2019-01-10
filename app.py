from flask import Flask,render_template,request,make_response,Response,stream_with_context,render_template_string
import prox
from flask_bootstrap import Bootstrap
import shutil
from glob import glob
import os
import re

#TODO: static/imdir => exclude non gx poke

app = Flask(__name__)
bootstrap = Bootstrap(app)

#TODO:Use bootstrap

url = ""
card_id_list = []

@app.route('/')
def index():

    global url
    global card_id_list

    url = ""
    card_id_list = []

    for pdf_file in glob("static/*.pdf"):
        os.remove(pdf_file)

    return render_template('index.html')

#TODO:Fix the routing => /result/deck_id

@app.route('/result',methods=["POST","GET"])
def ResultPage():

    global url
    global card_id_list

    try:
        url = request.form['name']
    except:
        pass

    d = prox.Deck(url)
    d.scrape()
    card_id_list = [i[2] for i in d.deck]

    for id in card_id_list:
        image_file = "static/imdir/" + id + ".jpg"
        if not os.path.exists(image_file):
            d.download_img(id)
    return render_template('result.html',deck=d.deck,f_name="imdir")

#TODO:Fix the routing => /result_pdf/id
@app.route('/result_pdf',methods=["POST","GET"])
def PDFPage():

    global url
    global card_id_list

    if not os.path.exists("static/" + url.lstrip("https://www.pokemon-card.com/deck/confirm.html/deckID/").rstrip("/") +".pdf"):
        f_info = zip(request.form.getlist("more_than_zero"),request.form.getlist("card_num"),card_id_list)
        p = prox.PDF_generater(url)
        p.make_pdf(f_info)
    binary_pdf = open("static/" + url.lstrip("https://www.pokemon-card.com/deck/confirm.html/deckID/").rstrip("/") +".pdf","rb").read()
    response = make_response(binary_pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
        'inline; filename=%s.pdf' % 'yourfilename'
    return response

if __name__ == '__main__':
    app.run()
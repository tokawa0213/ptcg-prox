from flask import Flask,render_template,request,make_response,Response,stream_with_context,render_template_string,session
import prox
from flask_bootstrap import Bootstrap
from glob import glob
import os
import random
import re
import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask_httpauth import HTTPBasicAuth

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
auth = HTTPBasicAuth()
app.secret_key=os.environ.get("SECRET_KEY")

users = {
    os.environ.get("ROOT_USER"): os.environ.get("PASSWORD"),
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():

    #vulnerable to edittable url

    for pdf_file in glob("static/*.pdf"):
        os.remove(pdf_file)

    return render_template('index.html')

@app.route('/result',methods=["GET"])
@auth.login_required
def ResultPage():
    if request.args.get('name') != 'failure':
        session["url"] = prox.change_url(request.args.get('name'))

        d = prox.Deck(session["url"])
        d.scrape()
        session["deck"] = d.deck
        card_id_list = [i[2] for i in session["deck"]]
        def f():
            for id in card_id_list:
                image_file = "static/imdir/" + id + ".jpg"
                if not os.path.exists(image_file):
                    d.download_img(id)
            return "false"
        return render_template('result.html',deck=session["deck"],f_name="imdir",func=f)
    else:
        pass

#TODO:Fix the routing => /result_pdf/id
@app.route('/result_pdf',methods=["POST","GET"])
@auth.login_required
def PDFPage():

    card_id_list = [i[2] for i in session["deck"]]

    f_info = zip(request.form.getlist("more_than_zero"),request.form.getlist("card_num"),card_id_list)
    p = prox.PDF_generater(session["url"])
    binary_pdf = p.make_pdf(f_info)

    #binary_pdf = open("static/" + session["url"].lstrip("https://www.pokemon-card.com/deck/confirm.html/deckID/").rstrip("/") +".pdf","rb").read()
    response = make_response(binary_pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
        'inline; filename=%s.pdf' % 'yourfilename'
    return response

@app.route('/play_ground',methods=["POST","GET"])
@auth.login_required
def play_ground():

    new_deck = []
    for _, _, idx, number in session["deck"]:
        for _ in range(int(number.rstrip("枚"))):
            new_deck.append(idx)
    random.shuffle(new_deck)
    hand = new_deck[:7]
    side = new_deck[7:13]
    rest_deck = new_deck[13:]
    return render_template("play_ground.html",hand=hand,side=side,deck=rest_deck)

if __name__ == '__main__':
    app.run()
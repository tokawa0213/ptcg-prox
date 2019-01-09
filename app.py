from flask import Flask,render_template,request,make_response,Response,stream_with_context,render_template_string
import prox
from flask_bootstrap import Bootstrap
import shutil
from glob import glob
import os


app = Flask(__name__)
bootstrap = Bootstrap(app)

#TODO:Use bootstrap
#TODO:Build a DB and don't download everytime?
#TODO: import os os.path.gettime
url = ""
card_id_list = []

@app.route('/')
def index():
    return render_template('index.html')
#TODO: Fix time out error
#TODO:Fix the routing => /result/deck_id

@app.route('/result',methods=["POST"])
def ResultPage():

    global url
    global card_id_list

    url = request.form['name']

    inside_data_folder = glob("static/*")
    if len(inside_data_folder) >= 10:
        time_folder = [os.path.getctime(folder) for folder in inside_data_folder]
        shutil.rmtree(glob(inside_data_folder[time_folder.index(sorted(time_folder,reverse=True)[1])]))

    d = prox.Deck(url)
    d.scrape()
    #d.download_img()
    new_name = url.lstrip("https://www.pokemon-card.com/deck/confirm.html/deckID/").rstrip("/")
    print(d.deck)
    card_id_list = [i[2] for i in d.deck]
    for id in card_id_list:
        image_file = "static/imdir/" + id + ".jpg"
        if not os.path.exists(image_file):
            os.system(
                "aria2c -x 16 -s 16  -o " + "static/img" + "/" + id + ".jpg" + " " + "https://www.pokemon-card.com/card-search/details.php/card/" + id
            )
    return render_template('result.html',deck=d.deck,f_name="imdir")
    '''
    gen = d.download_img()
    def generate_output():
        i = gen.__next__()
        while True:
            try:
                yield render_template('result.html',deck=enumerate(d.deck),f_name=new_name,loaded_img=i)
            except:
                break
            i = gen.__next__()
    return Response(stream_with_context(generate_output()))
    #return redirect('/result')
    #return Response(stream_template('result.html',loaded_img=gen,deck=enumerate(d.deck),f_name=new_name))
    '''
#TODO:Fix the routing => /result_pdf/id
@app.route('/result_pdf',methods=["POST"])
def PDFPage():

    global url
    global card_id_list

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
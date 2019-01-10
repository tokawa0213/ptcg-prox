from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from PIL import Image
from io import BytesIO
from glob import glob

def name_search(name):
    uri = "https://www.pokemon-card.com/card-search/index.php?keyword="+ name +"&regulation_header_search_item0=XY&sm_and_keyword=true"


def search(i):
    id = ["Name","Illust","Img","Pack","Goods","SpEn","Support","Stadium","AnAbName","AnAbDisc","AbName","AbDisc","Move1","Move2","Move3","Evo","What","HP","Type","Weak","Res","Ret","link"]
    val = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
    d = {
        "c_id":i,
        "Name":None,
        "Illust":None,
        "Img":None,
        "Pack":None,
        "Goods":False,
        "SpEn":False,
        "Support":False,
        "Stadium":False,
        "AnAbName":False,
        "AnAbDisc": False,
        "AbName":False,
        "AbDisc":False,
        "Move1":[],
        "Move2":[],
        "Move3":[],
        "Evo":False,
        "What":False,
        "HP":False,
        "Type":False,
        "Weak":False,
        "Res":False,
        "Ret":False,
        "Link":None
    }

    #max 35278
    #min 30001
    num = str(i)
    url = "https://www.pokemon-card.com/card-search/details.php/card/" + num
    d["Link"] = url
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"lxml")
    #name
    d["Name"] = soup.find("title").text.split()[0]

    #illust
    try:
        d["Illust"] = soup.find(class_ = "author").a.text
    except:
        pass

    #image
    try:
        r = requests.get("https://www.pokemon-card.com" +soup.find(class_ = "fit").get("src"))
    except:
        return
    # ability_list
    ability = [i.text for i in soup.findAll("h2")]
    try:
        ability_name = soup.find(class_="RightBox-inner").findAll("h4")
    except:
        pass
    try:
        ability_exp = soup.find(class_="RightBox-inner").findAll("p")
    except:
        pass

    ability_exp = [i for i in ability_exp if i.text != "グッズは、自分の番に何枚でも使える。" and
                   i.text != "スタジアムは、自分の番に1枚だけ、バトル場の横に出せる。別の名前のスタジアムが場に出たなら、このカードをトラッシュする。" and
                   i.text != "サポートは、自分の番に1枚しか使えない。" and
                   i.text != "グッズは、自分の番に何枚でも使える。" and
                   i.text != "ポケモンのどうぐは、自分のポケモンにつけて使う。ポケモン1匹につき1枚だけつけられ、つけたままにする。"]

    #pack
    d["Pack"] = soup.find(class_ = "Link Link-arrow").text

    for i in ability:
        if i == "グッズ" or i == "ポケモンのどうぐ":
            d["Goods"] = ability_exp.pop(0).text
        elif i == "特殊エネルギー":
            d["SpEn"] = ability_exp.pop(0).text
        elif i == "基本エネルギー":
            return
        elif i == "サポート":
            d["Support"] = ability_exp.pop(0).text
        elif i == "スタジアム":
            d["Stadium"] = ability_exp.pop(0).text
        elif i == "古代能力":
            d["AnAbName"] = ability_name.pop(0).text
            d["AnAbDisc"] = ability_exp.pop(0).text
        elif i == "特性":
            d["AbName"] = ability_name.pop(0).text
            d["AbDisc"] = ability_exp.pop(0).text
        elif i == "ワザ":
            temp = ""
            for i in ability_name[0].findAll("span"):
                if (i.get("class")[0].startswith("icon-")):
                    temp += i.get("class")[0].lstrip("icon-") + "="
            temp = temp.rstrip("=")
            d["Move1"] = temp + "-" + ability_name.pop(0).text + "-" + ability_exp.pop(0).text
        elif i == "特別なルール":
            #print(ability_exp.pop(0).text)
            pass
        elif i == "進化":
            pass
        else:
            pass
            #print("ADD ANOTHER FEATURE")
            #print(i)
    if ability_name != [] and ability_exp != []:
        temp = ""
        for i in ability_name[0].findAll("span"):
            if (i.get("class")[0].startswith("icon-")):
                temp += i.get("class")[0].lstrip("icon-") + "="
        temp = temp.rstrip("=")
        d["Move2"] = temp + "-" + ability_name.pop(0).text + "-" + ability_exp.pop(0).text
    if ability_name != [] and ability_exp != []:
        temp = ""
        for i in ability_name[0].findAll("span"):
            if (i.get("class")[0].startswith("icon-")):
                temp += i.get("class")[0].lstrip("icon-") + "="
        temp = temp.rstrip("=")
        d["Move3"] = temp + "-" + ability_name.pop(0).text + "-" + ability_exp.pop(0).text
    #tane/ichishinnka/nishinnka

    try:
        d["What"] = soup.find(class_ = "type").text
        #hp
        d["HP"] = soup.find(class_="hp-num").text
        #type
        temp = ""
        typ = soup.find(class_ = "TopInfo")
        typ = typ.findAll(class_ = re.compile("icon-[^\s]+ icon"))
        for i in typ:
            temp += i.get("class")[0].lstrip("icon-") + "-"
        temp = temp.rstrip("-")
        d["Type"] = temp
        weak_res_ret = soup.findAll("td")
    except:
        #pandas
        #data = pd.DataFrame([d.values()],columns=d.keys())
        #data.to_csv('out.csv',encoding="utf-8", mode='a')
        return d
    try:
        d["Weak"] = weak_res_ret[0].span.get("class")[0].lstrip("icon-")
    except:
        pass
    try:
        d["Res"] = weak_res_ret[1].span.get("class")[0].lstrip("icon-")
    except:
        pass
    try:
        d["Ret"] = len(weak_res_ret[2].findAll("span"))
    except:
        ret = "None"
    if d["HP"] == None or d["Name"].endswith("GX"):
        try:
            img = Image.open(BytesIO(r.content))
            img.save("./static/imdir/" + num + ".jpg")
            d["Img"] = "./static/imdir/" + num + ".jpg"
        except:
            d["Img"] = "TODO : Insert GIF"
    return d

#TODO: CHECK THE CARD ID ! THIS RANGE IS VERY TEKITO=
if __name__ == "__main__":
    #33553 : start of Best of XY
    #33851 : End of Nest of XY
    try:
        m = 33000 + len(glob("static/imdir/*"))-1
    except:
        m = 33000
        #sun moon regu
    for i in range(m+1,40000):
        print(i)
        d = search(i)
        if d == None:
            continue
        print(d)
        #data = pd.DataFrame([d.values()])
        #data.to_csv('out.csv', index=False, encoding="utf-8", mode='a',header=False)
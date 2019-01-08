import sqlite3
from glob import glob
import pickle

db = sqlite3.connect("./static/sample.db",isolation_level=None)
cursor = db.cursor()

try:
    cursor.execute("CREATE TABLE data_set(id,img)")
except:
    pass
p = "INSERT INTO data_set(id, img) VALUES(?, ?)"

id_to_img = {}

for img_path in glob("static/imdir/*.jpg"):
    img_id = img_path.lstrip("static/imdir/").rstrip(".jpg")
    with open(img_path,"rb") as f:
        id_to_img[img_id] = f.read()
for id,img in id_to_img.items():
    cursor.execute(p, (id,img))
db.close()
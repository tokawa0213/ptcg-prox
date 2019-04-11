FROM python:3
RUN virtualenv -p python3 /env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
ADD . /app/
# こんなのを加えるとスムーズに環境構築されると思います。
RUN pip install -r requirements.txt
CMD python app.py
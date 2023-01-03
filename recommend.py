import pandas as pd
import numpy as np
from flask import Flask, render_template, request
import pickle

popular_df = pickle.load(open('top50.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))
# =pickle.load(open('final.pkl','rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html",
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           rating=list(popular_df['Avg Rating'].values),
                           votes=list(popular_df['num Rating'].values),
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


def detail(book_name):
    temp = books[books["Book-Title"] == book_name]
    item = []
    item.append(list(temp["Book-Title"])[0])
    item.append(list(temp["Book-Author"])[0])
    item.append(list(temp["Image-URL-M"])[0])
    return item


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    if user_input in pt.index:
        index = np.where([pt.index == user_input])[1][0]
        distance = sorted(
            list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)
        similar_books = distance[1:5]
        book_list = [pt.index[x[0]] for x in similar_books]
        book_list = list(map(lambda x: detail(x), book_list))
        # print(book_list)
        return render_template('recommend.html', data=book_list)
    else:
        return f'{user_input} is not in Top-50 Books'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

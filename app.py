from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
recommend_data = pickle.load(open('recommend_data.pkl','rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values[:50]),
                           author=list(popular_df['Book-Author'].values[:50]),
                           publisher=list(popular_df['Publisher'].values[:50]),
                           image=list(popular_df['Image-URL-M'].values[:50]),
                           year=list(popular_df['Year-Of-Publication'].values[:50]),
                           ratings=list(popular_df['avg_ratings'].values.round(decimals=1)[:50]),
                           votes=list(popular_df['Num_ratings'].values[:50]))

@app.route('/sort', methods=['POST'])
def sort():
    sort_option = request.form.get('sortOption', '').strip()

    if sort_option == 'year':
        sorted_books = popular_df.sort_values(by='Year-Of-Publication')
    elif sort_option == 'popular':
        sorted_books = popular_df.sort_values(by='Num_ratings',ascending=False)
    else:
        sorted_books = popular_df

    return render_template('index.html', book_name=list(sorted_books['Book-Title'].values[:100]),
                           author=list(sorted_books['Book-Author'].values[:100]),
                           publisher=list(sorted_books['Publisher'].values[:100]),
                           image=list(sorted_books['Image-URL-M'].values[:100]),
                           year=list(sorted_books['Year-Of-Publication'].values[:100]),
                           ratings=list(sorted_books['avg_ratings'].values.round(decimals=1)[:100]),
                           votes=list(sorted_books['Num_ratings'].values[:100]))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    book = str(request.form.get('book'))
    for i in pt.index:
        if i.lower() == book.lower():
            index = np.where(pt.index == i)[0][0]
            distances = sorted(list(enumerate((similarity[index]))), key=lambda x: x[1], reverse=True)[:6]
            title = []
            image = []
            author = []
            year = []
            num_range = range(1,6)

            for i in distances:
                title.append(pt.index[i[0]])
                image.append(recommend_data[recommend_data['Book-Title'] == pt.index[i[0]]]['Image-URL-M'][:1].values[0])
                author.append(recommend_data[recommend_data['Book-Title'] == pt.index[i[0]]]['Book-Author'][:1].values[0])
                year.append(recommend_data[recommend_data['Book-Title'] == pt.index[i[0]]]['Year-Of-Publication'][:1].values[0])
            return render_template('recommend.html',
                                   title=title, image=image, author=author, year=year, num_range=num_range)
    else:
        return 'No books found named {}'.format(book)


if __name__=='__main__':
    app.debug = True
    app.run()
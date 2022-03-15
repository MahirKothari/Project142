import csv
from flask import Flask , jsonify , request
import csv
from storage import all_articles,liked_articles,not_liked_articles,did_not_watch
from Demographicfiltering import output
from Contentfiltering import getRecommendations
all_articles = []
with open('articles.csv',encoding = 'utf8') as f:
    reader = csv.reader(f)
    data = list(reader)
    all_articles = data[1:]
liked_articles = []
not_liked_articles = []
app = Flask(__name__)
@app.route('/get-article')
def getArticle():
    return jsonify({
        'data': all_articles[0],
        'status':'success'
    })
@app.route('/liked-articles',methods = ['POST'])
def liked_article():
    article = all_articles[0]
    all_articles = all_articles[1:]
    liked_articles.append(article)
    return jsonify({
        'status':'success'
    }),201
@app.route('/unliked-article',methods = ['POST'])
def not_liked_article():
    article = all_articles[0]
    all_articles = all_articles[1:]
    not_liked_articles.append(article)
    return jsonify({
        'status':'success'
    }),201
@app.route('/popular-articles')
def popular_articles():
    article_data = []
    for article in output:
        d = {
            'url' : article[0],
            'title' : article[1],
            'text' : article[2],
            'lang' : article[3],
            'total_events' : article[4],
        }
        article_data.append(d)
    return jsonify({
        'data': article_data,
        'status':'success'
    })
@app.route('/recommended-articles')
def recommended_articles():
    all_recommended = []
    for liked_article in liked_articles:
        output = getRecommendations(liked_article[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended in itertools.groupby(all_recommended))
    article_data = []
    for article in all_recommended:
        d = {
            'url' : article[0],
            'title' : article[1],
            'text' : article[2],
            'lang' : article[3],
            'total_events' : article[4],           
        }
        article_data.append(d)
    return jsonify({
        'data': article_data,
        'status':'success'
    })
if __name__ == '__main__':
    app.run()
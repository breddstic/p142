from flask import Flask, jsonify, request
import pandas as pd
from content_filtering import get_recommendations
from demographic_filtering import output
app = Flask(__name__)
articles_data = pd.read_csv("articles.csv")
liked_articles = []
not_liked_articles = []
all_articles = articles_data[['url', 'title', 'text', 'lang', 'total_events']]
@app.route("/get-article")
def get_article():
    article_data = {
        "title": all_articles[0][19],
        "poster_link": all_articles[0][27],
        "release_date": all_articles[0][13] or "N/A",
        "duration": all_articles[0][15],
        "rating": all_articles[0][20],
        "overview": all_articles[0][9]
    }
    return jsonify({
        "data": article_data,
        "status": "success"
    })

@app.route("/liked-article", methods=["POST"])
def liked_article():
    article = all_articles[0]
    liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/unliked-article", methods=["POST"])
def unliked_article():
    article = all_articles[0]
    not_liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/popular-articles")
def popular_articles():
    article_data = []
    for article in output:
        _d = {
            "title": article[0],
            "poster_link": article[1],
            "release_date": article[2] or "N/A",
            "duration": article[3],
            "rating": article[4],
            "overview": article[5]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    article_data = []
    for recommended in all_recommended:
        _d = {
            "title": recommended[0],
            "poster_link": recommended[1],
            "release_date": recommended[2] or "N/A",
            "duration": recommended[3],
            "rating": recommended[4],
            "overview": recommended[5]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

if __name__ == "__main__":
  app.run()
from flask import Flask, send_from_directory, request, escape, render_template, jsonify

from task5.search import search_page, search_with_ranging_tf_idf

app = Flask(__name__)


@app.route("/")
def index():
    print("hello")
    return render_template('index.html')


@app.route("/search")
def search():
    query = str(escape(request.args.get("query", "")))
    print("QUERY ", query)
    result = search_with_ranging_tf_idf(query)
    json = []
    for key, value in result.items():
        json.append({'link': key, 'title': value})
    print(json)
    return jsonify(json)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

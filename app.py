from flask import Flask, send_from_directory
from api.words import words_api
from api.game import game_api

app = Flask(__name__, static_folder='static')

# 注册 Blueprint，不加前缀
app.register_blueprint(words_api)
app.register_blueprint(game_api)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
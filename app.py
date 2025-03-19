from flask import Flask, send_from_directory, request, jsonify
from api.words import words_api
from api.game import game_api
from api.scores import scores_api
import os
import glob
import pandas as pd

app = Flask(__name__, static_folder='static')

app.register_blueprint(words_api)
app.register_blueprint(game_api)
app.register_blueprint(scores_api)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/upload_words', methods=['POST'])
def upload_words():
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)
    existing_files = glob.glob(os.path.join(data_dir, 'words*.csv'))
    new_file_num = len(existing_files) + 1
    new_file = os.path.join(data_dir, f'words{new_file_num}.csv')

    if 'file' in request.files:
        file = request.files['file']
        if file.filename.endswith('.csv'):
            file.save(new_file)
    elif 'text' in request.form:
        text = request.form['text']
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(text)
    else:
        return jsonify({'error': 'Invalid input'}), 400

    # 更新中转缓存文件
    update_game_words()
    return jsonify({'message': 'Words added successfully'})

def update_game_words():
    data_dir = 'data'
    default_file = os.path.join(data_dir, 'default_words.csv')
    game_file = os.path.join(data_dir, 'game_words.csv')
    word_files = glob.glob(os.path.join(data_dir, 'words*.csv'))

    all_words = []
    # 如果有用户添加的单词库，读取所有文件
    if word_files:
        for wf in word_files:
            try:
                df = pd.read_csv(wf)
                all_words.extend(df.to_dict(orient='records'))
            except Exception as e:
                print(f"Error reading {wf}: {e}")
    # 否则使用默认文件
    else:
        try:
            df = pd.read_csv(default_file)
            all_words = df.to_dict(orient='records')
        except Exception as e:
            print(f"Error reading default file: {e}")
            all_words = []

    # 保存到中转文件
    if all_words:
        df = pd.DataFrame(all_words)
        df.to_csv(game_file, index=False, encoding='utf-8')

if __name__ == '__main__':
    update_game_words()  # 启动时更新缓存
    app.run(debug=True)
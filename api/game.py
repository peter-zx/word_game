from flask import Blueprint, jsonify, request
from utils.words_util import load_words_from_csv
import random

game_api = Blueprint('game_api', __name__)

@game_api.route('/game', methods=['GET'])
def get_game():
    words = load_words_from_csv('data/words.csv')
    if not words:
        return jsonify({'error': 'No words found'}), 404

    # 随机选择 4 个单词（4 对英文-中文）
    selected_words = random.sample(words, min(4, len(words)))
    game_items = []
    for word in selected_words:
        game_items.append({'type': 'english', 'value': word['english'], 'pair': word['chinese']})
        game_items.append({'type': 'chinese', 'value': word['chinese'], 'pair': word['english']})

    # 打乱顺序并生成网格
    random.shuffle(game_items)
    game_grid = []
    word_ids = {}
    for i, item in enumerate(game_items):
        word_ids[i] = item
        game_grid.append({'id': i, 'value': item['value']})

    return jsonify({'grid': game_grid, 'word_ids': word_ids})

@game_api.route('/check', methods=['POST'])
def check_pair():
    data = request.get_json()
    word1_id = data.get('word1_id')
    word2_id = data.get('word2_id')
    word_ids = data.get('word_ids')

    if word1_id is None or word2_id is None or word_ids is None:
        return jsonify({'error': 'Invalid request'}), 400

    word1 = word_ids.get(str(word1_id))  # 键可能是字符串
    word2 = word_ids.get(str(word2_id))

    if word1 is None or word2 is None:
        return jsonify({'error': 'Invalid word IDs'}), 400

    # 检查是否匹配
    if word1['value'] == word2['pair'] and word2['value'] == word1['pair']:
        return jsonify({'result': True})
    return jsonify({'result': False})
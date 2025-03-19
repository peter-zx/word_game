from flask import Blueprint, jsonify, request
from utils.words_util import load_words_from_csv
import random

game_api = Blueprint('game_api', __name__)

@game_api.route('/game/<level>', methods=['GET'])
def get_game(level):
    words = load_words_from_csv('data/words.csv')
    if not words:
        return jsonify({'error': 'No words found'}), 404

    # 根据难度级别设置行数
    level_map = {'lv1': 4, 'lv2': 5, 'lv3': 6, 'lv4': 7, 'lv5': 8, 'lv6': 9}
    rows = level_map.get(level.lower(), 4)  # 默认 Lv1
    pair_count = min(rows, len(words))

    # 随机选择单词对
    selected_words = random.sample(words, pair_count)
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

    word1 = word_ids.get(str(word1_id))
    word2 = word_ids.get(str(word2_id))

    if word1 is None or word2 is None:
        return jsonify({'error': 'Invalid word IDs'}), 400

    if word1['value'] == word2['pair'] and word2['value'] == word1['pair']:
        return jsonify({'result': True})
    return jsonify({'result': False})
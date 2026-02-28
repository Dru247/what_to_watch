"""API."""
from flask import jsonify, request

from opinions_app import app, db
from .error_handlers import InvalidAPIUsage
from .models import Opinion
from .views import random_opinion


@app.route('/api/opinions/<int:id>/', methods=['GET'])
def get_opinion(id):
    """Получение мнения по id."""
    opinion = Opinion.query.get(id)
    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)
    return jsonify({'opinion': opinion.to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['PATCH'])
def update_opinion(id):
    """Обновление мнения по id."""
    data = request.get_json()
    if (
        'text' in data and
        Opinion.query.filter_by(text=data['text']).first() is not None
    ):
        raise InvalidAPIUsage('Такое мнение уже есть в базе данных')
    opinion = Opinion.query.get(id)
    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)
    opinion.title = data.get('title', opinion.title)
    opinion.text = data.get('text', opinion.text)
    opinion.source = data.get('source', opinion.source)
    opinion.added_by = data.get('added_by', opinion.added_by)
    db.session.commit()
    return jsonify({'error': 'Такое мнение уже усть в базе данных'}), 400


@app.route('/api/opinions/<int:id>/', methods=['DELETE'])
def delete_opinion(id):
    """Удаляет мнение по id."""
    opinion = Opinion.query.get(id)
    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)
    db.session.delete(opinion)
    db.session.commit()
    return '', 204


@app.route('/api/opinions/', methods=['GET'])
def get_opinions():
    """Получение всех мнений."""
    opinions = Opinion.query.all()
    opinions_data = [opinion.to_dict() for opinion in opinions]
    return jsonify({'opinions': opinions_data}), 200


@app.route('/api/opinions/', methods=['POST'])
def add_opinion():
    """Добавляет мнение."""
    data = request.get_json()
    if 'title' not in data or 'text' not in data:
        raise InvalidAPIUsage('В запросе отсутствуют обязательные поля')

    if Opinion.query.filter_by(text=data['text']).first() is not None:
        raise InvalidAPIUsage('Такое мнение уже есть в базе данных')

    opinion = Opinion()
    opinion.from_dict(data)
    db.session.add(opinion)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201


@app.route('/api/get-random-opinion/', methods=['GET'])
def get_random_opinion():
    """Возвращает случайное мнение."""
    opinion = random_opinion()
    if opinion is not None:
        return jsonify({'opinion': opinion.to_dict()}), 200
    raise InvalidAPIUsage('В базе данных нет мнений', 404)

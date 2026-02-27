"""Обработчики."""
from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from opinions_app import app, db
from .forms import OpinionForm
from .models import Opinion


@app.route('/')
def index_view():
    """Главная страница."""
    quantity = Opinion.query.count()

    if not quantity:
        abort(500)

    # Выбирает случайное число в диапазоне от 0 до quantity
    offset_value = randrange(quantity)
    opinion = Opinion.query.offset(offset_value).first()
    return render_template('opinion.html', opinion=opinion)


@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    """Страница добавления мнения."""
    form = OpinionForm()
    if form.validate_on_submit():
        text = form.text.data
        if Opinion.query.filter_by(text=text).first() is not None:
            flash('Такое мнение уже было оставлено ранее!')
            return render_template('add_opinion.html', form=form)
        opinion = Opinion(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)


@app.route('/opinions/<int:id>')
def opinion_view(id):
    """Страница отображения мнения."""
    opinion = Opinion.query.get_or_404(id)
    return render_template('opinion.html', opinion=opinion)

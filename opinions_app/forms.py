"""Формы приложения."""
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, MultipleFileField
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional


class OpinionForm(FlaskForm):
    """Форма мнения."""
    title = StringField(
        'Заголовок',
        validators=[DataRequired(), Length(max=100)]
    )
    text = TextAreaField('Текст', validators=[DataRequired()])
    source = URLField(
        'Добавьте ссылку на подробный обзор фильма',
        validators=[Optional(), Length(max=256)]
    )
    images = MultipleFileField(
        validators=[
            FileAllowed(
                ['jpg', 'jpeg', 'png', 'gif', 'bmp'],
                message=(
                    'Выбери файл с расширением '
                    '.jpg, .jpeg, .png, .gif или .bmp'
                )
            )
        ]
    )
    submit = SubmitField('Добавить мнение')

from flask_wtf import FlaskForm
from webapp.user.models import User
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
        )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
        )
    remember_me = BooleanField(
        'Запомнить меня',
        default=True,
        render_kw={'class': 'form-check-input'}
        )
    submit = SubmitField('Войти', render_kw={'class': 'btn btn-success'})


class RegistrationForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
        )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
        )
    password2 = PasswordField(
        'Повторите пароль',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={'class': 'form-control'}
        )
    email = StringField(
        'E-Mail',
        validators=[DataRequired(), Email()],
        render_kw={'class': 'form-control'}
        )
    submit = SubmitField('Зарегистрироваться', render_kw={'class': 'btn btn-success'})

    def validate_username(self, username):
        users = User.query.filter_by(username=username.data).count()
        if users:
            raise ValidationError(
                'Пользователь с таким именем уже зарегистрирован :('
            )

    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).count()
        if users:
            raise ValidationError(
                'Пользователь с такой почтой уже зарегистрирован :('
            )


# class RecipeForm(FlaskForm):
#     title = StringField(
#         'Название блюда',
#         validators=[DataRequired()],
#         render_kw={'class': 'form-control'}
#         )
#     recipe = StringField(
#         'Рецепт',
#         validators=[DataRequired()],
#         render_kw={'class': 'form-control'}
#         )
#     ingredients = StringField(
#         'Ингртдиенты',
#         validators=[DataRequired()],
#         render_kw={'class': 'form-control'}
#         )
#     submit = SubmitField('Сохранить', render_kw={'class': 'btn btn-success'})
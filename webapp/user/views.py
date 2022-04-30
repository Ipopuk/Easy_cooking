from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from webapp.db import db
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import Recipe, User
from werkzeug.utils import secure_filename
import os

blueprint = Blueprint('user', __name__)


@blueprint.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    recipes = Recipe.query.all()
    if len(recipes) % 3 == 1:
        recipes.extend(recipes[:2])
    elif len(recipes) % 3 == 2:
        recipes.append(recipes[0])
    if recipes:
        return render_template(
            'index.html',
            title='Рецепты',
            recipes=recipes
            )
    return redirect(url_for('user.add_recipe'))


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    title = 'Авторизация'
    form = LoginForm()
    return render_template('login.html', title=title, form=form)


@blueprint.route('/process-login', methods=['post'])
def process_login():
    form = LoginForm()
    user = User.query.filter_by(username=form.username.data).first()
    if user and user.check_password(form.password.data):
        login_user(user, remember=form.remember_me.data)
        flash('С возвращением!')
        return redirect(url_for('user.index'))
    flash('Неправильный пароль!')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.index'))


@blueprint.route('/registration')
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    title = 'Регистрация'
    form = RegistrationForm()
    return render_template('registration.html', title=title, form=form)


@blueprint.route('/process-registration', methods=['post'])
def process_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            wishlist=''
            )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Ошибка в поле {getattr(form, field).label.text}: {error}')
    return redirect(url_for('user.registration'))


@blueprint.route('/add-recipe')
def add_recipe(rows=0):
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    elif rows > 0:
        rows = int(rows)
        data = dict(request.form)
        data['ing'] = []
        for key, value in data.items():
            if 'ingredient' in key:
                key = key.split('_')[-1]
                measure = data[f'measure_{key}']
                data['ing'].append((value, data[f'value_{key}'], measure))
        try:
            data['image'] = request.files['file']
        except:
            pass
    else:
        data = None
    title = 'Мои рецепты'
    return render_template(
        'add_recipe.html',
        title=title,
        rows=rows,
        data=data,
        measures=["Ед. изм.", "гр", "кг", "шт", "ч.л.", "ст.л.", "л.", "мл."]
        )


@blueprint.route('/choose-func', methods=['post'])
def choose_func():
    if request.form['submit_button'] == '+':
        print(request.form)
        rows = [int(row.split('_')[-1]) for row in request.form if 'ingred' in row]
        return add_recipe(max(rows) + 1)
    else:
        return save_recipe(request.form)


@blueprint.route('/save-recipe', methods=['post'])
def save_recipe(form):
    title = request.form['title']
    recipe = request.form['recipe']
    image = request.files['file']
    filename = secure_filename(image.filename)
    basedir = os.path.dirname(__file__)
    path = os.path.join(basedir, '..', 'static', 'images', filename)
    image.save(path)
    ingredients = []
    for key, value in request.form.items():
        if 'ingredient' in key:
            key = key.split('_')[-1]
            measure = request.form[f'measure_{key}']
            ingredients.append(f"{value}: {request.form[f'value_{key}']} {measure}")
    ingredients = '\n'.join(ingredients)
    new_recipe = Recipe(
        title=title,
        recipe=recipe,
        ingredients=ingredients,
        image=os.path.join('.', 'static', 'images', filename),
        user_id=current_user.id
        )
    db.session.add(new_recipe)
    db.session.commit()
    flash('Рецепт добавлен!')
    return redirect(url_for('user.add_recipe'))


@blueprint.route('/recipe/<int:recipe_id>')
def show_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if not recipe:
        abort(404)
    return render_template(
        'recipe.html',
        title=recipe.title,
        recipe=recipe
    )


@blueprint.route('/settings')
def settings():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    title = 'Настройки профиля'
    form = RegistrationForm(
        username=current_user.username,
        email=current_user.email,
        submit='Сохранить'
        )
    return render_template('settings.html', title=title, form=form)


@blueprint.route('/save-settings', methods=['post'])
def save_settings():
    form = RegistrationForm()
    user = User.query.filter_by(username=current_user.username).first()
    user.username = form.username.data
    user.email = form.email.data
    user.set_password(form.password.data)
    db.session.commit()
    flash('Данные сохранены!')
    return redirect(url_for('user.settings'))


@blueprint.route('/add-to-fav')
def add_to_fav():
    recipe_id = request.args['recipe_id']
    user = User.query.filter_by(username=current_user.username).first()
    user.wishlist = user.wishlist + recipe_id + ';'
    db.session.commit()
    flash('Блюдо добавлено в ваш список желаний!')
    return redirect(url_for('user.index'))


@blueprint.route('/remove-from-fav')
def remove_from_fav():
    recipe_id = request.args['recipe_id']
    user = User.query.filter_by(username=current_user.username).first()
    user.wishlist = user.wishlist.replace(recipe_id + ';', '')
    db.session.commit()
    flash('Блюдо удалено!')
    return redirect(request.referrer)


@blueprint.route('/favs')
def show_favs():
    recipes = Recipe.query.all()
    recipes = list(filter(lambda x: str(x.id) in current_user.wishlist.split(';'), recipes))
    if recipes:
        return render_template(
            'wishlist.html',
            title='Избранное',
            recipes=recipes
            )
    flash('Вы еще ничего не добавляли в избранное!')
    return redirect(url_for('user.index'))


@blueprint.route('/search-result', methods=['post'])
def search_result():
    kw = request.form['kw'].lower()
    recipes = Recipe.query.all()
    recipes = list(filter(lambda x: kw in x.title.lower() or kw in x.ingredients.lower(), recipes))
    if recipes:
        return render_template(
            'wishlist.html',
            title='Результаты поиска',
            recipes=recipes
            )
    flash('Ничего не найдено :(')
    return redirect(url_for('user.index'))


@blueprint.route('/my-recipes')
def show_my_recipes():
    my_recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    if my_recipes:
        return render_template('my_recipes.html', my_recipes=my_recipes)
    flash('Вы еще не добавляли рецепты!')
    return redirect(url_for('user.add_recipe'))


@blueprint.route('/del-recipe')
def del_recipe():
    recipe_id = request.args['recipe_id']
    print(recipe_id)
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    print(recipe)
    db.session.delete(recipe)
    db.session.commit()
    flash('Рецепт удален :(')
    return redirect(url_for('user.show_my_recipes'))

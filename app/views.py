import secrets
import os
from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from flask_login import logout_user, login_user
from .forms import RegisterForm, LoginForm, UpdateAccountForm
from .forms import AritcleForm, UpdateArticleForm
from .models import db, User, Profile, Article


@app.route('/')
def main():
    articles = db.session.query(Article).order_by(Article.create_on.desc())
    return render_template('main.html', title='Статьи', articles=articles)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data,
                        email=form.email.data)
            user.set_password_hash(form.password.data)
            db.session.add(user)
            db.session.commit()
            profile = Profile(user_id=user.id)
            profile.set_default_information()
            db.session.add(profile)
            db.session.commit()
            flash('Вы успешно зарегистрированы',
                  category='alert alert-success')
            return redirect(url_for('login'))
        except Exception:
            flash('Произошла ошибка, попробуйте позднее',
                  category='alert alert-danger')
            db.session.rollback()
            return redirect(url_for('register'))

    return render_template('user/register.html', form=form,
                           title='Регистрация')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user.check_password(form.password.data):
            flash('Неверный email или пароль', category='alert alert-danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        return redirect(url_for('account'))

    return render_template('user/login.html',
                           form=form, title='Авторизация')


@app.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно вышли', category='alert alert-success')
    return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img',
                                picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile.image_file = picture_file
        current_user.username = form.username.data
        current_user.profile.firstname = form.firstname.data
        current_user.profile.lastname = form.lastname.data
        db.session.commit()
        return redirect(url_for('account'))
    form.username.data = current_user.username
    form.firstname.data = current_user.profile.firstname
    form.lastname.data = current_user.profile.lastname
    image_file = url_for('static',
                         filename='img/' + current_user.profile.image_file)
    return render_template('user/account.html', title='Аккаунт',
                           image_file=image_file, form=form)


@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    form = AritcleForm()
    if form.validate_on_submit():
        article = Article(title=form.title.data,
                          text=form.text.data,
                          user_id=current_user.id)
        db.session.add(article)
        db.session.commit()
        flash('Статья успешна создана!', category='alert alert-success')
        return redirect(url_for('add_article'))
    return render_template('add_article.html', title='Добавить статью',
                           form=form)


@app.route('/article/<int:article_id>')
@login_required
def article(article_id):
    article = db.session.query(Article).filter(
        Article.id == article_id).first()
    return render_template('article.html', title=f'{article.title}',
                           article=article)


@app.route('/update_article/<int:article_id>', methods=['GET', 'POST'])
@login_required
def update_article(article_id):
    article = db.session.query(Article).filter(
        Article.id == article_id).first()
    if not article:
        return redirect(url_for('account'))
    if current_user.id != article.user_id:
        return redirect(url_for('account'))
    form = UpdateArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.text = form.text.data
        db.session.add(article)
        db.session.commit()
        print(form.title.data)
        print(form.text.data)
        print(article.title, article.text)
        return redirect(url_for('account'))
    form.title.data = article.title
    form.text.data = article.text
    return render_template('update_article.html', title=f'{article.title}',
                           article=article, form=form)

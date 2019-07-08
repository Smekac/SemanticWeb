import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, jsonify

from flaskblog import app, db, bcrypte
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddFilm
from flaskblog.models import User, Post
from  flask_login import login_user, current_user, logout_user , login_required

from flaskblog import sparql_server

@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page,per_page=4)
    return render_template('home.html', posts=posts)


@app.route("/")
@login_required
def only_recomend():
    return render_template('recommender.html')

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    genre_film = request.args.get('genre')
    print("Ime zanra: " + str(genre_film))
    if not genre_film:
        message = "Missing 'genre' query param"
        #print("")
        return jsonify({'message': message}), 400

    books = sparql_server.get_films(genre_film)
    print("Sve knjigee: " + str(books))
    print(books)
    if not books:
        message = 'Invalid course name: {}'.format(genre_film)
        return jsonify({'message': message}), 400
   # data = []
   # for post in books:
   #     data.append(post)         #sorted(books, key=lambda post: post.title)
   # data = json.dumps(data)
    data = [book.onlyTitle() for book in sorted(books, key=lambda book: book.title)]
    print("Podacii " + str(data))
    return jsonify({'books': data}), 200

""" english_books = {book for book in books if book.language == 'en'}
    if english_books:
        book_titles = [book.title for book in english_books]
        recommendations = app.book_recommender.get_recommendations(titles=book_titles)
        books.update(recommendations)
"""



@app.route("/user/<string:username>")
def user_films(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author = user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page,per_page=4)
    return render_template('user_posts.html', posts=posts, user=user)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypte.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!, You can Log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypte.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_extension = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_extension
    picture_path = os.path.join(app.root_path, 'static/profile_pictures', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn

def save_film_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_extension = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_extension
    picture_path = os.path.join(app.root_path, 'static/films', picture_fn)
    output_size = (250, 350)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file #form.picture.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('account is updated', 'success')
        return  redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pictures/' + current_user.image_file)
    return render_template('account.html', title='Account',image_file = image_file,form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_film():
    form = AddFilm()
    if form.validate_on_submit():
        #if form.picture.data:
        picture_file = save_film_picture(form.picture.data)
        post = Post(title= form.title.data, content=form.content.data , author =current_user) #, image_file=picture_file
        post.image_file = picture_file
        db.session.add(post)
        db.session.commit()
        flash('Your film has been added!', "success")
        return redirect(url_for('home'))
    return render_template('create_film.html', title='New Film',form=form)

import flask
from foodcart.persistance import UserRepository
from foodcart.models.User import User
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from foodcart.forms.LoginForm import LoginForm
from foodcart.forms.SignupForm import SignupForm
from foodcart.connection.db_utils import cursor

app = flask.Flask(__name__)
app.secret_key = 'tDo4f]$QQa#mk,gyL+(+BsNQp'
login_manager = LoginManager()


@app.route('/')
@login_required
def hello():
    return flask.render_template('accueil.html')

@app.route('/about')
@login_required
def about_page():
    return flask.render_template('about.html')

@app.route('/cart')
@login_required
def cart_page():
    return flask.render_template('cart.html')

@app.route('/account')
@login_required
def account_page():
    return flask.render_template('account.html')

@app.route('/cart/<id>')
@login_required
def add_to_cart(id):
    return f"Ajout du produit avec le id {id} au panier"


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('hello'))

    form = SignupForm(flask.request.form)
    if form.validate_on_submit():
        user = user_loader(form.username.data)
        print(user)
        if not user:
            user = User(form.username.data, None, form.last_name.data, form.first_name.data, form.email.data, form.address.data)
            user.set_pwd(form.password.data)
            UserRepository.add_user(user)
            return flask.redirect(flask.url_for('login'))
        else:
            flask.flash('This username is already taken. Please try again.')
    return flask.render_template('signup.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('hello'))

    form = LoginForm(flask.request.form)
    if form.validate_on_submit():
        user = user_loader(form.username.data)
        if user and user.check_pwd(form.password.data):
            login_user(user)
            return flask.redirect(flask.url_for('hello'))
        else:
            flask.flash('Invalid username or password. Please try again')
    return flask.render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return flask.redirect("login")


@login_manager.user_loader
def user_loader(user_id):
    return UserRepository.get_user_from_username(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return flask.redirect("login")

@app.route('/fruits')
def show_fruit():
    cursor.execute("USE FoodCart")
    cursor.execute("SELECT * FROM products where class_name ='fruit' ")
    fruits= cursor.fetchall()
    return flask.render_template('fruits.html', data=fruits)

@app.route('/legumes')
def show_legume():
    cursor.execute("USE FoodCart")
    cursor.execute("SELECT * FROM products where class_name ='legume' ")
    legumes = cursor.fetchall()
    return flask.render_template('legume.html', data=legumes)

@app.route('/viandes')
def show_viandes():
    cursor.execute("USE FoodCart")
    cursor.execute("SELECT * FROM products where class_name ='viande' ")
    viandes = cursor.fetchall()
    return flask.render_template('viandes.html', data=viandes)

@app.route('/boulangerie')
def show_pains():
    cursor.execute("USE FoodCart")
    cursor.execute("SELECT * FROM products where class_name ='pain' ")
    pains = cursor.fetchall()
    return flask.render_template('boulangerie.html', data=pains)

@app.route('/produit_laitier')
def show_lait():
    cursor.execute("USE FoodCart")
    cursor.execute("SELECT * FROM products where class_name ='produit_laitier' ")
    lait = cursor.fetchall()
    return flask.render_template('produit_laitier.html', data=lait)

if __name__ == '__main__':
    login_manager.init_app(app)
    app.run(debug=True)

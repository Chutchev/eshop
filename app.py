from flask import Flask, redirect, render_template, url_for, flash, request, make_response
import db
from Forms import LoginForm



app = Flask(__name__)
TITLE = 'GEEKSHOP'
app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route('/home')
def home():
    return render_template('home.html', title=TITLE)


@app.route('/catalog')
def catalog():
    infos = db.select('products', 'name', 'price', 'description', 'image', 'category')
    categories = db.select('products', 'category')
    categories = list(sorted(set([category[0] for category in categories])))
    information = {'title': TITLE, 'info': infos, 'categories': categories}
    return render_template('catalog.html', **information)


@app.route('/contacts')
def contacts():
    information = {'title': TITLE}
    return render_template('home.html', **information)


@app.route('/sales')
def sales():
    information = {'title': TITLE}
    return render_template('home.html', **information)


@app.route('/<product_name>', methods=['GET', 'POST'])
def show_product(product_name):
    info = db.select_product(product_name)
    information = {'title': TITLE, 'info': info}
    if request.method == 'POST':
        count = request.form['count']
        login = request.cookies.get('login')
        price = info[2]
        cost = int(price)*int(count)
        db.insert_to_shopping_cart(product=product_name, login=login, count=count, cost=cost, price=price)
    return render_template('product.html', **information)


@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    form = LoginForm.LoginForm()
    if form.validate_on_submit():
        login = form.username.data
        password = form.password.data
        true_login, true_pass = db.select('admins', 'login', 'password', where=f"login='{login}'")[0]
        if login == true_login and password == true_pass:
            return redirect(url_for('sales'))
    return render_template('admin.html', title='Sign In', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm.LoginForm()
    if form.validate_on_submit():
        login = form.username.data
        password = form.password.data
        true_login, true_pass = db.select('users', 'user_login', 'user_password', where=f"user_login='{login}'")[0]
        if login == true_login and password == true_pass:
            cookies = make_response(redirect(url_for('sales')))
            cookies.set_cookie('login', login, max_age=60*60*24*7)
            return cookies
    return render_template('admin.html', title='Sign In', form=form)


@app.route('/shopping_cart')
def shopping_cart():
    login = request.cookies.get('login')
    information = db.select('shopping_cart', '*', where=f'user_login="{login}"')
    print(information)
    return render_template('shopping_cart.html', information=information)


@app.route('/')
def pusto():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')

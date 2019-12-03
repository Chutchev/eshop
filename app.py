from flask import Flask, redirect, render_template, url_for, request, make_response
import db
from Forms import LoginForm
import helpers

app = Flask(__name__)
TITLE = 'GEEKSHOP'
app.config['SECRET_KEY'] = 'you-will-never-guess'


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        user_login = request.form['login']
        password = helpers.create_md5(request.form['password'])
        address = request.form['address']
        email = request.form['email']
        name = request.form['name']
        information = {'user_login': user_login, 'password': password, 'address': address, 'email': email, 'name': name}
        db.insert_to_users(**information)
        return redirect(url_for('login'))
    return render_template('registration.html', title='Регистрация')


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
    flag = True
    information = {'title': TITLE, 'info': info, "true_count": flag}
    if request.method == 'POST':
        price = info[1]
        login = request.cookies.get('login')
        try:
            count = int(request.form['count'])
        except ValueError:
            flag = False
            information.update({"true_count": flag})
            return render_template('product.html', **information)
        cost = int(price) * int(count)
        if login is None:
            return redirect(url_for('login'))
        db.insert_to_shopping_cart(product=product_name, login=login, count=count, cost=cost, price=price)
    return render_template('product.html', **information)

@app.route('/adminpanel', methods=['GET', 'POST'])
def admin_panel():
    is_admin = bool(request.cookies.get('admin'))
    if is_admin:
        if request.method == 'POST':
            product = request.form['product']
            try:
                price = request.form['price']
                description = request.form['description']
                image = request.files.getlist('image')[0].filename
                keyword = request.form['keyword']
                info = {'name': product, 'count': 800, 'price': price, 'image': f'./static/images/{image}', 'keyword': keyword,
                    'description': description, 'category': keyword}
                db.add_to_products(**info)
            except Exception:
                db.delete_into_products(product)
        products = db.select('products', '*')
        return render_template('admin_panel.html', title='GEEKSHOP', products=products)

    else:
        return render_template('404.html', title="404")


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm.LoginForm()
    if form.validate_on_submit():
        login = form.username.data
        password = form.password.data
        true_login, true_pass = db.select('admins', 'login', 'password', where=f"login='{login}'")[0]
        if login == true_login and password == true_pass:
            cookies = make_response(redirect(url_for('admin_panel')))
            cookies.set_cookie('admin', 'True', max_age=60 * 60)
            return cookies
    return render_template('admin.html', title='Sign In', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm.LoginForm()
    if form.validate_on_submit():
        login = form.username.data
        password = helpers.create_md5(form.password.data)
        try:
            true_login, true_pass = db.select('users', 'user_login', 'user_password', where=f"user_login='{login}'")[0]
        except IndexError:
            return render_template('admin.html', title='Sign In', form=form, error=True)
        if login == true_login and password == true_pass:
            cookies = make_response(redirect(url_for('sales')))
            cookies.set_cookie('login', login, max_age=60 * 60 * 24 * 7)
            return cookies
        else:
            return render_template('admin.html', title='Sign In', form=form, error=True)
    return render_template('admin.html', title='Sign In', form=form)


@app.route('/shopping_cart', methods=['GET', 'POST'])
def shopping_cart():
    login = request.cookies.get('login')
    information = db.select('shopping_cart', '*', where=f'user_login="{login}"')
    if request.method == 'POST':
        login = request.cookies.get('login')
        db.change_status(login)
        return redirect(url_for('shopping_cart'))
    return render_template('shopping_cart.html', information=information)


@app.route('/')
def pusto():
    login = request.cookies.get('login')
    if not login:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('catalog'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')

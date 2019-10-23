from flask import Flask, redirect, render_template, url_for, flash
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
    information = {'title': TITLE, 'info': infos}
    return render_template('catalog.html', **information)


@app.route('/contacts')
def contacts():
    information = {'title': TITLE}
    return render_template('home.html', **information)


@app.route('/sales')
def sales():
    information = {'title': TITLE}
    return render_template('home.html', **information)


@app.route('/<product_name>')
def show_product(product_name):
    info = db.select_product(product_name)
    information = {'title': TITLE, 'info': info}
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


@app.route('/')
def pusto():
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')

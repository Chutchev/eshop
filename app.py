from flask import Flask, redirect, render_template, url_for
import db

app = Flask(__name__)
TITLE = 'GEEKSHOP'
app.config['SECRET_KEY'] = 'you-will-never-guess'


@app.route('/home')
def home():
    return render_template('home.html', title=TITLE)


@app.route('/catalog')
def catalog():
    info = db.select('products', 'name', 'price', 'description', 'image', 'category')
    information = {'title': TITLE, 'info': info}
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

@app.route('/admin')
def admin_panel():
    info = db.select('admins', '*')
    return render_template('admin.html')


@app.route('/')
def pusto():
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')

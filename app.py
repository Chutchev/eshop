from flask import Flask, redirect, render_template, url_for
import db

app = Flask(__name__)


@app.route('/home')
def home():
    return render_template('home.html', title='КУКУЕПТА')


@app.route('/catalog')
def catalog():
    info = db.select('products', 'product_name', 'product_price', 'product_description', 'image')
    return render_template('catalog.html', title='КУКУЕПТА', info=info)


@app.route('/contacts')
def contacts():
    return render_template('home.html', title='КУКУЕПТА')


@app.route('/sales')
def sales():
    return render_template('home.html', title='КУКУЕПТА')


@app.route('/')
def pusto():
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')

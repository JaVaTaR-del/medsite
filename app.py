from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ProductItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    smallDecription = db.Column(db.Text, nullable=False)
    decription = db.Column(db.Text, nullable=False)
    application = db.Column(db.Text, nullable=False)
    size = db.Column(db.String(100), nullable=False)
    Type = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<ProductItem %r>' % self.id

@app.route('/')
@app.route('/home')
def index():
    Productitem = ProductItem.query.all()
    return render_template('index.html', Productitem=Productitem)

@app.route('/products/leather')
def productsleather():
    productitem = ProductItem.query.all()
    return render_template('products-leather.html', productitem=productitem)

@app.route('/products/coat')
def productscoat():
    productitem = ProductItem.query.all()
    return render_template('products-coat.html', productitem=productitem)

@app.route('/products/hoof')
def productshoof():
    productitem = ProductItem.query.all()
    return render_template('products-hoof.html', productitem=productitem)

@app.route('/products/health')
def productshealth():
    productitem = ProductItem.query.all()
    return render_template('products-health.html', productitem=productitem)

@app.route('/products/<string:Type>/<string:id>')
def product_card(Type,id):
    productitem = ProductItem.query.get(Type)
    productitem = ProductItem.query.get(id)
    Productitem = ProductItem.query.all()
    return render_template('product-card.html', productitem=productitem, Productitem=Productitem)

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        Type = request.form['Type']
        size = request.form['size']
        smallDecription = request.form['smallDecription']
        decription = request.form['decription']
        application = request.form['application']

        productitem = ProductItem(name=name, Type=Type, size=size, smallDecription=smallDecription, decription=decription, application=application)
        
        db.session.add(productitem)
        db.session.commit()

        return render_template('create.html')

    else:
        return render_template('create.html')

@app.route('/shops', methods=['POST', 'GET'])
def shops():
    return render_template('shops.html')

@app.route('/kontakts', methods=['POST', 'GET'])
def kontakts():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        telephone = request.form['telephone']
        message = request.form['message']
        
        msg = MIMEMultipart()
        
        from_email = 'carrdaymartinru@gmail.com'
        password = '$VFR4567ygv$'
        to_email = 'nnakozhemm@gmail.com'
        text = 'Почта: ' + email + '\n' + 'Телефон: ' + telephone + '\n' + 'Заголовок: ' + name + '\n' + 'Сообщение: ' + message + '\n'
        
        msg.attach(MIMEText(text, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        return "successfully sent email to:"
    
    else:
        return render_template('kontakts.html')


if __name__ == "__main__":
    app.run(debug = True)
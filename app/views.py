from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, current_user, logout_user, login_required
from . import mysql
from .models import User, Product
from .forms import RegistrationForm, LoginForm, SearchForm, CheckoutForm
import json


main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__, url_prefix='/auth')
products = Blueprint('products', __name__, url_prefix='/products')


@main.route('/')
@main.route('/index')
def index():
    search_form = SearchForm()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    return render_template('index.html', products=products, search_form=search_form)

@main.route('/search', methods=['GET', 'POST'])
def search():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        query = search_form.query.data
        products = Product.search_products(query)
        return render_template('search_results.html', products=products, search_form=search_form, query=query)
    
    
    if request.args.get('query'):
        query = request.args.get('query')
        products = Product.search_products(query)
        return render_template('search_results.html', products=products, search_form=search_form, query=query)
    
    return redirect(url_for('main.index'))

@main.route('/summary')
def summary():
    search_form = SearchForm()
    return render_template('summary.html', search_form=search_form)

@main.route('/checkout', methods=['GET', 'POST'])
def checkout():
    
    checkout_form = CheckoutForm()
    search_form = SearchForm()
    
    if checkout_form.validate_on_submit():
        
        full_name = checkout_form.full_name.data
        phone = checkout_form.phone.data
        address = checkout_form.address.data
        
        
        payment_method = request.form.get('paymentMethod', 'UPI Payment')
        delivery_method = request.form.get('deliveryMethod', 'Standard Delivery')
        
        
        subtotal = float(request.form.get('cart_subtotal', 0))
        delivery_fee = float(request.form.get('cart_delivery', 6.99))
        tax = float(request.form.get('cart_tax', 0))
        total = float(request.form.get('cart_total', 0))
        
        
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO orders (user_id, full_name, phone, address, total, delivery_fee, tax, payment_method, delivery_method) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (current_user.id if current_user.is_authenticated else None, 
                 full_name, phone, address, total, delivery_fee, tax, payment_method, delivery_method)
            )
            mysql.connection.commit()
            order_id = cursor.lastrowid
            
            
            cart_data = request.form.get('cart_items')
            if cart_data:
                cart_items = json.loads(cart_data)
                for item in cart_items:
                    cursor.execute(
                        "INSERT INTO orders_items (order_id, product_id, product_name, price, quantity) VALUES (%s, %s, %s, %s, %s)",
                        (order_id, item['id'], item['name'], item['price'], item['quantity'])
                    )
                mysql.connection.commit()
            
            
            flash('Your order has been placed successfully! Thank you for shopping with PharmaGo.', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            flash(f'An error occurred while processing your order. Please try again.', 'danger')
            print(e)  
    
    
    return render_template('checkout.html', form=checkout_form, search_form=search_form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    search_form = SearchForm()
    
    if form.validate_on_submit():
        try:
            User.create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('An error occurred during registration. Please try again.', 'danger')
            print(e)  
    
    return render_template('register.html', form=form, search_form=search_form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    search_form = SearchForm()
    
    if form.validate_on_submit():
        try:
            user = User.get_by_email(form.email.data)
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash('Login successful! Welcome back.', 'success')
                return redirect(next_page if next_page else url_for('main.index'))
            else:
                flash('Login unsuccessful. Please check email and password.', 'danger')
        except Exception as e:
            flash('An error occurred during login. Please try again.', 'danger')
            print(e)  
    
    return render_template('login.html', form=form, search_form=search_form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/account')
@login_required
def account():
    search_form = SearchForm()
    
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC", (current_user.id,))
    orders = cursor.fetchall()
    cursor.close()
    
    return render_template('account.html', search_form=search_form, orders=orders)


@products.route('/details/<int:product_id>')
def details(product_id):
    search_form = SearchForm()
    
    try:
        product = Product.get_product_by_id(product_id)
        if not product:
            flash('Product not found', 'danger')
            return redirect(url_for('main.index'))
        
        return render_template('details.html', product=product, search_form=search_form)
    except Exception as e:
        flash('An error occurred while retrieving product details.', 'danger')
        print(e)  
        return redirect(url_for('main.index'))
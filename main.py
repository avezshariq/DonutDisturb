from flask import Flask, render_template, url_for, request, redirect, session, flash
import maintenance
import uuid
import json


app = Flask(__name__)
app.secret_key = 'my_sooper_secret_key_in_palce_here'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        order_items = request.form.to_dict()
        session['order_items'] = order_items
        return redirect(url_for('cart'))
    data_dict = maintenance.get_all_items()
    return render_template('menu.html', data_dict=data_dict)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    order_items = session.get('order_items', {})
    buy_items = [(key, value) for key, value in order_items.items() if value != '0']
    if not buy_items:
        return render_template('empty.html')
    item_prices = maintenance.get_all_prices()
    item_prices_dict = {item:price for item, price in item_prices}
    print(f'{buy_items = }')
    print(f'{item_prices = }')
    buy_items_with_price = [(x, y, item_prices_dict[x], int(y)*float(item_prices_dict[x])) for x, y in buy_items]
    sub_total = sum(val for x, y, z, val in buy_items_with_price)
    disc = discount = 0
    if request.method == 'POST':
        coupon_name = request.form.get('coupon', None)
        disc = maintenance.get_discount(coupon_name=coupon_name)
        discount = round(disc*sub_total*0.01, 2)
    tax = 0.15 * sub_total
    grand_total = round(sub_total - discount + tax, 2)
    session['buy_items_with_price'] = buy_items_with_price
    session['sub_total'] = sub_total
    session['disc'] = disc
    session['discount'] = discount
    session['tax'] = tax
    session['grand_total'] = grand_total
    return render_template('cart.html', order_items=buy_items_with_price, sub_total=f'{sub_total:.2f}', disc=disc, discount=f'{discount:.2f}', tax=f'{tax:.2f}', grand_total=f'{grand_total:.2f}')

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    transaction_amount = session['grand_total']
    choice = 'upi'
    if request.method == 'POST':
        form_data = request.form.to_dict()
        choice = list(form_data.keys())[0]
    session['choice'] = choice
    return render_template('pay.html', choice=choice, transaction_amount=transaction_amount)

@app.route('/invoice', methods=['POST'])
def invoice():
    invoice_id = uuid.uuid4()
    choice = session['choice']
    buy_items_with_price = session['buy_items_with_price']
    sub_total = session['sub_total']
    disc = session['disc']
    discount = session['discount']
    tax = session['tax']
    grand_total = session['grand_total']
    session.clear()
    return render_template('invoice.html', invoice_id=invoice_id, buy_items_with_price=buy_items_with_price, sub_total=f'{sub_total:.2f}', disc=disc, discount=f'{discount:.2f}', tax=f'{tax:.2f}', grand_total=f'{grand_total:.2f}')

@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        the_form = request.form.to_dict()
        if the_form['act'] == 'create':
            if the_form['password'] == the_form['password_again']:
                data = maintenance.get_user(email=the_form['email'])
                print(data)
                if not data:
                    maintenance.insert_data(db_name='server', table_name="users", data=[(the_form['email'], the_form['password'])])
                    flash('Welcome!!! Now start getting disturbed by donuts after login 😋', category='info')
                else:
                    flash('User already exists', category='error')
            else:
                flash("I know you're in a hurry, but type the passwords correctly", category='error')
        else:
            stored_password = maintenance.get_user(db_name='server', table_name='users', email=the_form['email'])
            if stored_password:
                if stored_password[1] == the_form['password']:
                    if the_form['email'] == 'admin@admin.com':
                        return redirect(url_for('admin'))
                    return 'Login Successful'
                else:
                    flash("I'm hungry too. But type the credentials correctly", category='error')
            else:
                flash('First time? Create account first', category='error')

    return render_template('account.html')

@app.route('/admin')
def admin():
    no_of_users, payment_methods_chart, sold_items_chart, payment_methods_scatter_chart, total_business, total_orders = maintenance.analytics(db_name='server')
    return render_template('admin.html', payment_methods_chart=json.dumps(payment_methods_chart), no_of_users=no_of_users, sold_items_chart=json.dumps(sold_items_chart), payment_methods_scatter_chart=json.dumps(payment_methods_scatter_chart), total_business=total_business, total_orders=total_orders)

if __name__ == '__main__':
    app.run(debug=True)

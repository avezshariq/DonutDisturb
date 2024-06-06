from flask import Flask, render_template, url_for, request, redirect, session
import maintenance

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
    item_prices = maintenance.get_all_prices()
    item_prices_dict = {item:price for item, price in item_prices}
    print(f'{buy_items = }')
    print(f'{item_prices = }')
    buy_items_with_price = [(x, y, item_prices_dict[x], int(y)*float(item_prices_dict[x])) for x, y in buy_items]
    sub_total = sum(val for x, y, z, val in buy_items_with_price)
    discount = 0
    if request.method == 'POST':
        coupon_name = request.form.get('coupon', None)
        disc = maintenance.get_discount(coupon_name=coupon_name)
        discount = round(disc*sub_total*0.01, 2)
    tax = 0.15 * sub_total
    grand_total = round(sub_total - discount + tax, 2)
    session['grand_total'] = grand_total
    return render_template('cart.html', order_items=buy_items_with_price, sub_total=f'{sub_total:.2f}', disc=disc, discount=f'{discount:.2f}', tax=f'{tax:.2f}', grand_total=f'{grand_total:.2f}')

@app.route('/pay')
def pay():
    return 'Payment'

if __name__ == '__main__':
    app.run(debug=True)
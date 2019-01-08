from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'My Store',
        'items': [
            {
            'name': 'Moj przedmiot',
            'price': 9.99,
            }
        ],
    }
]

@app.route('/')
def home():
    return render_template('index.html')

#POST używane do otrzymania danych do serwera
#GET używane do wysyłania danych z serwera

#POST /sklep data: {nazwa:}         --stworzenie sklepu o podanej nazwie
@app.route('/store', methods=['POST'])
def create_store():
    """Utworzenie sklepu"""
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': [],
    }
    stores.append(new_store)
    return jsonify(new_store)

#GET /sklep/<string:nazwa>          --wyświetlenie konkretnego sklepu
@app.route('/store/<string:name>')
def get_store(name):
    """Wyświetl podany sklep"""
    for store in stores:
        if name == store['name']:
            return jsonify(store)
    return jsonify({'message': 'store not found'})

#GET /sklep                         --wyświetlenie listy sklepów
@app.route('/store')
def get_stores():
    """Wyświetla listę sklepów"""
    return jsonify({'stores': stores})

#POST /sklep/<string:nazwa>/item {nazwa:, cena:} --stworzenie przedmiotu w sklepie z własną nazwą i ceną
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item(name):
    """Utworzenie przedmiotu w danym sklepie"""
    request_data = request.get_json()
    for store in stores:
        if name == store['name']:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price'],
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found'})

#GET /sklep/<string:nazwa>/item     --wyświetla przedmiot
@app.route('/store/<string:name>/item')
def show_item(name):
    """Wyświetl przedmiot w sklepie"""
    for store in stores:
        if name == store['name']:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'})


app.run(port=8000)


# from http import client
from flask import Flask, jsonify, request, render_template, url_for, redirect
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
client = MongoClient("mongodb+srv://palashgupta94:har23071990@cluster0.qrhlii4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", server_api=ServerApi('1'))
db = client['mydatabase']
collection = db['mycollection']

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route('/api', methods=['GET'])
def api():
    with open('data.json', 'r') as file:
        data = json.load(file)
        return jsonify(data)
    
@app.route('/add-data', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            collection.insert_one({'name': name, 'email': email})
            return redirect(url_for('success'))
        except Exception as e:
            return render_template('form.html', error=str(e))
    return render_template('form.html')

@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')
    
@app.route('/submittodoitem', methods=['GET', 'POST'])
def submit_to_do():
    if request.method == 'POST':
        try:
            itemName = request.form['item_name']
            itemDescription = request.form['item_desc']
            app.logger.info(f"task name: {itemName}, desciption: {itemDescription}")
            collection.insert_one({'name': itemName, 'description': itemDescription})
            return jsonify({'status': 'success'})
        except Exception as e:
            print(e)
    return render_template('To-Do page.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

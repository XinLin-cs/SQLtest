from flask import jsonify
from app import app
from app import POST


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/test', methods=['GET'])
def get_data():
    myData = POST.query.all()
    output = []
    for record in myData:
        r_data = {}
        r_data['postTitle'] = record.postTitle
        output.append(r_data)
    return jsonify({'message': output})

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/reverse', methods=['POST'])
def reverse_string():
    input_string = request.data.decode('utf-8')

    if not input_string:
        return jsonify({'error': 'Input string not provided'}), 400

    reversed_string = input_string[::-1]

    return jsonify({'reversed_string': reversed_string})

if __name__ == '__main__':
    app.run(debug=True)

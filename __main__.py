from flask import Flask, request, jsonify

app = Flask(__name__)


def calculate(expression):
    tokens = tokenize(expression)
    result, _ = parse_expression(tokens)
    return result


def tokenize(expression):
    operators = set("+-*/()")
    tokens = []
    current_token = ""

    for char in expression:
        if char.isdigit() or char == '.' or (char == '-' and (not current_token or current_token[-1] in operators)):
            current_token += char
        elif char in operators:
            if current_token:
                tokens.append(current_token)
                current_token = ""
            tokens.append(char)
        elif char.isspace():
            if current_token:
                tokens.append(current_token)
                current_token = ""

    if current_token:
        tokens.append(current_token)

    return tokens


def parse_expression(tokens):
    result, rest = parse_term(tokens)

    while rest and rest[0] in ('+', '-'):
        operator = rest[0]
        term, rest = parse_term(rest[1:])
        if operator == '+':
            result += term
        elif operator == '-':
            result -= term

    return result, rest


def parse_term(tokens):
    result, rest = parse_factor(tokens)

    while rest and rest[0] in ('*', '/'):
        operator = rest[0]
        factor, rest = parse_factor(rest[1:])
        if operator == '*':
            result *= factor
        elif operator == '/':
            if factor == 0:
                raise ValueError("Division by zero")
            result /= factor

    return result, rest


def parse_factor(tokens):
    if not tokens:
        raise ValueError("Unexpected end of expression")

    token = tokens[0]
    if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
        return float(token), tokens[1:]
    elif token == '(':
        subexpression, rest = parse_expression(tokens[1:])
        if not rest or rest[0] != ')':
            raise ValueError("Mismatched parentheses")
        return subexpression, rest[1:]
    else:
        raise ValueError(f"Invalid token: {token}")


@app.route('/calculate', methods=['POST'])
def calculator():
    try:
        data = request.get_data(as_text=True)
        result = calculate(data)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)

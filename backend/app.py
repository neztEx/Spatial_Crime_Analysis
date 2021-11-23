import os
from flask import Flask, jsonify
from query_generator import query_builder


app = Flask(__name__)


@app.route('/run_sample', methods=['GET'])
def table():
    try:
        result = query_builder.sample_query(df)
        return result
    except Exception as e:
        print(e)
        return e

if __name__ == '__main__':
    try:
        query_builder.configure_spark()
        app.run(port=os.environ.get('FLASK_PORT', 8080), host='0.0.0.0')
    finally:
        sc.stop()
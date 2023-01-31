from flask import Flask, send_from_directory, render_template
from waitress import serve
from csv_to_html import to_html
# from connect_devices import to_df

app = Flask(__name__)

@app.route('/buildings/files/<string:filename>/')
def get_css(filename):
    return send_from_directory('static', filename)

@app.route('/buildings/<string:code>/')
def get_html(code):
    # to_df()
    return to_html(code)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # serve(app, host='0.0.0.0', port=5000)
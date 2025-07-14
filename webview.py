from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
PLOT_PATH = os.path.join(STATIC_DIR, 'last_plot.png')

@app.route('/')
def index():
    if os.path.exists(PLOT_PATH):
        return render_template_string('''
            <h2>Latest Visualization</h2>
            <img src="/static/last_plot.png" style="max-width:90vw; max-height:80vh; border:1px solid #ccc;"/>
            <p>Refresh this page after generating a new plot.</p>
        ''')
    else:
        return '<h2>No visualization generated yet.</h2>'

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(STATIC_DIR, filename)

if __name__ == '__main__':
    os.makedirs(STATIC_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=8080, debug=True) 
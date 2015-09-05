from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def server():
	return render_template("index.html")

@app.route('/music')
def music_function():
    return test

if __name__ == "__main__":
    app.run()

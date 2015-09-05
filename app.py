from flask import Flask, render_template

from learn import Learn

app = Flask(__name__)
@app.route('/')
def server():
	return render_template("index.html")

@app.route('/music')
def music_function():
    return test

@app.route('/train')
def train_function():
    learner = Learn()
    learner.train()
    learner.saveToFile()
    return server()

if __name__ == "__main__":
    app.run(debug = True)

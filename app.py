from factory import app
from flask import abort

@app.route('/')
def index():
	abort(403)


if __name__ == '__main__':

	app.run(debug=True)
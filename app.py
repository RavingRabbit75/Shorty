from flask import Flask, render_template, redirect, request, url_for
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# If we are in production, make sure we DO NOT use the debug mode
if os.environ.get('ENV') == 'production':
    debug = False

    # Heroku gives us an environment variable called DATABASE_URL when we add a postgres database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

else:
    debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/bitlyClone'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
modus=Modus(app)

class User(db.Model):
	__tablename__ = "users"

	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.Text)
	redirects=db.relationship("Redirect", backref="user", lazy="dynamic")

	def __init__(self, username):
		# needs to be unique
		self.username = username

	def __repr__(self):
		return "User is {}".format(self.username)



class Redirect(db.Model):
	__tablename__ = "redirects"

	id=db.Column(db.Text, primary_key=True)
	url=db.Column(db.Text)
	title=db.Column(db.Text)
	user_id=db.Column(db.Integer, db.ForeignKey("users.id"))

	def __init__(self, url, title, user_id):
		self.url = url
		self.title = title
		self.user_id = user_id

	def __repr__(self):
		return "Redirect for {}".format(self.title)



@app.route("/")
def root():
	return redirect("/users")


@app.route("/users", methods=["GET", "POST"])
def index():
	if request.method=="POST":
		new_user=User(request.form["username"])
		db.session.add(new_user)
		db.session.commit()
	return render_template("users/index.html", users=User.query.all())


@app.route("/users/<int:id>", methods=["GET", "PATCH", "DELETE"])
def show(id):
	found_user=User.query.get(id)
	if found_user==None:
		return render_template("404.html"), 404

	if request.method=="GET":
		return render_template("users/show.html", user=found_user)

	elif request.method == b"PATCH":
		found_user.username = request.form["username"]
		db.session.add(found_user)
		db.session.commit()
		return redirect("/users")

	elif request.method == b"DELETE":
		db.session.delete(found_user)
		db.session.commit()
		return redirect("/users")


	return render_template("users/show.html")


@app.route("/users/new")
def new():
	return render_template("users/new.html")


@app.route("/users/<int:id>/edit")
def edit(id):
	found_user=User.query.get(id)
	return render_template("users/edit.html", user=found_user)


@app.route("/users/<int:id>/redirects", methods=["GET","POST"])
def redirects_index(id):
	from IPython import embed; embed()
	if request.method=="POST":


		new_redirect=Redirect(request.form["new_title"],request.form["new_url"])
		# db.session.add(new_redirect)
		# db.session.commit()

	found_redirects=User.query.get(id).redirects.all()
	found_user=User.query.get(id)
	return render_template("redirects/index.html", redirects=found_redirects, user=found_user)



@app.route("/users/<int:id>/redirects/new")
def redirects_new(id):
	found_user=User.query.get(id)
	return render_template("redirects/new.html", user=found_user)


@app.route("/users/<int:id>/redirects/<redirect_id>", methods=["GET", "PATCH", "DELETE"])
def redirects_show(id, redirect_id):
	found_redirect=Redirect.query.get(redirect_id)
	found_user=User.query.get(id)
	# if found_redirect==None:	
	# 	return render_template("404.html"), 404


	if request.method == b"PATCH":
		found_redirect.url = request.form["original_url"]
		found_redirect.title = request.form["title"]
		db.session.add(found_redirect)
		db.session.commit()
		return redirect(url_for('redirects_index', id=id))

	elif request.method == b"DELETE":
		db.session.delete(found_redirect)
		db.session.commit()
		return redirect(url_for('redirects_index', id=id))

	return render_template("redirects/show.html", redirect=found_redirect, user=found_user)


@app.route("/users/<int:id>/redirects/<redirect_id>/edit")
def redirects_edit(id,redirect_id):
	found_user=User.query.get(id)
	found_redirect=Redirect.query.get(redirect_id)
	return render_template("redirects/edit.html", redirect=found_redirect, user=found_user)



@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404






if __name__ == "__main__":
	app.run(debug=debug)




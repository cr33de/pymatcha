import os
import sys
import base64
import mysql.connector as mySQL

from mysql.connector import errorcode
from flask import Flask, flash, request, redirect, render_template, session
from validate_email import validate_email
from time import time, ctime

sys.path.insert(0, "./incs")

from userAuth import db_connect, credentials, userSignUp, userSignIn, goneSince

# from simplecrypt import encrypt, decrypt
# from binascii import hexlify, unhexlify

from Retrieve import sendEmail
from displayUsers import Home, showUsers
from Notifs import Notifs, notifList

from handleChange import handleUserInfoChange, showBlocked
from ShowMsgsBtwn import MsgsBtwn
from Search import unsearchedUsers

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

def allowed_file(filename):
	return "." in filename and \
	filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

WebApp = Flask(__name__)

@WebApp.route("/")

def index():

	if not session.get("loggedIn"):

		return render_template("loginForm.html")

	else:
		return render_template(
			"dashBoard.html",
			Home = Home(),
			Notifs = Notifs(),
			cards = showUsers([])
		)

@WebApp.route("/login", methods = ["POST"])

def login():

	POST_USERNAME = str(request.form["username"])
	POST_PASSWORD = str(request.form["password"])

	return userSignIn(POST_USERNAME, POST_PASSWORD)

@WebApp.route("/logout")

def logout():

	if session.get("loggedIn"):

		localtime = "gone since " + ctime(time())

		goneSince(session.get("loggedIn"), localtime)

		session["userName"] = None
		session["loggedIn"] = False
		session["uId"] = None

		return index()
	else:
		return index()

#--- Password Retrieving Mechanism ;

@WebApp.route("/passRetrieveForm")

def passRetrieveFrom():

	return render_template("Retrieve.html")

@WebApp.route("/passRetrieve", methods = ["POST"])

def passRetrieve():

	POST_USERNAME = str(request.form["username"])

	if POST_USERNAME == "":
		print("\nfailed to get the userName; type it in the form\n")
	else:
		cnx, cursor = db_connect(credentials)

		if (cnx and cursor):

			q = """
					SELECT *
					FROM `users`
					WHERE username = "{}"
				""".format(
					str(POST_USERNAME)
				)

			try:

				cursor.execute(q)

				R = cursor.fetchall()

				cnx.close()

				if len(R) != 0:

					sendEmail(str(R[0][0]), str(R[0][1 + 1]), str(R[0][5]))

					print("\nan email was sent to %s\n" % str(R[0][5]))

					return index()

			except mySQL.Error as e:

				print(e)

				cnx.close()

				return redirect("/passRetrieveForm")

		else:

			return redirect("/passRetrieveForm")

	return index()

@WebApp.route("/newPasswordForm_<y>")

def newPasswordForm(y):

	cnx, cursor = db_connect(credentials)

	if (cnx and cursor):

		q = """
				SELECT *
				FROM `users`
				WHERE username = "{}"
			""".format(
				str(POST_USERNAME)
			)

		try:

			cursor.execute(q)

			R = cursor.fetchall()

			cnx.close()

			if len(R) != 0:

				return render_template(
					"newPasswordForm.html",
					y = y,
					realName = str(R[0][1 + 1])
				)

		except mySQL.Error as e:

			print(e)

			cnx.close()

			return redirect("/passRetrieveForm")

@WebApp.route("/newPasswordSet_<y>", methods = ["POST"])

def newPasswordSet(y):

	POST_PASSWORD = str(request.form["password"])
	POST_CONFRIM = str(request.form["confirm"])

	if POST_PASSWORD == "" or POST_CONFRIM == "":

		print("\nfailed to get the password; type it in the form\n")

	else:

		if POST_PASSWORD != POST_CONFRIM:

			print("failed to change the password; unconfirmed password")

			return index()

		else:
			# password check
			password = POST_PASSWORD

			upperCFlag = False
			lowerCFlag = False
			numberFlag = False

			for i in password:
				if i.isalpha():
					if i.isupper():
						upperCFlag = True
					elif i.islower():
						lowerCFlag = True
				elif i.isdigit():
					numberFlag = True
			if upperCFlag is False:
				errMsg = "password must include capital latter/s"

				print("failed to sign up; password missing capital latter(s)")
				# flash(errMsg, "warning")
				return render_template("nwusrForm.html", e = errMsg)

			if lowerCFlag is False:
				errMsg = "password must include small latter/s"

				print("failed to sign up; password missing small latter(s)")
				# flash(errMsg, "warning")
				return render_template("nwusrForm.html", e = errMsg)

			if numberFlag is False:
				errMsg = "password must include number/s"

				print("failed to sign up; password missing number(s)")
				# flash(errMsg, "warning")
				return render_template("nwusrForm.html", e = errMsg)

			if len(password) < 8:
				errMsg = "password is too short"

				print("failed to sign up; password is too short")
				# flash(errMsg, "warning")
				return render_template("nwusrForm.html", e = errMsg)

		return index()

@WebApp.route("/passResetFrom")

def passResetFrom():

	return render_template("passResetFrom.html")

@WebApp.route("/passReset", methods = ["POST"])

def passReset():

	return index()

#--- User Info Changing Mechanism ;

@WebApp.route("/profile")

def userProfile():

	if not session["loggedIn"]:

		return render_template("loginForm.html")

	cnx, cursor = db_connect(credentials)

	if (cnx and cursor):

		q = """
				SELECT *
				FROM `users`
				WHERE username = "{}"
			""".format(
				str(session["userName"])
			)

		try:

			cursor.execute(q)

			R = cursor.fetchall()

			cnx.close()

			if len(R) != 0:

				return render_template(
					"userProfile.html",
					Home = Home(),
					Notifs = Notifs(),
					userName = R[0][1],
					gender = 0,
					realName = R[0][1 + 1],
					e_mail = R[0][5],
					pYDL = showBlocked()
				)

		except mySQL.Error as e:

			print(e)

			cnx.close()

			return index()

	else:

		return index()

@WebApp.route("/infoChange", methods = ["GET", "POST"])

def infoChange():

	if not session["loggedIn"]:

		return render_template("loginForm.html")

	POST_USERNAME = str(request.form["username"])
	# ---
	if request.method == "POST":
		gender = request.form.getlist("gender")
		if len(gender) is 1:
			POST_GENDER = "0"
		else:
			POST_GENDER = "1"
	# ---
	POST_REALNAME = str(request.form["realname"])
	# ---
	POST_E_MAIL = str(request.form["e_mail"])
	# ---
	POST_PASSWORD = str(request.form["password"])
	POST_CONFIRM = str(request.form["confirm"])
	# ---
	Biography = str(request.form["biography"])
	Interests = str(request.form["interests"])
	# ---
	POST_SEXUALITY = str(request.form["sexuality"])
	# ---
	handleUserInfoChange(
		POST_USERNAME,
		POST_GENDER,
		POST_REALNAME,
		POST_E_MAIL,
		POST_PASSWORD,
		POST_CONFIRM,
		Biography,
		Interests,
		POST_SEXUALITY
	)

	if request.method == "POST":

		if "file" not in request.files:

			print("No picture chosen")

		else:

			file = request.files["file"]

			if file.filename == "":

				print("No file selected for uploading")

			elif file and allowed_file(file.filename):

				inputStr = base64.b64encode(file.read())

				cnx, cursor = db_connect(credentials)

				if (cnx and cursor):

					q = """
							UPDATE `users`
							SET pic  = "{}"
							WHERE username = "{}"
						""".format(
							str(inputStr)[1 + 1:-1],
							str(session["userName"])
						)

					try:

						cursor.execute(q)

						cnx.commit()

						print("Picture successfully uploaded")

						ChangeFlag = True

						cnx.close()

					except mySQL.Error as e:

						print(q)

						print(e)

						cnx.close()

				return index()

			else:

				print("Not a valied format")

	return index()

@WebApp.route("/deleteUserRoute")

def deleteUserRoute():

	if not session["loggedIn"]:

		return render_template("loginForm.html")

	return render_template("deleteUser.html")

@WebApp.route("/deleteUser")

def deleteUser():

	if not session["loggedIn"]:

		return render_template("loginForm.html")

	cnx, cursor = db_connect(credentials)

	if (cnx and cursor):

		q = """
				DELETE FROM `users`
				WHERE username = "{}"
			""".format(
				str(session["userName"])
			)

		try:

			cursor.execute(q)

			cnx.commit()

			cnx.close()

			print("User No. [\033[1m", end = " ")
			print(session["userName"], end = " ")
			print("\033[0m] just deleted their account")
			session["userName"] = None
			session["loggedIn"] = False

			return index()

		except mySQL.Error as e:

			print(e)

			cnx.close()

			return index()

	else:

		return index()

@WebApp.route("/<x>LikesNo<y>")

def xLikesNoY(x, y):

	if not session["loggedIn"]:

		return render_template("loginForm.html")

	cnx, cursor = db_connect(credentials)

	if (cnx and cursor):

		q = """
				SELECT `liked`
				FROM `likes`
				WHERE liker = {}
			""".format(
				int(x)
			)

		try:

			cursor.execute(q)

			R = cursor.fetchall()

			if len(R) == 0:

				q = """
					INSERT INTO `likes` (
						liker,
						liked
					) VALUES (
						{},
						{}
					)
				""".format(
					str(x),
					str(y)
				)

				try:
					cursor.execute(q)

					cnx.commit()

				except mySQL.Error as e:

					print(e)

					cnx.close()

					return redirect("/")

			else:

				R = [i[0] for i in R]

				print(R)

				if int(y) in R:

					q = """
						DELETE FROM `likes`
						WHERE liker = {}
						AND liked = {}
					""".format(
						str(x),
						str(y)
					)

					try:

						cursor.execute(q)

						cnx.commit()

					except mySQL.Error as e:

						print(e)

						cnx.close()

						return redirect("/")

					# ---

					q = """
						UPDATE `users`
						SET `fameR` = `fameR` - 1
						WHERE uId = {}
					""".format(
						int(y)
					)

					try:

						cursor.execute(q)

						cnx.commit()

					except mySQL.Error as e:

						print(e)

						cnx.close()

					# ---

				else:

					q = """
						INSERT INTO `likes` (
							liker,
							liked
						) VALUES (
							{},
							{}
						)
					""".format(
						str(x),
						str(y)
					)

					try:

						cursor.execute(q)

						cnx.commit()

					except mySQL.Error as e:

						print(e)

						cnx.close()

					# ---

					q = """
						UPDATE `users`
						SET `fameR` = `fameR` + 1
						WHERE uId = {}
					""".format(
						int(y)
					)

					try:

						cursor.execute(q)

						cnx.commit()

					except mySQL.Error as e:

						print(e)

						cnx.close()

					# ---

		except mySQL.Error as e:

			print(e)

			cnx.close()

	cnx.close()

	#---

	cnx, cursor = db_connect(credentials)

	if (cnx and cursor):

		q = """
				SELECT `realName`
				FROM `users`
				WHERE userName = "{}"
			""".format(
				str(session["userName"])
			)

		try:

			cursor.execute(q)

			R = cursor.fetchall()

			realName = R[0][0]

		except mySQL.Error as e:

			print(e)

			cnx.close()

			return redirect("/")

		q = """
			INSERT INTO `notifs` (
				uId,
				content,
				seen
			) VALUES (
				{},
				"{}",
				{}
			)
		""".format(
			str(y),
			"%s liked your profile (at %s)" % (realName, ctime(time())),
			0
		)

		try:

			cursor.execute(q)

			cnx.commit()

			cnx.close()

		except mySQL.Error as e:

			print(e)

			cnx.close()

	#---

	return redirect("/")

@WebApp.route("/blockUserNo<y>")

def blockUserNo(y):

	if not session["loggedIn"]:

		return render_template("loginForm.html")

	cnx, cursor = db_connect(credentials)

	if (cnx and cursor):

		q = """
				SELECT `realName`
				FROM `users`
				WHERE `uId` = {}
			""".format(
				session["uId"]
			)

		try:

			cursor.execute(q)

			R = cursor.fetchall()

			realName = str(R[0][0])

			cnx.close()

		except mySQL.Error as e:

			print(e)

			cnx.close()

	else:

		return index()

	return render_template(
		"blockingForm.html",
		x = session["uId"],
		y = y,
		N = realName
	)

@WebApp.route("/<x>HatesNo<y>", methods = ["POST"])

def xHatesNoY(x, y):

	if not session["loggedIn"]:

		return render_template("loginForm.html")

	POST_REASON = str(request.form["why"])

	if POST_REASON == "":
		POST_REASON = "#NoReason"

	cnx, cursor = db_connect(credentials)

	if (cnx and cursor):

		q = """
				SELECT `realName`
				FROM `users`
				WHERE `uId` = {}
			""".format(
				int(y)
			)

		try:
			cursor.execute(q)

			R = cursor.fetchall()

			realName = str(R[0][0])

		except mySQL.Error as e:

			print(e)

			cnx.close()

			return index()

		q = """
				INSERT INTO `hates` (
					hater,
					hated,
					reason,
					name
				) VALUES (
					{},
					{},
					"{}",
					"{}"
				)
			""".format(
				int(x),
				int(y),
				POST_REASON,
				realName
			)

		try:
			cursor.execute(q)

			cnx.commit()

			cnx.close()

			return index()

		except mySQL.Error as e:

			print(e)

			cnx.close()

			return index()

	else:

		return index()

@WebApp.route("/unblockUserNo<y>")

def unblockUserNo(y):

	if not session["loggedIn"]:

		return render_template("loginForm.html")

	x = session["uId"]

	cnx, cursor = db_connect(credentials)

	if (cnx and cursor):

		q = """
				DELETE FROM `hates`
				WHERE hater = {}
				AND hated = {}
			""".format(
				int(x),
				int(y)
			)

		try:

			cursor.execute(q)

			cnx.commit()

			cnx.close()

			return redirect("/profile")

		except mySQL.Error as e:

			print(e)

			cnx.close()

			return redirect("/profile")

	else:

		return redirect("/profile")

#--- Chat & Notifications Mechanisms ;

@WebApp.route("/notifs")

def notifListRoute():

	if not session["loggedIn"]:

		return render_template("loginForm.html")

	return render_template(
		"notifList.html",
		Home = Home(),
		Notifs = Notifs(),
		notifList = notifList()
	)

@WebApp.route("/<x>chatingTo<y>")

def xChatingToY(x, y):

	if not session["loggedIn"]:

		return render_template("loginForm.html")

	return render_template(
		"xChatingToY.html",
		Home = Home(),
		Notifs = Notifs(),
		Msgs = MsgsBtwn(x, y),
		y = y
	)

@WebApp.route("/sendMsgTo<y>", methods = ["POST"])

def sendMsgToY(y):

	if not session["loggedIn"]:

		return render_template("loginForm.html")

	POST_MESSAGE = str(request.form["yourMsg"])

	cnx, cursor = db_connect(credentials)

	if (cnx and cursor):

		q = """
			INSERT INTO `msgs` (
				`from`,
				`to`,
				`text`
			) VALUES (
				{},
				{},
				"{}"
			)
		""".format(
			int(session["uId"]),
			int(y),
			POST_MESSAGE
		)

		try:

			cursor.execute(q)

			cnx.commit()

			cnx.close()

			return redirect(
				"/%schatingTo%s" % (
					str(session["uId"]),
					str(y)
				)
			)

		except mySQL.Error as e:

			print(e)

			cnx.close()

	return redirect("/")

#--- New User Registration Mechanism ;

@WebApp.route("/nwusrForm/<e>")

def nwusrForm(e):

	errMsg = ""

	if e:
		if int(e) is 1:
			errMsg = "input is incomplete / invalid"
			flash(errMsg, "warning")

		elif int(e) is 2:
			errMsg = "username is already used"
			flash(errMsg, "warning")

		elif int(e) is 3:
			errMsg = "mySQL failure..."
			flash(errMsg, "warning")

		elif int(e) is 4:
			errMsg = "unconfirmed password"
			flash(errMsg, "warning")

		elif int(e) is 5:
			errMsg = "email isn't valid"
			flash(errMsg, "warning")

		elif int(e) is 9:
			# errMsg = "invalid password"
			# flash(errMsg, "warning")
			pass

		elif int(e) is 10:
			errMsg = "userName is shorter than 5 characters"
			flash(errMsg, "warning")

	return render_template("nwusrForm.html", e = errMsg)

@WebApp.route("/signup", methods = ["POST"])

def signup():

	POST_USERNAME = str(request.form["username"])
	POST_REALNAME = str(request.form["realname"])
	POST_PASSWORD = str(request.form["password"])
	POST_REPEAT = str(request.form["repeat"])
	POST_E_MAIL = str(request.form["e_mail"])

	POST_SEXUALITY = str(request.form["sexuality"])

	if not (POST_USERNAME
	   and POST_REALNAME
	   and POST_PASSWORD
	   and POST_REPEAT
	   and POST_E_MAIL
	   and POST_SEXUALITY):

		return redirect("/nwusrForm/01")

	elif POST_USERNAME == "":

		return redirect("/nwusrForm/01")

	elif len(POST_USERNAME) < 5:

		return redirect("/nwusrForm/10")

	cnx, cursor = db_connect(credentials)

	# return str((cnx, cursor))

	if (cnx and cursor):

		q = """
				SELECT *
				FROM `users`
				WHERE username = "{}"
			""".format(
				str(POST_USERNAME)
			)

		try:

			cursor.execute(q)

			if len(cursor.fetchall()) != 0:

				return redirect("/nwusrForm/02")

			cnx.close()

		except mySQL.Error as e:

			print(e)

			cnx.close()

			return redirect("/nwusrForm/03")

	else:

		return redirect("/nwusrForm/03")

	# ---
	if POST_PASSWORD != POST_REPEAT:

		return redirect("/nwusrForm/04")
	# ---

	if not validate_email(POST_E_MAIL):

		return redirect("/nwusrForm/05")
	# ---
	if request.method == "POST":
		gender = request.form.getlist("gender")
		if len(gender) is 1:
			POST_GENDER = "0"
		else:
			POST_GENDER = "1"
	# ---

	return userSignUp(
		POST_USERNAME,
		POST_REALNAME,
		POST_PASSWORD,
		POST_E_MAIL,
		POST_GENDER,
		POST_SEXUALITY
	)

@WebApp.route("/verify<y>")

def verify(y):

	cnx, cursor = db_connect(credentials)

	# return str((cnx, cursor))

	if (cnx and cursor):

		q = """
				UPDATE `users`
				SET active = 1
				WHERE uId = {}
			""".format(
				int(y)
			)

		try:

			cursor.execute(q)

			cnx.commit()

			cnx.close()

			return index()

		except mySQL.Error as e:

			print(e)

			cnx.close()

			infoMsg = "SQL failure..."
			flash(infoMsg, "warning_login")
			return render_template("loginForm.html", e = infoMsg)

	else:

		infoMsg = "SQL failure..."
		flash(infoMsg, "warning_login")
		return render_template("loginForm.html", e = infoMsg)

	pass

# #--- Search / Filter Mechanism ;

@WebApp.route("/search", methods = ["POST"])

def search():
	POST_SEARCH = str(request.form["searchTxt"])

	usersToLeave = unsearchedUsers(POST_SEARCH)

	return render_template(
		"dashBoard.html",
		Home = Home(),
		Notifs = Notifs(),
		cards = showUsers(usersToLeave)
	)

#--- MainFn

if __name__ == "__main__":
	WebApp.secret_key = os.urandom(12)
	WebApp.run(host = "0.0.0.0", port = 4000, debug = True)

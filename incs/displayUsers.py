import mysql.connector as mySQL

from userAuth import db_connect, credentials
from mysql.connector import errorcode
from flask import session, redirect

# ---

def Home():

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

				userPic = R[0][6]

				if R[0][6] is None:
					return "<a href=\"#\" class=\"noPicsHome\">Home</a>"
				else:
					return "<a href=\"/\">Home</a>"

		except mySQL.Error as e:

			print(e)

			cnx.close()

			return redirect("/")

	return redirect("/")

# ---

def grabUsers():

	cnx, cursor = db_connect(credentials)

	if (cnx and cursor):

		q = """
				SELECT *
				FROM `users`
				WHERE username != "{}"
			""".format(
				str(session["userName"])
			)

		try:

			cursor.execute(q)

			R = cursor.fetchall()

			cnx.close()

			if len(R) != 0:

				return R

			else:

				return []

		except mySQL.Error as e:

			print(e)

			cnx.close()

			return redirect("/")

	return -1

def getSexuality(gender, Sexuality):
	if Sexuality == "1":
		return u"⚤"
	elif Sexuality == "0":
		return u"⚥"
	elif Sexuality == "-1":
		if gender == "1":
			return u"⚣"
		else:
			return u"⚢"

def moreUserInfo(userX):

	rStr = "" # str(userX[16]) + ("&#13;" * 2)
	rStr += "Location: " + str(userX[12]) + "&#13;"
	rStr += "Gender: " + (u"♂" if userX[8] == "1" else u"♀") + ", "
	rStr += "Sexuality: " + getSexuality(userX[8], userX[9]) + "&#13;"
	rStr += ("Interests: " + userX[11] + "&#13;") if userX[11] else ""
	rStr += ("Biography: " + userX[10] + "&#13;") if userX[10] else ""
	return rStr

#---

def cardPic(pic):

	htmlImgs = ""
	NoBs = 0

	if pic is not None:
		htmlImgs += "".join((
			# "<img class=\"img_avatar mySlides" src=\"data:image/png;base64, %s"" % (
			# 	r.hget(userId, "pic1")
			# )
			# + "style=\"padding: 2.5px; width: 100%%\">"
			"<div style=\"%s %s %s %s %s %s %s %s %s %s\"></div>" % (
				"background-color: #cccccc;",
				"background-image: url(\'data:image/png;base64, %s\');" % pic,
				"background-repeat: no-repeat;",
				"background-position: center;",
				"background-size: contain;",
				"background-size: cover;",
				"height: 180px;",
				"width: 100%;",
				"border-radius: 3px;",
				"margin-top: -.0px;"
			)
		))
		NoBs += 1

	if NoBs > 1:
		htmlBdgs = ""
		CoCD = 1
		while CoCD <= NoBs:
			htmlBdgs += "".join((
				"<span class=\"w3-badge demo w3-border w3-transparent w3-hover-white\""
				+ "onclick=\"currentDiv({})\"></span>".format(str(CoCD))
			))
			CoCD += 1

		htmlPics = "".join((
			"<div class=\"w3-content w3-display-container\" style=\"min-height:180px\">",
				htmlImgs,
				"<div class=\"w3-center w3-container w3-section w3-large w3-text-white w3-display-bottommiddle\""
				+ "style=\"width:99.99%\">",
					"<div class=\"w3-left w3-hover-text-khaki\" onclick=\"plusDivs(-1)\">&#10094;</div>",
					"<div class=\"w3-right w3-hover-text-khaki\" onclick=\"plusDivs(1)\">&#10095;</div>",
					htmlBdgs,
				"</div>",
			"</div>"
		))
	else:
		htmlPics = "".join((
			"<div class=\"w3-content w3-display-container\" style=\"min-height:180px\">",
				htmlImgs, # <- pic1
				"<div class=\"w3-center w3-container w3-section w3-large w3-text-white w3-display-bottommiddle\""
				+ "style=\"width:99.99%\">",
				"</div>",
			"</div>"
		))

	return None if NoBs is 0 else htmlPics

#---

def TheyLikeThem(x, y):

	cnx, cursor = db_connect(credentials)

	if (cnx and cursor):

		q = """
				SELECT `liked`
				FROM `likes`
				WHERE liker = {}
			""".format(
				str(x)
			)

		try:

			cursor.execute(q)

			R = cursor.fetchall()

			cnx.close()

			if len(R) != 0:

				for i in R:

					if i[0] == y:

						return True

				return False

			else:

				return False

		except mySQL.Error as e:

			print(e)

			cnx.close()

			return redirect("/")

#---

def common_interest(x, y):
	if TheyLikeThem(x, y) and TheyLikeThem(y, x):
		return "<i class=\"far fa-comment-dots\"></i>" # <- &#xf4ad;
	else:
		return ""

#---

def showUsers(usersToLeave):

	users = grabUsers()

	if len(users) == 0:

		return ""

	for i in users : users.remove(i) if i[6] is None else 0

	for i in users : users.remove(i) if i[7] is False else 0

	if usersToLeave is not None and usersToLeave != []:

		for i in usersToLeave : users.remove(i) if i in users else 0

	myInfo = []

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

				myInfo = R[0]

		except mySQL.Error as e:

			print(e)

			cnx.close()

	# removing blocked & blocking users (another approach):

	cnx, cursor = db_connect(credentials)

	if (cnx and cursor):

		q = """
				SELECT `hated`
				FROM `hates`
				WHERE hater = {}
			""".format(
				session["uId"]
			)

		try:

			cursor.execute(q)

			hatedList = [i[0] for i in cursor.fetchall()]

			if len(R) != 0:

				for i in hatedList:

					for j in users:

						if j[0] == i:

							users.remove(j) 

			cnx.close()

			unH = [i[0] for i in users]

		except mySQL.Error as e:

			print(e)

			cnx.close()

			return redirect("/")

	# ---

	cnx, cursor = db_connect(credentials)

	if (cnx and cursor):

		q = """
				SELECT `hater`
				FROM `hates`
				WHERE hated = {}
			""".format(
				session["uId"]
			)

		try:

			cursor.execute(q)

			hatedList = [i[0] for i in cursor.fetchall()]

			if len(R) != 0:

				for i in hatedList:

					for j in users:

						if j[0] == i:

							users.remove(j) 

			cnx.close()

		except mySQL.Error as e:

			print(e)

			cnx.close()

			return redirect("/")

	# ---

	Cards = "<div class=\"dashRow\">"

	C = 0
	while C < len(users):

		if C % 4 is 0:
			Cards += "</div><div class=\"dashRow\">"
		# ---
		Cards += "".join((
			"<div class=\"column\">",
				"<div class=\"card\" title=\"%s\">" % moreUserInfo(users[C]),
					cardPic(users[C][6]),
					"<div class=\"blockBtn\">",
						"<a href=\"/blockUserNo%s\" class=\"blockBtn\">" % str(users[C][0]),
							u"✘",
						"</a>",
					"</div>",
					"<div class=\"likeBtn\">",
						"<a href=\"/%sLikesNo%s\" class=\"likeBtn\" style=\"color: %s\">" % (
							myInfo[0],
							str(users[C][0]),
							"indianred" if TheyLikeThem(myInfo[0], users[C][0]) else "lightgray"
						),
							u"♥",
						"</a>",
					"</div>",
					"<h2 class=\"fameR\">%s</h2>" % str(users[C][15]),
					"<div class=\"container\">",
						"<h4><b>%s <a href=\"%schatingTo%s\" class=\"chatBtn\">%s</a></b></h4>" % (
							users[C][2],
							myInfo[0],
							str(users[C][0]),
							common_interest(myInfo[0], users[C][0])
						),
						"<p>%s</p>" % users[C][10] if users[C][10] is not None else "_",
					"</div>",
				"</div>",
			"</div>"
		))

		# ---

		C += 1

	R = (4 - (len(users) % 4)) if (len(users) % 4) > 0 else 0

	while R > 0:
		Cards += "".join((
			"<div class=\"column\">",
				"<!-- Nothing.. -->",
			"</div>"
		))

		R -= 1

	return Cards

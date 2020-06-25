import mysql.connector as mySQL

from userAuth import db_connect, credentials
from mysql.connector import errorcode
from flask import session, redirect

def Notifs():

	cnx, cursor = db_connect(credentials)

	if (cnx and cursor):

		q = """
				SELECT *
				FROM `notifs`
				WHERE uId = {}
			""".format(
				str(session["uId"])
			)

		try:

			cursor.execute(q)

			R = cursor.fetchall()

			cnx.close()

			if len(R) != 0:

				for i in R:

					if i[3] is 0:

						return "<span style=\"color: red;\"> %s</span>" % u"•"

				return "<span style=\"color: #333;\"> %s</span>" % u"•"

			else:

				return "<span style=\"color: #333;\"> %s</span>" % u"•"

		except mySQL.Error as e:

			print(e)

			cnx.close()

			return redirect("/")

	return redirect("/")

#---

def notifList():

	cnx, cursor = db_connect(credentials)

	if (cnx and cursor):

		q = """
				SELECT content, seen
				FROM `notifs`
				WHERE uId = {}
				ORDER BY timedate DESC
			""".format(
				str(session["uId"])
			)

		try:

			cursor.execute(q)

			R = cursor.fetchall()

			q = """
				UPDATE `notifs`
				SET seen = 1
				WHERE uId = {}
			""".format(
				str(session["uId"])
			)

			try:

				cursor.execute(q)

				cnx.commit()

			except mySQL.Error as e:

				print(e)

				cnx.close()

				return redirect("/")

			cnx.close()

			if len(R) != 0:

				rStr = ""

				for j in R:

					if j[1] == 1:

						rStr += "".join((
							"<div style=\"color: %s;\">" % "gray",
								"<h5 style=\"font-size: 13.5px; Margin-left: 15px;\">",
									u" • "
									+ "%s, " % j[0],
								"</h5>",
							"</div>",
							"<hr>"
						))

					else:

						rStr += "".join((
							"<div style=\"color: %s;\">" % "#303030",
								"<h5 style=\"font-size: 13.5px; Margin-left: 15px;\">",
									u" • "
									+ "%s, " % j[0],
								"</h5>",
							"</div>",
							"<hr>"
						))

			else:

				rStr += "".join((
					"<div style=\"text-align: center; color: gray;\">",
						"<h5>",
							"you don\"t have any notifications yet",
						"</h5>",
					"</div>"
				))

			return rStr

		except mySQL.Error as e:

			print(e)

			cnx.close()

			return redirect("/")

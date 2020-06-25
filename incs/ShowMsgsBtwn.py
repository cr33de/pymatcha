import mysql.connector as mySQL

from mysql.connector import errorcode
from userAuth import db_connect, credentials
from flask import session, redirect
from time import time, ctime

def MsgsBtwn(x, y):

	cnx, cursor = db_connect(credentials)

	if (cnx and cursor):

		q = """
				SELECT *
				FROM `msgs`
				WHERE (`from` = {} AND `to` = {}) OR (`from` = {} AND `to` = {})
				ORDER BY timedate DESC
			""".format(
				int(x),
				int(y),
				int(y),
				int(x)
			)
		try:

			cursor.execute(q)

			msgs = cursor.fetchall()

			rStr = ""

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

				otherName = str(R[0][0])

				cnx.close()

			except mySQL.Error as e:

				print(e)

				cnx.close()

			if len(msgs) != 0:

				for i in msgs:

					if int(i[1]) == int(session["uId"]) or int(i[1]) == int(y):

						rStr += "".join((
							"<div class=\"Msgs\">",
								"<h5 style=\"font-size: 13.5px\">",
									"%s : " % ("you" if int(i[1]) == int(session["uId"]) else otherName)
									+ i[3]
									+ "<br><br><span style=\"color: gray; float: left;\">{}</span>".format(i[4]),
								"</h5>",
							"</div>",
							"<hr>"
						))

			else:

				rStr += "".join((
					"<div style=\"text-align: center; color: gray;\">",
						"<h5>",
							"you didn't start a conversation with %s yet." % otherName,
						"</h5>",
					"</div>"
				))

			return rStr

		except mySQL.Error as e:

			print(e)

			cnx.close()

	return redirect("/")

import mysql.connector as mySQL

from userAuth import db_connect, credentials
from flask import session, flash, redirect
from validate_email import validate_email

def handleUserInfoChange(
	POST_USERNAME,
	POST_GENDER,
	POST_REALNAME,
	POST_E_MAIL,
	POST_PASSWORD,
	POST_CONFIRM,
	Biography,
	Interests,
	POST_SEXUALITY
):

	ChangeFlag = False

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

				Crnt_USERNAME = R[0][1]
				Crnt_GENDER = R[0][8]
				Crnt_REALNAME = R[0][2]
				Crnt_E_MAIL = R[0][5]
				Crnt_Biography = R[0][10]
				Crnt_Interests = R[0][11]
				Crnt_SEXUALITY = R[0][9]

		except mySQL.Error as e:

			print(e)

			cnx.close()

			return redirect("/")

	if POST_USERNAME != "" and POST_USERNAME != Crnt_USERNAME:

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

				if len(R) != 0:

					print("failed to change; userName already exists")

					cnx.close()

				else:

					if len(POST_USERNAME) < 5:

						print("failed to change; userName is shorter than 5 characters")

						cnx.close()

					else:

						q = """
							UPDATE `users`
							SET username  = "{}"
							WHERE username = "{}"
						""".format(
							str(POST_USERNAME),
							str(Crnt_USERNAME)
						)

						cursor.execute(q)

						cnx.commit()

						print("changed userName successfully")

						ChangeFlag = True

						cnx.close()

						Crnt_USERNAME = POST_USERNAME

						session["userName"] = Crnt_USERNAME

			except mySQL.Error as e:

				print(q)

				print(e)

				cnx.close()

	if POST_GENDER != Crnt_GENDER:

		cnx, cursor = db_connect(credentials)

		if (cnx and cursor):

			q = """
					UPDATE `users`
					SET gender  = "{}"
					WHERE username = "{}"
				""".format(
					str(POST_GENDER),
					str(Crnt_USERNAME)
				)

			try:

				cursor.execute(q)

				cnx.commit()

				print("changed gender successfully")

				ChangeFlag = True

				cnx.close()

			except mySQL.Error as e:

				print(q)

				print(e)

				cnx.close()

				return redirect("/profile")

	if POST_REALNAME != "" and POST_REALNAME != Crnt_REALNAME:

		testName = POST_REALNAME.split()

		if len(testName) < 2:

			print("failed to change; Name & Surname are required")

		else:

			cnx, cursor = db_connect(credentials)

			if (cnx and cursor):

				q = """
						UPDATE `users`
						SET realName  = "{}"
						WHERE username = "{}"
					""".format(
						str(POST_REALNAME),
						str(Crnt_USERNAME)
					)

				try:

					cursor.execute(q)

					cnx.commit()

					print("changed gender successfully")

					ChangeFlag = True

					cnx.close()

				except mySQL.Error as e:

					print(q)

					print(e)

					cnx.close()

	if POST_E_MAIL != "" and POST_E_MAIL != Crnt_E_MAIL:

		if not validate_email(POST_E_MAIL):

			print("failed to change; email isn't valid")

		else:

			cnx, cursor = db_connect(credentials)

			if (cnx and cursor):

				q = """
						UPDATE `users`
						SET e_mail  = "{}"
						WHERE username = "{}"
					""".format(
						str(POST_E_MAIL),
						str(Crnt_USERNAME)
					)

				try:

					cursor.execute(q)

					cnx.commit()

					print("changed e_mail successfully")

					ChangeFlag = True

					cnx.close()

				except mySQL.Error as e:

					print(q)

					print(e)

					cnx.close()

	if POST_PASSWORD == "" and POST_CONFIRM != "":

		print("failed to change password; unconfirmed password")

	if POST_PASSWORD != "" and POST_CONFIRM == "":

		print("failed to change password; unconfirmed password")

	if POST_PASSWORD != "" and POST_CONFIRM != "":

		if POST_PASSWORD != POST_CONFIRM:

			print("failed to change password; unconfirmed password")
		else:
			# password check
			passWordChng = 1

			upperCFlag = False
			lowerCFlag = False
			numberFlag = False
			for i in POST_PASSWORD:
				if i.isalpha():
					if i.isupper():
						upperCFlag = True
					elif i.islower():
						lowerCFlag = True
				elif i.isdigit():
					numberFlag = True

			if upperCFlag is False:

				print("failed to change password; password missing capital latter(s)")

			if lowerCFlag is False:

				print("failed to change password; password missing small latter(s)")

			if numberFlag is False:

				print("failed to change password; password missing number(s)")

			if upperCFlag is False or lowerCFlag is False or numberFlag is False:

				passWordChng = -1

			if len(POST_PASSWORD) < 10:

				print("failed to change password; password is too short")

				passWordChng = -1

			if passWordChng > 0:

				cnx, cursor = db_connect(credentials)

				if (cnx and cursor):

					q = """
							UPDATE `users`
							SET password  = "{}"
							WHERE username = "{}"
						""".format(
							str(POST_PASSWORD),
							str(Crnt_USERNAME)
						)

					try:

						cursor.execute(q)

						cnx.commit()

						print("changed password successfully")

						ChangeFlag = True

						cnx.close()

					except mySQL.Error as e:

						print(q)

						print(e)

						cnx.close()

	if Biography != "":

		cnx, cursor = db_connect(credentials)

		if (cnx and cursor):

			q = """
					UPDATE `users`
					SET Biography  = "{}"
					WHERE username = "{}"
				""".format(
					str(Biography),
					str(Crnt_USERNAME)
				)

			try:

				cursor.execute(q)

				cnx.commit()

				print("changed Biography successfully")

				ChangeFlag = True

				cnx.close()

			except mySQL.Error as e:

				print(q)

				print(e)

				cnx.close()

	if Interests != "":

		cnx, cursor = db_connect(credentials)

		if (cnx and cursor):

			q = """
					UPDATE `users`
					SET Interests  = "{}"
					WHERE username = "{}"
				""".format(
					str(Interests),
					str(Crnt_USERNAME)
				)

			try:

				cursor.execute(q)

				cnx.commit()

				print("changed Interests successfully")

				ChangeFlag = True

				cnx.close()

			except mySQL.Error as e:

				print(q)

				print(e)

				cnx.close()

	if POST_SEXUALITY != Crnt_SEXUALITY:

		cnx, cursor = db_connect(credentials)

		if (cnx and cursor):

			q = """
					UPDATE `users`
					SET Sexuality  = "{}"
					WHERE username = "{}"
				""".format(
					str(POST_SEXUALITY),
					str(Crnt_USERNAME)
				)

			try:

				cursor.execute(q)

				cnx.commit()

				print("changed Sexuality successfully")

				ChangeFlag = True

				cnx.close()

			except mySQL.Error as e:

				print(q)

				print(e)

				cnx.close()

	if ChangeFlag is False:

		print("failed to change; nothing to change")

	return redirect("/profile")

def showBlocked():

	cnx, cursor = db_connect(credentials)

	if (cnx and cursor):

		q = """
				SELECT *
				FROM `hates`
				WHERE hater = {}
			""".format(
				session["uId"]
			)

		try:

			cursor.execute(q)

			hatedList = cursor.fetchall()

			cnx.close()

		except mySQL.Error as e:

			print(e)

			cnx.close()

			return redirect("/profile")

	if len(hatedList) is 0:

		return ""

	rStr = ""

	for i in hatedList:

		rStr += "".join((
			"<h5 class=\"blockedList\">",
				u"•"
				+ " [<a href=\"/unblockUserNo%s\">unBlock</a>] " % i[2] + i[4]
				+ (", " + i[3] if i[4] != "#NoReason" else ""),
			"</h5>"
		))

	return rStr

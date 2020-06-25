import mysql.connector as mySQL

from userAuth import db_connect, credentials
from mysql.connector import errorcode
from flask import session, redirect

from displayUsers import grabUsers

def unsearchedUsers(search):

	everyOne = grabUsers()

	search = search.split()

	for i in search:

		# embedded search / filter

		if ":" in i:

			if i.split(":")[0].lower() == "gender":

				if i.split(":")[1].lower() == "male":

					for j in everyOne:

						if j[8] == 1:

							everyOne.remove(j) if j in everyOne else None

				elif i.split(":")[1].lower() == "female":

					for j in everyOne:

						if j[8] == 0:

							everyOne.remove(j) if j in everyOne else None

				else:

					print("failed to filter gender; unrecognised gender")

			elif i.split(":")[0].lower() == "famerate":

				if i.split(":")[1].isnumeric():

					for j in everyOne:

						if int(j[15]) is int(i.split(":")[1]):

							everyOne.remove(j) if j in everyOne else None

				else:

					print("failed to filter fame; unnumeric rate")

		# normal search / filter

		else:

			for j in everyOne:

				if i in str(j[2]).split():

					everyOne.remove(j) if j in everyOne else None

				elif i in str(j[12]).split():

					everyOne.remove(j) if j in everyOne else None

				elif i in str(str(j[11])).split(", "):

					everyOne.remove(j) if j in everyOne else None

	return everyOne

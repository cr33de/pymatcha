
## Setting Up

##### 1st; Making sure you have the following installed :

| requirement     | version | installation command on UNIX / Linux |
| --------------- | ------- | ------------------------------------ |
|                 |         |                                      |
| Python          | ^ 3.6.5 | `brew install python/3`              |
| Flask           | ^ 1.1.x | `pip3 install pandas`                |
| mysql.connector | ^ 2.2.9 | `pip3 install mysql-connector`       |
| validate_email  | ^ 1.3.x | `pip3 install validate_email`        |
| sendgrid        | ^ 6.3.x | `pip3 install sendgrid`              |
|                 |         |                                      |
| mySQL           | ^ 8.0.X | `brew install mysql`                 |

##### 2nd; setting up the database :

Once you have your tools installed, you're good to go. But first be sure to run `python3  DB_config/setUpMyDB.py`, and the script will take care of the work for you (including the insertion of dummy data).

##### 3rd; running the server :

You could run the server by simply running :

`python3 mainFn.py`

where 4000 is your port number.

##### code breakdown :

```
mainFn.py
templates:
	- Retrieve.html
	- blockingForm.html
	- dashBoard.html
	- deleteUser.html
	- loginForm.html
	- newPasswordForm.html
	- notifList.html
	- nwusrForm.html
	- passResetFrom.html
	- userProfile.html
	- xChatingToY.html
static:
	- Flask.svg.png
	- style.css
incs:
	- Notifs.py
	- Retrieve.py
	- Search.py
	- ShowMsgsBtwn.py
	- displayUsers.py
	- handleChange.py
	- userAuth.py
DB_config:
	- setUpMyDB.py
sendgrid.env
```

 - `mainFn.py` is the file that contains the code for running the web server, it contains the declared endpoints and the code to handle them too.

 - `templates/` contains the html renderings of the application's pages, Flask accesses them using render_template().

 - `incs/` contains the logic for the features / functionalities of the application, as explained below:

	- Notifs.py contains the notification display & management functions.
	- Retrieve.py contains the email trafficing functions.
	- Search.py contains the search & fliter implementation.
	- ShowMsgsBtwn.py contains the chat display & management functions.
	- displayUsers.py contains the dashboard display & management functions.
	- handleChange.py contains the profile display & management functions.
	- userAuth.py contains the sign up / sign in functions and their auxiliary functions.

 - `DB_config/` contains the script that sets up the database and is to be ran before running the web server.

 - `sendgrid.env` is a sendgrid utility file that contains the API key.


# PersonalOAuthApplication

# Description
Falsk application to login/register users using google authentication.

Instead of giving user information to every website while registering, we can use google as user authenticator and use only information that google exposes of users.
Only that small spec of Information received from google can be used for user identitification in our applications.

This app implementes a UI interface where users can login/register(both are same in my app as I am not storing info anywhere) using their gmail account.
In the next page it will show the user information which I received from google APIs.


# How to Use.
## Prerequisite:
1. created this app to run on linux.
2. Create Oauth client credentials in google cloud console to get client id and client secret.
   
## Linux(OS):
1. clone the repository on your machine.
2. Install Python depedencies  - < TODO on what dependensies to be installed >
3. create a .env file inside the repository to add these values

```
FLASK_APP=app.py
SECRET_KEY=< generate random string with 16 minimum characters, its a secret so keep this file in .gitignore >
GOOGLE_CLIENT_ID=< this client id you get when you create oauth application on google cloud console >
GOOGLE_CLIENT_SECRET=< this client secret you get when you create oauth application on google cloud console ></this>
```
4. run command ``` flask run ``` to start the sever on https://127.0.0.1:5000
5. open the above url in your browser when you can click on login button and see the information returned from google.

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import datetime
import cgi
import re
# self.response is sort of a global response object
# it sets the content type header to text/plain, by default its text/html

form = """
<form method="post" 
	<strong><h1>Enter some text to ROT13</h1></strong>
	<br>
	<br>
	<textarea name="text" rows="20" cols="100">%(user_output)s</textarea>
	
	<br>
	<input type="submit">
</form>
"""

form2 = """
		<form method="post">
			<strong><h1>Signup Page</h1></strong>
			<br>
			<br>
			<label>Username
				<input type="text" name="username" value="%(username)s">
			</label>
			%(error_username)s
			<br>
			<label>Password
				<input type="password" name="password">
			</label>
			%(error_password)s
			<br>
			<label>Verify Password
				<input type="password" name="verify">
			</label>
			%(error_verify)s
			<br>
			<label>Email(optonal)
				<input type="text" name="email" value="%(email)s">
			</label>
			%(error_email)s
			<br>
			<input type="submit">
		</form>
		"""
def html_escape(s):
	return cgi.escape(s,quote=True)

def ROT13(s):
	i=0
	p = ""
	while  i < len(s) :
		x = ord(s[i])
		if 96<= x <= 122:
			if x+13 > 122 :
				p = p + chr(97 + (x+ 13 - 122 ) -1)
			else:
				p = p + chr(x+13)

		elif 65<= x <= 90:
			if x+13 > 90 :
				p = p + chr(65 + (x+13 - 90 )-1)
			else:
				p=p+chr(x+13)

		else :
			p = p + s[i]

		i=i+1
	return p

def valid_username(s):
	USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
	return USER_RE.match(s)

def valid_password(s):
	USER_RE = re.compile(r"^.{3,20}$")
	return USER_RE.match(s)

def valid_email(s):
	if s == "":
		return True
	USER_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
	return USER_RE.match(s)

class MainPage(webapp2.RequestHandler):
	# when we open MainPage , the browser make a GET Request by default hence we define the get method
	
	def get(self):
		self.response.out.write("new page")
	
	def post(self):
		self.response.out.write("hello")
		
class CipherROT13(webapp2.RequestHandler):

	def write_form(self,user_output=""):
		self.response.out.write(form % {"user_output":user_output})

	def get(self):
		self.write_form()


	def post(self):
		user_input = self.request.get("text")
		user_output=ROT13(user_input)		
		user_output= html_escape(user_output)
		self.write_form(user_output)

class SignupPage(webapp2.RequestHandler):

	def write_form2(self,username="",error_username="",error_password="",error_verify="",email="",error_email=""):
		self.response.out.write(form2 % {"username" : username,
										 "error_username" : error_username,
										 "error_password": error_password,	
										 "error_verify" : error_verify,
										 "email" : email,
										 "error_email" : error_email,
										 })

	def get(self):
		self.write_form2()

	def post(self):
		input_username = self.request.get("username")
		input_password = self.request.get("password")
		input_verify = self.request.get("verify")
		input_email= self.request.get("email")

		error_username = ""
		error_password= ""
		error_email = "" 
		error_verify = ""

		username=valid_username(input_username)
		password= valid_password(input_password)
		email =  valid_email(input_email)
		verify = (input_password==input_verify)

		if (username and password and verify and email):
			self.redirect('/unit2/Welcome?username=%s'%input_username)
		else:
			if not username:
				error_username = "This is not a valid username"
			if not password :
				error_password = " This is not a valid password"
			if not verify:
				error_verify =" The password entered did not match"
			if not email:
				error_email = "This is not a valid email id"

			self.write_form2(input_username,error_username,error_password,error_verify,input_email,error_email)

class WelcomePage(webapp2.RequestHandler):
	
	def get(self):
		input_username= self.request.get("username")
		self.response.out.write("Welcome %s"% input_username)



app = webapp2.WSGIApplication([
	('/',MainPage),('/unit2/ROT13',CipherROT13),('/unit2/Signup',SignupPage),('/unit2/Welcome',WelcomePage)
], debug=True)



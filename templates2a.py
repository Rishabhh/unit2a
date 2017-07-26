import os
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

form_html= """

"""

hidden_html = """
<input type="hidden" name = "food" value = "%s">
"""
items_html = """
<li>%s</li>
"""

shopping_list_html = """
<br>
<br>
<h2>Shopping list </h2>
<ul>
%s
</ul>
"""
class Handler(webapp2.RequestHandler):
	
	def write(self,*a,**kw):
		self.response.out.write(*a,**kw)

	def render_str(self,template,**params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self,template,**kw):
		self.write(self.render_str(template,**kw))

class MainPage(Handler):
	def get(self,name="true"):
		name = self.request.get("name")
		self.render("shopping_list.html",name=name)

		# output = form_html									#how it works is that initially output_hidden is empty but after we enter food for first time 
															# and the form is rendered again, url contains the parameter name="apple" and hence items will
															# not be null this time and hence output_hidden variable is contructed and it actually is a
															# concatenated string of strings like <input type="hidden" name="food" value= "apple">
															# <input type="hidden" name="food" value= "mango"> <input type="hidden" name="food" value= "banana">
															# now this string is substituted in the (%s) of form_html to which output has been equated
															# hence the form is rendered with many query parameters named "food" with different values

															# similarly output_items is a string of type <li>apple</li> <li>mango</li> <li>banana </li>
															# this is then substituted in (%s) of shopping_list_html (which is inside <ul> %s </ul> so a
															# list is formed ) and is assigned to output_shopping and this output shopping is then 
															# CONCATENATED with form_html (output variable actually) so that form_html and shopping list 
															# is displayed on the html page.

		# output_hidden=""
		
		# items = self.request.get_all("food")
		# if items:
		# 	output_items= ""
		# 	for item in items:
		# 		if item :
		# 			output_hidden +=hidden_html % item
					
		# 			output_items += items_html % item

			
		# 	output_shopping = shopping_list_html % output_items   # creates the shopping list's shopping_list_html string with all items
		# 	output += output_shopping     # concatenating the form_html html string with shopping_list_html html string
		
		# output = output % output_hidden    
		
		# self.write(output)


app = webapp2.WSGIApplication([
	('/',MainPage),
], debug=True)
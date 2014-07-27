import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb


import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), '../view/adviser')
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
header_dir = os.path.join(os.path.dirname(__file__), '../view')

JINJA_HEADER_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(header_dir),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def get_user(self):
    if users.get_current_user():
        url = users.create_logout_url(self.request.uri)
        url_linktext ='Logout'
        name = users.get_current_user();
    else:
        url = users.create_login_url(self.request.uri)
        url_linktext = 'Login'
        name=""

    header_values={
        'url': url,
        'url_linktext': url_linktext,
        'name': name
    }
    return header_values
def get_existing_data(first_name,last_name):
    return ndb.gql("SELECT * FROM Adviser where first_name=:fname AND last_name= :lname",fname=first_name,lname=last_name).fetch()

def get_post(self,model):
    model.first_name = self.request.get('first_name')
    model.last_name = self.request.get('last_name')
    model.title = self.request.get('title')
    model.email = self.request.get('email')
    model.phone_number = self.request.get('phone_number')
    model.department = self.request.get('department')
    return model
def write_template(self,template,template_values=None):
    header_values = get_user(self)
    header_template = JINJA_HEADER_ENVIRONMENT.get_template('header.html')
    thesis_header = JINJA_ENVIRONMENT.get_template('adviserNav.html')
    template = JINJA_ENVIRONMENT.get_template(template)
    self.response.write(header_template.render(header_values))
    self.response.write(thesis_header.render())
    if template_values:
        self.response.write(template.render(template_values))
    else:
        self.response.write(template.render())

class Adviser(ndb.Model):
    title = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    phone_number = ndb.StringProperty()
    department = ndb.StringProperty()

class ADVISER_HOME_HANDLER(webapp2.RequestHandler):
    def get(self):
        write_template(self,'adviserHome.html')
        
class ADVISER_NEW_HANDLER(webapp2.RequestHandler):
    def get(self):
        write_template(self,'adviserNew.html')

    def post(self):
        first_name = self.request.get("first_name")
        last_name = self.request.get('last_name')
        email = self.request.get('email')
        adviser_from_db = get_existing_data(first_name,last_name)
        if adviser_from_db:
            for adviser in adviser_from_db:
                adv = adviser
            self.response.write("<script>alert('Adviser Already Exist.'); window.location.assign('/adviser/view/"+str(adv.key.id())+"');</script>")
        else:
            adviser = Adviser()
            adviser = get_post(self,adviser)
            adviser.put();
            self.response.write("<script>alert('Adviser Successfully Added.'); window.location.assign('/adviser/view/"+str(adviser.key.id())+"');</script>")

class ADVISER_LIST_HANDLER(webapp2.RequestHandler):
    def get(self):
        adviser = Adviser.query().fetch()
        header_values = get_user(self)
        template_values = {
            'advisers' : adviser
        }
        write_template(self,'adviserList.html',template_values)

class ADVISER_VIEW_HANDLER(webapp2.RequestHandler):
    def get(self,id):
        adviser = Adviser.get_by_id(long(id))
        if(adviser):
            header_values = get_user(self)
            template_values = {
                'adviser' : adviser
            }
            write_template(self,'adviserView.html',template_values)
        else:
            self.response.write("<script>alert('No Adviser Found'); window.location.assign('/adviser/list')</script>")

    def post(self,id):
        adviser = Adviser.get_by_id(long(id))
        adviser = get_post(self,adviser)
        adviser_from_db = get_existing_data(adviser.first_name,adviser.last_name)
        if(adviser):
            adviser.put();
            header_values = get_user(self)
            template_values = {
                'adviser' : adviser
            }

            write_template(self,'adviserView.html',template_values)
        else:
            self.response.write("<script>alert('No Adviser Found'); window.location.assign('/adviser/list')</script>")

    

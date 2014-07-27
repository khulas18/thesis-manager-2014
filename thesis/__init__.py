import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), '../view/thesis')
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
header_dir = os.path.join(os.path.dirname(__file__), '../view')

JINJA_HEADER_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(header_dir),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def write_template(self,template,template_values=None):
    header_values = get_user(self)
    header_template = JINJA_HEADER_ENVIRONMENT.get_template('header.html')
    nav = JINJA_ENVIRONMENT.get_template('nav.html')
    template = JINJA_ENVIRONMENT.get_template(template)
    self.response.write(header_template.render(header_values))
    self.response.write(nav.render())
    if template_values:
        self.response.write(template.render(template_values))
    else:
        self.response.write(template.render())

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


def get_post(self,model):
    model.title = self.request.get('title')
    model.description = self.request.get('description')
    model.status = self.request.get('status')
    model.school_year = self.request.get('school_year')
    return model

class Research(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    title = ndb.StringProperty()
    description = ndb.StringProperty(indexed=False)
    school_year = ndb.StringProperty()
    status = ndb.StringProperty()

class THESIS_HOME_HANDLER(webapp2.RequestHandler):
    def get(self):
        write_template(self,'home.html')

class THESIS_NEW_HANDLER (webapp2.RequestHandler):
    def get(self):
        write_template(self,'new.html')

    def post(self):
        research = Research()
        research = get_post(self,research)
        a = research.put()
        if a:
            self.response.write("<script>alert('Thesis Successfully Added.'); window.location.assign('/thesis/view/"+str(research.key.id())+"')</script>")
        else:
            self.reponse.write(showAlert("Submission Error. Review your input then try again."),'back');

class THESIS_LIST_HANDLER (webapp2.RequestHandler):
    def get(self):
        researches = Research.query().fetch();
        header_values = get_user(self)
        template_values = {
            'researches' : researches
        }
       
        write_template(self,'list.html',template_values)

class THESIS_VIEW_HANDLER(webapp2.RequestHandler):
    def get(self, id):
        research = Research.get_by_id(long(id))
        template_values = {
            'research' : research
        }
        write_template(self,'view.html',template_values)
    def post(self,id):
        research = Research.get_by_id(long(id))
        research = get_post(self,research)
        research.put()
        self.response.write("<script>alert('Update Successful.'); window.location.assign('/thesis/view/"+id+"')</script>")
        
            
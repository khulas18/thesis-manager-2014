import os
import urllib
import sys

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from student import *
from adviser import *
from thesis import *

template_dir = os.path.join(os.path.dirname(__file__), 'view')
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def get_header(self):
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

def write_template(self,template,template_values=None):
    header_values = get_header(self)
    header_template = JINJA_HEADER_ENVIRONMENT.get_template('header.html')
    template = JINJA_ENVIRONMENT.get_template(template)
    self.response.write(header_template.render(header_values))
    if template_values:
        self.response.write(template.render(template_values))
    else:
        self.response.write(template.render())

class MainPage(webapp2.RequestHandler):

    def get(self):
        write_template(self,'home.html')

class Member1_Handler(webapp2.RequestHandler):

    def get(self):
        write_template(self,'personalwebpage.html')

class Member2_Handler(webapp2.RequestHandler):

    def get(self):
        write_template(self,'personalwebpage2.html')

application = webapp2.WSGIApplication([
    ('/student/home', STUDENT_HOME_HANDLER),
    ('/student/new', STUDENT_NEW_HANDLER),
    ('/student/list', STUDENT_LIST_HANDLER),
    ('/student/view/(.*)', STUDENT_VIEW_HANDLER),
    ('/adviser/home', ADVISER_HOME_HANDLER),
    ('/adviser/new', ADVISER_NEW_HANDLER),
    ('/adviser/list',ADVISER_LIST_HANDLER),
    ('/adviser/view/(.*)', ADVISER_VIEW_HANDLER),
    ('/adviser/edit/(.*)', ADVISER_VIEW_HANDLER),
    ('/thesis/new', THESIS_NEW_HANDLER),
    ('/thesis/list', THESIS_LIST_HANDLER),
    ('/thesis/view/(.*)', THESIS_VIEW_HANDLER),
    ('/thesis/home',THESIS_HOME_HANDLER),
    ('/',MainPage),
    ('/member1',Member1_Handler),
    ('/member2',Member2_Handler)
    
], debug=True)



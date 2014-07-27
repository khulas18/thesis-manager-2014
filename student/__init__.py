import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), '../view/student')
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
header_dir = os.path.join(os.path.dirname(__file__), '../view')

JINJA_HEADER_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(header_dir),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Student(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    student_number = ndb.StringProperty()

def get_existing_data(student_number):
    return ndb.gql("SELECT * FROM Student where student_number=:snumber",snumber=student_number).fetch()

def get_post(self,model):
    model.first_name = self.request.get('first_name')
    model.last_name = self.request.get('last_name')
    model.email = self.request.get('email')
    model.student_number = self.request.get('student_number')
    return model

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

class STUDENT_HOME_HANDLER(webapp2.RequestHandler):
    def get(self):
        write_template(self,'home.html')

class STUDENT_NEW_HANDLER(webapp2.RequestHandler):
    def get(self):
        write_template(self,'new.html')
    #create new entity
    def post(self):
        student = Student()
        get_post(self,student)
        #check if already exist
        existing = get_existing_data(student.first_name,student.last_name)
        if existing:
            for s in existing:
                id = str(s.key.id())
            self.response.write("<script>alert('Student Already Exist.'); window.location.assign('/student/view/"+id+"')</script>")
        else:
            student.put()
            self.response.write("<script>alert('Student Successfully Added.'); window.location.assign('/student/view/"+str(student.key.id())+"')</script>")

class STUDENT_LIST_HANDLER(webapp2.RequestHandler):
    def get(self):
        student_result = Student.query().fetch()
        values = {
            'students': student_result
        }
        write_template(self,'list.html',values)

class STUDENT_VIEW_HANDLER(webapp2.RequestHandler):
    #view entity
    def get(self,id):
        student = Student.get_by_id(long(id))
        values = {
            'student':student
        }
        write_template(self,'view.html',values)
    #update entity then view
    def post(self,id):
        student = Student.get_by_id(long(id))
        student = get_post(self,student)
        exist= get_existing_data(student.student_number)
        update = 1
        for s in exist:
            if s.key.id() != student.key.id():
                update=0
        if update==1:
            student.put()
            self.response.write("<script>alert('Update Successful.')</script>")
        else:
            self.response.write("<script>alert('Failed to update. Duplicate Identity'); window.location.assign('/student/view/"+str(student.key.id())+"')</script>")
        
        values={
            'student': student
        }
        write_template(self,'view.html',values)

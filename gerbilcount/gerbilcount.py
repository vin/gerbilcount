#!/usr/bin/python2.5

import cgi
import os
import wsgiref.handlers

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class Gerbil(db.Model):
    owner = db.UserProperty()
    name = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)


class AddGerbil(webapp.RequestHandler):
    def post(self):
        gerbil = Gerbil()

        if users.get_current_user():
            gerbil.owner = users.get_current_user()

        gerbil.name = self.request.get('name')
        gerbil.put()
        self.redirect('/')


class MainPage(webapp.RequestHandler):
    def get(self):
        gerbils = Gerbil.all().order('-date')

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
                'gerbils' : gerbils,
                'url': url,
                'url_linktext': url_linktext,
                }

        path= os.path.join(os.path.dirname(__file__), 'index.xhtml')
        self.response.headers['Content-Type'] = 'text/xml; charset=utf-8'
        self.response.out.write(template.render(path, template_values))


def main():
    application = webapp.WSGIApplication(
            [('/', MainPage),
                ('/add', AddGerbil)],
            debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()

import webapp2
import os
import jinja2

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Content(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class CastanoBlog(Handler):
    def render_front(self, subject="", content="", contents=""):
        contents = db.GqlQuery("SELECT * FROM Content ORDER BY created DESC")

        self.render("blog.html", subject = subject, content = content, contents = contents)

    def get(self):
        self.render_front()

class NewPost(Handler):
    def render_newpost(self, subject="", content="", error=""):

        self.render("newpost.html", subject = subject, content = content, error = error)

    def get(self):
        self.render_newpost()

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            a = Content(subject = subject, content = content)
            a.put()
            self.redirect("/")
        else:
            error = "We need both a subject and content!"
            self.render_newpost(subject, content, error)


app = webapp2.WSGIApplication([
    ('/', CastanoBlog),
    ('/newpost', NewPost),
])
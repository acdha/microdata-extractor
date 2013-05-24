# encoding: utf-8

import datetime
import json
import os
import urllib
import sys

sys.path.insert(0, "html5lib")
sys.path.insert(0, "microdata")

import jinja2
import webapp2

import microdata


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                                       extensions=['jinja2.ext.autoescape'])

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())


class ExtractionHandler(webapp2.RequestHandler):
    def get(self):
        url = self.request.get('url')
        if not url:
            self.redirect('/')

        extracted = {}
        extracted['items'] = items = []

        url_contents = urllib.urlopen(url).read()

        for item in microdata.get_items(url_contents):
            items.append(item.json_dict())

        context = {
            "url": url,
            "request_url": self.request.url,
            "extracted": json.dumps(extracted, indent=4),
            "items": items,
            "access_date": datetime.date.today(),
            "show_wikipedia": self.request.get('wikipedia', 'off') == 'on'
        }

        best_match = self.request.accept.best_match(['application/json', 'text/html'])
        if best_match == 'application/json':
            self.response.content_type = 'application/json'
            self.response.write(context['extracted'])
        else:
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render(context))


app = webapp2.WSGIApplication([
    (r'/extract/', ExtractionHandler),
    (r'/', MainHandler),
], debug=True)

# encoding: utf-8

import datetime
import json
import os
from urlparse import urlsplit

import jinja2
import microdata
import requests
from flask import Flask, make_response, redirect, request

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_DIR), extensions=["jinja2.ext.autoescape"]
)


app = Flask(__name__)


@app.route("/")
def index():
    template = JINJA_ENVIRONMENT.get_template("index.html")
    return template.render()


@app.route("/extract/")
def extract_microdata():
    url = request.args.get("url")
    if not url:
        return redirect("/")

    extracted = {}
    extracted["items"] = items = []

    resp = requests.get(url)
    resp.raise_for_status()
    url_contents = resp.content

    for item in microdata.get_items(url_contents):
        items.append(item.json_dict())

    context = {
        "url": url,
        "request_url": url,
        "extracted": json.dumps(extracted, indent=4),
        "items": items,
        "access_date": datetime.date.today(),
        "show_wikipedia": request.args.get("wikipedia", "off") == "on",
    }

    url_parts = urlsplit(url)
    site_name = url_parts.netloc
    if site_name.endswith("wdl.org"):
        site_name = "WDL"
        wiki_site_name = "[[World Digital Library]]"
    else:
        wiki_site_name = site_name

    context["site_name"] = site_name
    context["wiki_site_name"] = wiki_site_name

    if "text/html" in request.headers.get("Accept", ""):
        template = JINJA_ENVIRONMENT.get_template("index.html")
        return template.render(context)
    else:
        return context["extracted"], 200, {"Content-Type": "application/json"}


if __name__ == "__main__":
    app.run()

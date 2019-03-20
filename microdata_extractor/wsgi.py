# /usr/bin/env python3

import datetime
import json
import os
from urllib.parse import urlsplit

import jinja2
import microdata
import requests
from flask import Flask, redirect, request

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_DIR), extensions=["jinja2.ext.autoescape"]
)


def clean_strings_recursively(obj):
    if isinstance(obj, list):
        return [clean_strings_recursively(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: clean_strings_recursively(v) for k, v in obj.items()}
    elif isinstance(obj, str):
        return obj.strip()
    else:
        return obj


application = Flask(__name__)


@application.route("/")
def index():
    template = JINJA_ENVIRONMENT.get_template("index.html")
    return template.render()


@application.route("/extract/")
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
        items.append(clean_strings_recursively(item.json_dict()))

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
    port = os.getenv("PORT", "5000")
    application.run(port=int(port))

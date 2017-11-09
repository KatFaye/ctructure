# base_page.py
# Create a blueprint for rendering template pages
# Author: Kat Herring
# Date: 11/7/2017

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

base_page = Blueprint('base_page', __name__,
                        template_folder='templates')

@base_page.route('/', defaults={'page': 'index'})
@base_page.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)

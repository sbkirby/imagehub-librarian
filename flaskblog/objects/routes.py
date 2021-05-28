"""
objects/routes.py

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Objects, ImageObjects
from flaskblog.objects.forms import ObjectsForm

objects = Blueprint('objects', __name__)


@objects.route("/objects")
def objects_list():
    page = request.args.get('page', 1, type=int)
    object_list = Objects.query.order_by(Objects.ObjectName.desc()).paginate(page=page, per_page=30)
    return render_template('objects.html', objects=object_list, title='Select Object')


@objects.route("/object/new", methods=['GET', 'POST'])
@login_required
def add_object():
    form = ObjectsForm()
    if form.validate_on_submit():
        object = Objects(ObjectName=form.ObjectName.data)
        db.session.add(object)
        db.session.commit()
        flash('Your Object has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_object.html', title='New Object',
                           form=form, legend='New Object')


@objects.route("/object/<int:object_id>")
def object(object_id):
    object = Objects.query.get_or_404(object_id)
    return render_template('object.html', object=object, title='Object: ' + object.ObjectName)


@objects.route("/object/<int:object_id>/update", methods=['GET', 'POST'])
@login_required
def update_object(object_id):
    object = Objects.query.get_or_404(object_id)
    form = ObjectsForm()
    if form.validate_on_submit():
        object.ObjectName = form.ObjectName.data
        db.session.commit()
        flash('Your ALPR Event has been updated!', 'success')
        return redirect(url_for('objects.object', object_id=object.ID))
    elif request.method == 'GET':
        form.ObjectName.data = object.ObjectName
    return render_template('create_object.html', title='Update Object',
                           form=form, legend='Update Object')


@objects.route("/object/<int:object_id>/images")
def object_images(object_id):
    page = request.args.get('page', 1, type=int)
    object = Objects.query.get_or_404(object_id)
    images = ImageObjects.query.filter_by(object_id=object.ObjectName)\
        .order_by(ImageObjects.datetime.desc())\
        .paginate(page=page, per_page=30)
    return render_template('object_images.html', images=images, object=object, title='Object: ' + object.ObjectName)


@objects.route("/object/<int:object_id>/delete", methods=['POST'])
@login_required
def delete_object(object_id):
    object = Objects.query.get_or_404(object_id)
    db.session.delete(object)
    db.session.commit()
    flash('Your object event has been deleted!', 'success')
    return redirect(url_for('main.home'))

"""
imageobjs/routes.py

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import ImageObjects, Objects
from flaskblog.imageobjs.forms import ImageObjectsForm, ImageObjectsSelectForm

imageobjs = Blueprint('imageobjs', __name__)


@imageobjs.route("/imageobjs")
def imageobjs_list():
    page = request.args.get('page', 1, type=int)
    imageobj_list = ImageObjects.query.order_by(ImageObjects.ID.desc()).paginate(page=page, per_page=30)
    return render_template('imageobjs.html', imageobjs=imageobj_list, title='Image Objects')


@imageobjs.route("/imageobj/<int:imageobj_id>")
def imageobj(imageobj_id):
    imageobj = ImageObjects.query.get_or_404(imageobj_id)
    return render_template('imageobj.html', imageobj=imageobj, title='Image Object: ' + imageobj.object_id)


@imageobjs.route("/imageobj/<int:imageobj_id>/update", methods=['GET', 'POST'])
@login_required
def update_imageobj(imageobj_id):
    imageobj = ImageObjects.query.get_or_404(imageobj_id)
    form = ImageObjectsSelectForm()
    form.object_id.choices = [(object.ObjectName, object.ObjectName) for object in
                               Objects.query.order_by(Objects.ObjectName).all()]
    if form.validate_on_submit():
        imageobj.datetime = form.datetime.data
        imageobj.image_id = form.image_id.data
        imageobj.object_id = form.object_id.data
        imageobj.count = form.count.data
        db.session.commit()
        flash('Your Image Object has been updated!', 'success')
        return redirect(url_for('imageobjs.imageobj', imageobj_id=imageobj.ID))
    elif request.method == 'GET':
        form.datetime.data = imageobj.datetime
        form.image_id.data = imageobj.image_id
        form.object_id.process_data(imageobj.object_id)
        form.count.data = imageobj.count
    return render_template('create_imageobj.html', title='Update Image Object',
                           form=form, legend='Update Image Object')


@imageobjs.route("/imageobj/<int:imageobj_id>/delete", methods=['POST'])
@login_required
def delete_imageobj(imageobj_id):
    imageobj = ImageObjects.query.get_or_404(imageobj_id)
    db.session.delete(imageobj)
    db.session.commit()
    flash('Your Object has been deleted!', 'success')
    return redirect(url_for('main.home'))

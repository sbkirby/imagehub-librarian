"""
images/routes.py

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Images, CameraNodes
from flaskblog.images.forms import ImagesForm, ImagesSelectForm

images = Blueprint('images', __name__)


@images.route("/images")
def images_list():
    page = request.args.get('page', 1, type=int)
    image_list = Images.query.order_by(Images.datetime.desc()).paginate(page=page, per_page=30)
    return render_template('images.html', images=image_list, title='Images from all Cameras')


@images.route("/image/<string:image_id>")
def image(image_id):
    image = Images.query.get_or_404(image_id)
    return render_template('image.html', image=image, title='Image: ' + image.image)


@images.route("/image/new", methods=['GET', 'POST'])
@login_required
def add_image():
    form = ImagesSelectForm()
    form.camera_id.choices = [(camera.ID, camera.NodeName)
                               for camera in CameraNodes.query.order_by(CameraNodes.NodeName).all()]
    if form.validate_on_submit():
        image = Images(image=form.image.data,
                     camera_id=form.camera_id.data,
                     ViewName=form.ViewName.data,
                     size=form.size.data)
        db.session.add(image)
        db.session.commit()
        flash('Your image has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_image.html', title='New Image',
                           form=form, legend='New Image')


@images.route("/image/<string:image_id>/update", methods=['GET', 'POST'])
@login_required
def update_image(image_id):
    image = Images.query.get_or_404(image_id)
    form = ImagesSelectForm()
    form.camera_id.choices = [(camera.ID, camera.NodeName)
                               for camera in CameraNodes.query.order_by(CameraNodes.NodeName).all()]
    if form.validate_on_submit():
        image.datetime = form.datetime.data
        image.image = form.image.data
        image.camera_id = form.camera_id.data
        image.ViewName = form.ViewName.data
        image.size = form.size.data
        db.session.commit()
        flash('Your image has been updated!', 'success')
        return redirect(url_for('images.image', image_id=image.datetime))
    elif request.method == 'GET':
        form.datetime.data = image.datetime
        form.image.data = image.image
        form.camera_id.process_data(image.camera_id)
        form.ViewName.data = image.ViewName
        form.size.data = image.size
    return render_template('create_image.html', title='Update Image',
                           form=form, legend='Update Image')


@images.route("/image/<string:image_id>/delete", methods=['POST'])
@login_required
def delete_image(image_id):
    image = Images.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()
    flash('Your image has been deleted!', 'success')
    return redirect(url_for('main.home'))

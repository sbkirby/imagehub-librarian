
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db

"""
cameras/routes.py

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""
from flaskblog.models import CameraNodes, Images
from flaskblog.cameras.forms import CameraNodesForm

cameras = Blueprint('cameras', __name__)


@cameras.route("/cameras")
def cameras_list():
    page = request.args.get('page', 1, type=int)
    camera_list = CameraNodes.query.order_by(CameraNodes.ViewName).paginate(page=page, per_page=10)
    return render_template('cameras.html', cameras=camera_list, title='Select Camera')


@cameras.route("/camera/new", methods=['GET', 'POST'])
@login_required
def add_camera():
    form = CameraNodesForm()
    if form.validate_on_submit():
        camera = CameraNodes(NodeName=form.NodeName.data,
                             ViewName=form.ViewName.data,
                             CameraType=form.CameraType.data,
                             Display=form.Display.data,
                             Chk_Objects=form.Chk_Objects.data,
                             ALPR=form.ALPR.data,
                             ROI_name=form.ROI_name.data,
                             Message=form.Message.data,
                             Twilio_Enabled=form.Twilio_Enabled.data)
        db.session.add(camera)
        db.session.commit()
        flash('Your camera has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_camera.html', title='New Camera',
                           form=form, legend='New Camera')


@cameras.route("/camera/<int:camera_id>")
def camera(camera_id):
    camera = CameraNodes.query.get_or_404(camera_id)
    return render_template('camera.html', title=camera.NodeName, camera=camera)


@cameras.route("/camera/<int:camera_id>/update", methods=['GET', 'POST'])
@login_required
def update_camera(camera_id):
    camera = CameraNodes.query.get_or_404(camera_id)
    form = CameraNodesForm()
    if form.validate_on_submit():
        camera.NodeName = form.NodeName.data
        camera.ViewName = form.ViewName.data
        camera.CameraType = form.CameraType.data
        camera.Display = form.Display.data
        camera.Chk_Objects = form.Chk_Objects.data
        camera.ALPR = form.ALPR.data
        camera.ROI_name = form.ROI_name.data
        camera.Message = form.Message.data
        camera.Twilio_Enabled = form.Twilio_Enabled.data
        db.session.commit()
        flash('Your camera has been updated!', 'success')
        return redirect(url_for('cameras.camera', camera_id=camera.ID))
    elif request.method == 'GET':
        form.NodeName.data = camera.NodeName
        form.ViewName.data = camera.ViewName
        form.CameraType.data = camera.CameraType
        form.Display.data = camera.Display
        form.Chk_Objects.data = camera.Chk_Objects
        form.ALPR.data = camera.ALPR
        form.ROI_name.data = camera.ROI_name
        form.Message.data = camera.Message
        form.Twilio_Enabled.data = camera.Twilio_Enabled
    return render_template('create_camera.html', title='Update Camera',
                           form=form, legend='Update Camera')


@cameras.route("/camera/<int:camera_id>/images")
def camera_images(camera_id):
    page = request.args.get('page', 1, type=int)
    camera = CameraNodes.query.get_or_404(camera_id)
    images = Images.query.filter_by(camera_id=camera.ID)\
        .order_by(Images.image.desc())\
        .paginate(page=page, per_page=30)
    return render_template('camera_images.html', images=images, camera=camera, title='Camera: ' + camera.NodeName)


@cameras.route("/camera/<int:camera_id>/delete", methods=['POST'])
@login_required
def delete_camera(camera_id):
    camera = CameraNodes.query.get_or_404(camera_id)
    db.session.delete(camera)
    db.session.commit()
    flash('Your camera has been deleted!', 'success')
    return redirect(url_for('main.home'))

"""
events/routes.py

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Events, CameraNodes
from flaskblog.events.forms import EventsForm
from sqlalchemy import func, select, column, alias, text

events = Blueprint('events', __name__)


@events.route("/events")
def events_list():
    page = request.args.get('page', 1, type=int)
    events_list = Events.query.order_by(Events.hubEvent.desc()).paginate(page=page, per_page=30)
    return render_template('events.html', events=events_list, title='Events')


@events.route("/event/<int:event_id>")
def event(event_id):
    event = Events.query.get_or_404(event_id)
    return render_template('event.html', title=event.event.NodeName, event=event)


@events.route("/event/<int:event_id>/update", methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    event = Events.query.get_or_404(event_id)
    form = EventsForm()
    form.camera_id.choices = [(camera.ID, camera.NodeName)
                               for camera in CameraNodes.query.order_by(CameraNodes.NodeName).all()]
    if form.validate_on_submit():
        event.datetime = form.datetime.data
        event.hubEvent = form.hubEvent.data
        event.camera_id = form.camera_id.data
        event.Event = form.Event.data
        event.Value = form.Value.data
        event.ROI_name = form.ROI_name.data
        db.session.commit()
        flash('Your Event has been updated!', 'success')
        return redirect(url_for('events.event', event_id=event.hubEvent))
    elif request.method == 'GET':
        form.datetime.data = event.datetime
        form.hubEvent.process_data(event.hubEvent)
        form.camera_id.data = event.camera_id
        form.Event.data = event.Event
        form.Value.data = event.Value
        form.ROI_name.data = event.ROI_name
    return render_template('create_event.html', title='Update Event',
                           form=form, legend='Update Event')


@events.route("/event/last_events")
def last_events():
    page = request.args.get('page', 1, type=int)
    events_list = Events.query.filter_by(camera_id=camera.ID)\
        .order_by(Events.hubEvent.desc())\
        .paginate(page=page, per_page=50)
    return render_template('camera_events.html', events=events_list, camera=camera, title='Events: ' + camera.NodeName)


@events.route("/event/<int:camera_id>/events")
def camera_events(camera_id):
    page = request.args.get('page', 1, type=int)
    camera = CameraNodes.query.get_or_404(camera_id)
    events_list = Events.query.filter_by(camera_id=camera.ID)\
        .order_by(Events.hubEvent.desc())\
        .paginate(page=page, per_page=50)
    return render_template('camera_events.html', events=events_list, camera=camera, title='Events: ' + camera.NodeName)


@events.route("/event/<int:event_id>/delete", methods=['POST'])
@login_required
def delete_event(event_id):
    event = Events.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Your Event has been deleted!', 'success')
    return redirect(url_for('main.home'))


@events.route("/events/latest", methods=['GET', 'POST'])
# @login_required
def latest_events():
    page = request.args.get('page', 1, type=int)
    events_list = db.session.query(Events.camera_id, func.max(Events.hubEvent).label("max_hubEvent"), Events.Event, Events.Value, Events.ROI_name)\
        .group_by(Events.camera_id) \
        .filter(Events.camera_id.in_([1, 2, 3, 4, 8])) \
        .paginate(page=page, per_page=50)
    return render_template('latest_events.html', title='Latest Events for each Camera', events=events_list)


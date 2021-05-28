"""
alprs/routes.py

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import AlprEvents, LicensePlates
from flaskblog.alprs.forms import AlprEventsForm

alprs = Blueprint('alprs', __name__)


@alprs.route("/alprs")
def alprs_list():
    page = request.args.get('page', 1, type=int)
    alpr_list = AlprEvents.query.order_by(AlprEvents.ID.desc()).paginate(page=page, per_page=48)
    return render_template('alprs.html', alprs=alpr_list, title='ALPR Events')


@alprs.route("/alpr/<int:alpr_id>")
def alpr(alpr_id):
    alpr = AlprEvents.query.get_or_404(alpr_id)
    return render_template('alpr.html', title=alpr.licenseplates.license, alpr=alpr)


@alprs.route("/alpr/<int:alpr_id>/update", methods=['GET', 'POST'])
@login_required
def update_alpr(alpr_id):
    alpr = AlprEvents.query.get_or_404(alpr_id)
    form = AlprEventsForm()
    form.license_id.choices = [(license.ID, license.license)
                               for license in LicensePlates.query.order_by(LicensePlates.license).all()]
    if form.validate_on_submit():
        alpr.license_id = form.license_id.data
        alpr.datetime = form.datetime.data
        alpr.image_id = form.image_id.data
        alpr.processing_time = form.processing_time.data
        db.session.commit()
        flash('Your ALPR Event has been updated!', 'success')
        return redirect(url_for('alprs.alpr', alpr_id=alpr.ID))
    elif request.method == 'GET':
        form.license_id.process_data(alpr.license_id)
        form.datetime.data = alpr.datetime
        form.image_id.data = alpr.image_id
        form.processing_time.data = alpr.processing_time
    return render_template('create_alpr.html', title='Update ALPR Event',
                           form=form, legend='Update ALPR Event')


@alprs.route("/alpr/<int:alpr_id>/delete", methods=['POST'])
@login_required
def delete_alpr(alpr_id):
    alpr = AlprEvents.query.get_or_404(alpr_id)
    db.session.delete(alpr)
    db.session.commit()
    flash('Your alpr event has been deleted!', 'success')
    return redirect(url_for('main.home'))

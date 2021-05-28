"""
plates/routes.py

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import LicensePlates, AlprEvents
from flaskblog.plates.forms import LicensePlatesForm, LicensePlatesLookupForm

plates = Blueprint('plates', __name__)


@plates.route("/plates", methods=['GET', 'POST'])
def plates_list():
    form = LicensePlatesLookupForm()
    form.license.choices = [(license.ID, license.license) for license in
                               LicensePlates.query.order_by(LicensePlates.license).all()]
    plate = LicensePlates(license=form.license.choices)
    if form.validate_on_submit():
        plate.license = form.license.data
        if (request.args.get('link_id') == "images"):
            return redirect(url_for('plates.plate_images', plate_id=form.license.data))
        if (request.args.get('link_id') == "update"):
            return redirect(url_for('plates.plate', plate_id=form.license.data))
        else:
            return render_template('plates.html', title='Try Again - Select License Plate',
                                   form=form, legend='Try Again - Select License Plate')
    elif request.method == 'GET':
        form.license.data = plate.license
    return render_template('plates.html', title='Select License Plate',
                           form=form, legend='Select License Plate')


@plates.route("/plate/new", methods=['GET', 'POST'])
@login_required
def add_plate():
    form = LicensePlatesForm()
    if form.validate_on_submit():
        plate = LicensePlates(license=form.license.data,
                             color=form.color.data,
                             type=form.type.data,
                             identified=form.identified.data)
        db.session.add(plate)
        db.session.commit()
        flash('Your License Plate has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_plate.html', title='New License Plate',
                           form=form, legend='New License Plate')


@plates.route("/plate/<int:plate_id>")
def plate(plate_id):
    plate = LicensePlates.query.get_or_404(plate_id)
    return render_template('plate.html', plate=plate, title='License Plate: ' + plate.license)


@plates.route("/plate/<int:plate_id>/update", methods=['GET', 'POST'])
@login_required
def update_plate(plate_id):
    plate = LicensePlates.query.get_or_404(plate_id)
    form = LicensePlatesForm()
    if form.validate_on_submit():
        plate.license = form.license.data
        plate.color = form.color.data
        plate.type = form.type.data
        plate.identified = form.identified.data
        db.session.commit()
        flash('Your License Plate has been updated!', 'success')
        return redirect(url_for('plates.plate', plate_id=plate.ID))
    elif request.method == 'GET':
        form.license.process_data(plate.license)
        form.color.data = plate.color
        form.type.data = plate.type
        form.identified.data = plate.identified
    return render_template('create_plate.html', title='Update License Plate',
                           form=form, legend='Update License Plate')


@plates.route("/plate/<int:plate_id>/images")
def plate_images(plate_id):
    page = request.args.get('page', 1, type=int)
    plate = LicensePlates.query.get_or_404(plate_id)
    images = AlprEvents.query.filter_by(license_id=plate_id)\
        .order_by(AlprEvents.image_id.desc())\
        .paginate(page=page, per_page=30)
    return render_template('plate_images.html', images=images, plate=plate, title='License Plate: ' + plate.license)


@plates.route("/plate/<int:plate_id>/delete", methods=['POST'])
@login_required
def delete_plate(plate_id):
    plate = LicensePlates.query.get_or_404(plate_id)
    db.session.delete(plate)
    db.session.commit()
    flash('Your License Plate has been deleted!', 'success')
    return redirect(url_for('main.home'))

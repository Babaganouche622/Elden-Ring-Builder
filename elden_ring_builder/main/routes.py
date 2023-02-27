"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from elden_ring_builder.models import User, Build
from elden_ring_builder.main.forms import CreateBuildForm

# Import app and db from events_app package so that we can run app
from elden_ring_builder.extensions import app, db, bcrypt

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def home():
    all_builds = Build.query.all()
    print(all_builds)
    all_users = User.query.all()
    print(all_users)
    return render_template('home.html', all_users=all_users, all_builds=all_builds)

# route for create_build
@main.route('/create_build', methods=['GET', 'POST'])
@login_required
def create_build():
    form = CreateBuildForm()
    if form.validate_on_submit():
        build = Build(
            name=form.name.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(build)
        db.session.commit()
        return redirect(url_for('main.home', build_id=build.id))
    return render_template('create_build.html', form=form)

# route for build_detail
@main.route('/build_detail/<int:build_id>', methods=['GET', 'POST'])
def build_detail(build_id):
    build = Build.query.get(build_id)
    form = CreateBuildForm(obj=build)
    
    if form.validate_on_submit():
        build.name = form.name.data
        build.description = form.description.data

        db.session.commit()

        flash('Build Was updated')
        return redirect(url_for('main.build_detail', build_id=build.id))

    return render_template('build_detail.html', build=build, form=form)

# route for delete_build
@main.route('/delete_build/<int:build_id>')
def delete_build(build_id):
    build = Build.query.filter_by(id=build_id).one()
    db.session.delete(build)
    db.session.commit()
    return redirect(url_for('main.home'))

# route for profile
@main.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).one()
    return render_template('profile.html', user=user)

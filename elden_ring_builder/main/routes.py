"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from elden_ring_builder.models import User, Build, Weapon
from elden_ring_builder.main.forms import CreateBuildForm, CreateWeaponForm

# Import app and db from events_app package so that we can run app
from elden_ring_builder.extensions import app, db, bcrypt

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def home():
    all_builds = Build.query.all()
    all_users = User.query.all()
    all_weapons = Weapon.query.all()
    return render_template('home.html', 
    all_users=all_users, 
    all_builds=all_builds, 
    all_weapons=all_weapons)

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
    all_weapons = Weapon.query.all()

    if form.validate_on_submit():
        build.name = form.name.data
        build.description = form.description.data

        db.session.commit()

        flash('Build Was updated')
        return redirect(url_for('main.build_detail', build_id=build.id))

    return render_template('build_detail.html', build=build, form=form, all_weapons=all_weapons)

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
    if current_user.is_anonymous:
        return redirect(url_for('main.home'))
    if current_user.username != username:
        return redirect(url_for('main.home'))
    user = User.query.filter_by(username=username).one()
    return render_template('profile.html', user=user)

# route for creating weapon
@main.route('/create_weapon', methods=['GET', 'POST'])
def create_weapon():
    form = CreateWeaponForm()

    if form.validate_on_submit():
        weapon = Weapon(
            name=form.name.data,
            image=form.image.data,
        )
        db.session.add(weapon)
        db.session.commit()
        return redirect(url_for('main.weapon_detail', weapon_id=weapon.id))

    return render_template('create_weapon.html', form=form)

# route for delete_weapon
@main.route('/delete_weapon/<int:weapon_id>')
def delete_weapon(weapon_id):
    weapon = Weapon.query.filter_by(id=weapon_id).one()
    db.session.delete(weapon)
    db.session.commit()
    return redirect(url_for('main.home'))

# route for weapon_detail
@main.route('/weapon_detail/<int:weapon_id>', methods=['GET', 'POST'])
def weapon_detail(weapon_id):
    weapon = Weapon.query.get(weapon_id)
    form = CreateWeaponForm(obj=weapon)

    if form.validate_on_submit():
        weapon.name = form.name.data
        weapon.image = form.image.data

        db.session.commit()

        flash('Weapon Was updated')
        return redirect(url_for('main.weapon_detail', weapon_id=weapon.id))

    return render_template('weapon_detail.html', weapon=weapon, form=form)


# route for adding a weapon to a build
@main.route('/add_weapon/<int:build_id>/<int:weapon_id>', methods=['POST'])
def add_weapon(build_id, weapon_id):
    build = Build.query.get(build_id)
    weapon = Weapon.query.get(weapon_id)
    build.weapon.append(weapon)
    db.session.add(build)
    db.session.commit()
    return redirect(url_for('main.build_detail', build_id=build.id))

# route for removing a weapon from a build
@main.route('/remove_weapon/<int:build_id>/<int:weapon_id>', methods=['POST'])
def remove_weapon(build_id, weapon_id):
    build = Build.query.get(build_id)
    weapon = Weapon.query.get(weapon_id)
    build.weapon.remove(weapon)
    db.session.add(build)
    db.session.commit()
    return redirect(url_for('main.build_detail', build_id=build.id))

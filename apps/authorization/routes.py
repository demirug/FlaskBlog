import datetime

from flask import redirect, request, url_for, render_template, flash, current_app, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash

from application import db
from apps.authorization import authorization as app, User
from apps.authorization.forms import LoginForm, RegisterForm, ChangePasswordForm, ResetForm, ResetConfirmForm
from services.mail import send_template_email
from services.tokens import generate_token


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(request.args.get("next") or url_for(current_app.config.get('INDEX_VIEW')))

    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user()

        user.last_login = datetime.datetime.utcnow()

        db.session.add(user)
        db.session.commit()
        login_user(user, form.remember_me.data)
        return redirect(request.args.get("next") or url_for(current_app.config.get('INDEX_VIEW')))
    return render_template('authorization/login.html', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("blog.list"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            psw_hash=generate_password_hash(form.password.data)
        )

        db.session.add(user)
        db.session.commit()

        _token = generate_token(f"{user.id}{user.email}", user.username, 10)

        send_template_email(
            user.email,
            "Confirm email",
            "authorization/email/confirm.html",
            user=user,
            url=request.url_root[:-1] + url_for('.validate', username=user.username, token=_token))

        flash("Your registered success. Please confirm your email and login")
        return redirect(url_for('.login'))
    return render_template('authorization/register.html', form=form)


@app.route('/validate/<string:username>/<string:token>')
def validate(username, token):
    user: User = User.query.filter_by(username=username).first()
    if user is not None:
        _token = generate_token(f"{user.id}{user.email}", user.username, 10)

        if _token == token:
            user.is_active = True
            db.session.add(user)
            db.session.commit()

            flash("Your email confirmed. Please login")
            return redirect(url_for('.login'))

    abort(404)


@app.route('/changepassword', methods=['POST', 'GET'])
@login_required
def change_password():
    user: User = current_user
    form = ChangePasswordForm(user)
    if form.validate_on_submit():

        user.psw_hash = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()

        logout_user()
        flash("Your password changed. Please login")

        return redirect(url_for('.login'))
    return render_template('authorization/changepassword.html', form=form,  breadcrumbs=[('Home', '/'), ('Profile', url_for('.profile')), ('Change password',)])


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for(current_app.config.get('INDEX_VIEW')))


@app.route('/reset', methods=['POST', 'GET'])
def reset():
    if current_user.is_authenticated:
        return redirect(url_for(current_app.config.get('INDEX_VIEW')))

    form = ResetForm()

    if form.validate_on_submit():

        target: User = User.query.filter_by(username=form.username.data, is_active=True).first()

        if target:

            _token = generate_token(f"{target.id}{target.email}{target.last_login}", target.username, 10)

            send_template_email(target.email, 'Password reset', 'authorization/email/reset.html', user=target,
                                url=request.url_root[:-1] + url_for('.reset_confirm', username=target.username, token=_token))

        flash('Reset email sent to your email')
        return redirect(url_for('.login'))

    return render_template('authorization/reset.html', form=form, breadcrumbs=[('Home', '/'), ('Login', url_for('.login')), ('Reset',)])


@app.route('/reset-confirm/<string:username>/<string:token>', methods=['POST', 'GET'])
def reset_confirm(username, token):
    if current_user.is_authenticated:
        return redirect(url_for(current_app.config.get('INDEX_VIEW')))

    target: User = User.query.filter_by(username=username, is_active=True).first()

    if target:
        _token = generate_token(f"{target.id}{target.email}{target.last_login}", target.username, 10)
        if _token == token:
            form = ResetConfirmForm()
            if form.validate_on_submit():
                target.psw_hash = generate_password_hash(form.password.data)
                target.last_login = datetime.datetime.utcnow()

                db.session.add(target)
                db.session.commit()

                login_user(target)

                flash('Account password changed')

                return redirect(url_for('.profile'))

            return render_template('authorization/reset.html', form=form, breadcrumbs=[('Home', '/'), ('Login', url_for('.login')), ('Reset',)])

    abort(404)


@app.route('/profile')
@login_required
def profile():
    return render_template('authorization/profile.html', object=current_user, breadcrumbs=[('Home', '/'), ('Profile',)])

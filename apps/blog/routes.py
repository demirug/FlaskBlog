from flask import request, render_template, abort, redirect, url_for, flash
from flask_login import login_required, current_user

from application import db
from apps.blog import Blog, blog as app
from apps.blog.forms import BlogForm


@app.route('/')
def list():
    paginator = Blog.query.paginate(per_page=5, error_out=False)
    page = request.args.get('page', 1, int)
    if page > paginator.pages:
        return redirect(request.base_url)
    paginator.page = page
    return render_template('blog/list.html', page_obj=paginator, display_more_pages=2)


@app.route('/view/<string:slug>')
def detail(slug):
    blog = Blog.query.filter_by(slug=slug).first()
    if blog is None:
        abort(404)
    return render_template('blog/detail.html', object=blog)


@app.route("/add", methods=['POST', 'GET'])
@login_required
def add_blog():
    form = BlogForm()

    if form.validate_on_submit():
        blog: Blog = form.save()
        db.session.add(blog)
        db.session.commit()
        return redirect(blog.get_absolute_url())

    return render_template('blog/create.html', form=form)


@app.route("/edit/<string:slug>", methods=['POST', 'GET'])
@login_required
def edit_blog(slug):
    blog: Blog = Blog.query.filter_by(slug=slug).first()

    if blog is None:
        abort(404)

    if blog.author_id != current_user.id:
        abort(403)

    form = BlogForm(instance=blog)

    if form.validate_on_submit():
        blog = form.save()
        db.session.add(blog)
        db.session.commit()

        return redirect(blog.get_absolute_url())
    return render_template('blog/edit.html', object=blog, form=form)


@app.route('/delete/<string:slug>')
@login_required
def delete_blog(slug):
    blog: Blog = Blog.query.filter_by(slug=slug, author_id=current_user.id).first()
    if blog is None:
        abort(404)

    db.session.delete(blog)
    db.session.commit()

    flash(f"Blog {blog.title} has been deleted")

    return redirect(url_for(".list"))

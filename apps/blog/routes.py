from flask import request, render_template, abort, redirect, url_for, flash
from flask_login import login_required, current_user

from application import db
from apps.authorization import User
from apps.blog import Blog, blog as app, Comment
from apps.blog.forms import BlogForm, CommentForm


@app.route('/')
def list():
    paginator = Blog.query.paginate(per_page=5, error_out=False)
    page = request.args.get('page', 1, int)
    if page > paginator.pages:
        return redirect(request.base_url)
    paginator.page = page
    return render_template('blog/list.html', page_obj=paginator, display_more_pages=2)


@app.route('/view/<string:slug>', methods=['POST', 'GET'])
def detail(slug):
    blog = Blog.query.filter_by(slug=slug).first()
    if blog is None:
        abort(404)

    form = None

    # Adding comments to blog
    if current_user.is_authenticated:
        # Check for comment per user limit
        if Comment.query.filter_by(blog_id=blog.id, author_id=current_user.id).count() < 3:

            form = CommentForm()
            if form.validate_on_submit():
                comment = Comment(text=form.text.data, blog_id=blog.id, author_id=current_user.id)

                db.session.add(comment)
                db.session.commit()
                flash("You comment sent")

                return redirect(blog.get_absolute_url())

    comments = db.session.query(Comment.text, Comment.date, User.username).join(User, Comment.blog_id == blog.id and User.id == Comment.author_id)

    return render_template('blog/detail.html', object=blog, form=form,
                           comments=comments,
                           breadcrumbs=[("Main", '/'), (blog.title,)]
                           )


@app.route("/add", methods=['POST', 'GET'])
@login_required
def add_blog():
    form = BlogForm()

    if form.validate_on_submit():
        blog: Blog = form.save()
        blog.author_id = current_user.id

        db.session.add(blog)
        db.session.commit()

        flash(f"Blog {blog.title} created")

        return redirect(blog.get_absolute_url())

    return render_template('blog/create.html', form=form,
                           breadcrumbs=[("Main", '/'), ("Add blog",)])


@app.route("/edit/<string:slug>", methods=['POST', 'GET'])
@login_required
def edit_blog(slug):
    blog: Blog = Blog.query.filter_by(slug=slug, author_id=current_user.id).first()
    if blog is None:
        abort(404)

    form = BlogForm(instance=blog)

    if form.validate_on_submit():
        blog = form.save()
        db.session.add(blog)
        db.session.commit()

        flash(f"Blog {blog.title} updated")

        return redirect(blog.get_absolute_url())
    return render_template('blog/edit.html', object=blog, form=form,
                           breadcrumbs=[("Main", '/'), (f"Edit blog `{blog.title}`",)])


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

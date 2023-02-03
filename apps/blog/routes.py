from flask import request, render_template, abort
from apps.blog import Blog, blog as app


@app.route('/')
def list():
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.paginate(page=page, per_page=5)
    return render_template('blog/list.html', blogs=blogs)


@app.route('/<string:slug>')
def detail(slug):
    blog = Blog.query.filter_by(slug=slug).first()
    if blog is None:
        abort(404)
    return render_template('blog/detail.html', object=blog)


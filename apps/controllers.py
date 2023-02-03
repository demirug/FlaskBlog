
def register_blueprints(app):
    from apps.authorization import authorization
    app.register_blueprint(authorization, url_prefix="")

    from apps.blog import blog
    app.register_blueprint(blog, url_prefix="")
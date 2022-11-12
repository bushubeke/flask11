import os
from flask_admin import Admin
from flask_openapi3 import Info, Tag,OpenAPI
from flask_admin.contrib.sqla import ModelView
from main.db import db
from flask_openapi3 import HTTPBearer
from user.approutes import auth
from store.approutes import store_app
from user.admin import UserAdmin,RoleAdmin,ContentTypesAdmin
from user.models import User,Role,ContentTypes
from config import settings

def create_dev_app():

    info = Info(title="Flask OpenAPI", version="1.0.0")
    security_schemes = {"APP-Token": HTTPBearer(bearerFormat="JWT")}
    app = OpenAPI(__name__, info=info,security_schemes=security_schemes)
    app.config.update(**dict(settings))
    app.app_context().push()
    db.init_app(app)
    app.register_api(auth)
    app.register_api(store_app)
    admin=Admin(app,template_mode='bootstrap4')
    @app.get("/")
    def index():
        return {"Message":"There is no index page Please make one yourself"}
        
    admin.add_view(UserAdmin(User,db.session))
    admin.add_view(RoleAdmin(Role,db.session))
    admin.add_view(ContentTypesAdmin(ContentTypes,db.session))
  
    return app

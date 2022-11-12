
import jwt
from typing import Any
from datetime import datetime,timedelta
from flask import current_app
from flask_openapi3 import APIBlueprint
from flask_openapi3.openapi import json as JSONResponse
from passlib.hash import pbkdf2_sha512
from sqlalchemy import select,update,delete
from sqlalchemy.orm import joinedload
from flask_sqlalchemy import Pagination
from main.db import db
from user.utils import *
from user.models import User,Role
from user.serializers import *
from config import settings
from status import status


#  make_response(jsonify(d), 200)
###########################################################
auth = APIBlueprint('auth', __name__, url_prefix='/auth')
##########################################################


@auth.post("/user",responses={"200": UserModelAll})
def add_new_user(user : UserModel):
    data=dict(user)
    data['uid']=str(uuid.uuid4())
    
    return dict(UserModelAll.from_orm(User(**data))),status.HTTP_200_OK

@auth.get('/user/<int:user_id>',responses={"200": UserModelAll})
def get_one_user(path : UserPathSerilizer):
	try:
		user=db.session.execute(select(User).where(User.id==path.user_id).options(joinedload(User.roles)))
		user=user.unique().scalars().first()
		user=UserModelAll.from_orm(user)
		return {'user' : user.dict()},status.HTTP_200_OK
	except Exception as e:
		return {"Message" : str(e)}
	finally:
		db.session.close()
@auth.get('/user/<int:page>/<int:size>')
def get_all_user( path : PageSerilizer): 
	try:
		users=db.paginate(select(User).options(joinedload(User.roles)).order_by(User.id),page=path.page,per_page=path.size)
		current_page,total_pages=users.page,users.pages
		users=list(users)
		users=[UserModelAll.from_orm(user).dict() for user in users]
		return {"page" : current_page, 'total_pages':total_pages, 'users' : users },status.HTTP_200_OK
	except Exception as e:
		print(e)
		return {"Message" : str(e)},status.HTTP_404_NOT_FOUND
	finally:
		db.session.close()
@auth.get('/role/<int:role_id>')
def get_one_role(role_id : int):
	try:
		role=db.session.execute(select(Role).where(Role.id==role_id).options(joinedload(Role.users)))
		return RoleModelAll.from_orm(role.unique().scalars().first())
	except Exception as e:
		JSONResponse({"Message" : str(e)}),status.HTTP_500_INTERNAL_SERVER_ERROR
	finally:
		db.session.close()
		
@auth.get('/role')
def get_some_role(): 
	try:
		roles=db.session.execute(select(Role).options(joinedload(Role.users)).order_by(Role.id))
		roles=roles.unique().scalars().all()
		resp=[dict(RoleModel.from_orm(role)) for role in roles]
		return {"Page" : 1, "roles" : resp},status.HTTP_200_OK
	except Exception as e:
		return {"Message" : str(e)},status.HTTP_500_INTERNAL_SERVER_ERROR
	finally:
		db.session.close()
@auth.post("/login")
def login_user():
    # logdata=dict(login_data)
    try:
            return {"access_token": "something", "token_type": "bearer"}
            # if logdata['grant_type'] =='authorization_code':
            #     user=db.session.execute(select(User).filter_by(username=logdata['username']).options(joinedload(User.roles)))
            #     user=user.unique().scalars().first()
            #     data=dict(UserModelAll.from_orm(user))
            #     #handling data for nested pydantic and datacalss objects
            #     data=dataclass_to_dic(data)
            #     data=uuid_to_str(data)
            #     if  pbkdf2_sha512.verify(logdata['password'],data["password"]):                        
            #         exp=datetime.utcnow()+timedelta(hours=settings.JWT_APP_TOKEN_EXPIRE_TIME)
            #         exp2=datetime.utcnow()+timedelta(hours=settings.JWT_REFRESH_TOKEN_EXPIRE_TIME)
            #         key=settings.SECRET_KEY 
            #         del data["password"]
            #         del data["date_registerd"]
            #         token=jwt.encode({"data":data,"exp":exp,},key,algorithm="HS256")
            #         reftoken=jwt.encode({'data':data,'exp':exp2},key,algorithm="HS256")
            #         return JSONResponse({"access_token": token,"refresh_token":reftoken, "token_type": "bearer"},status_code=status.HTTP_202_ACCEPTED)
            #     return JSONResponse({"Message":"Invalid Password"},status_code=status.HTTP_401_UNAUTHORIZED)
            # elif logdata['grant_type'] == "refresh_token":
            #         exp=datetime.utcnow()+timedelta(hours=4)
            #         exp2=datetime.utcnow()+timedelta(hours=5)
            #         key=settings.SECRET_KEY
            #         data=jwt.decode(logdata['token'],key,algorithms="HS256")
            #         data=data["data"]
            #         token=jwt.encode({'data':data,'exp':exp},key,algorithm="HS256")
            #         reftoken=jwt.encode({'data':data,'exp':exp2},key,algorithm="HS256")
            #         return JSONResponse({"access_token": token,"refresh_token":reftoken, "token_type": "bearer"},status_code=status.HTTP_202_ACCEPTED)
            # elif logdata['grant_type'] == "token_decode":
            #         key=settings.SECRET_KEY
            #         data=jwt.decode(logdata['token'],key,algorithms="HS256")
            #         return JSONResponse(data["data"],status_code=status.HTTP_206_PARTIAL_CONTENT)
            # else:
            #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    except Exception as e:
            db.session.rollback()
            return JSONResponse({"detail":"Message: Something Unexpected Happended"},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
            db.session.close()

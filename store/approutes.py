import jwt
from datetime import datetime,timedelta
from typing import List
from flask import jsonify as JSONResponse,request as Request
from status import status
from flask_openapi3 import APIBlueprint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update,delete,text
from sqlalchemy.orm import selectinload,joinedload
from main.db import db
from main.roleadmin import check_user_role
from store.models import Customer,Address,Order,OrderItem,Promotion,Product,ProductPromotion,\
        Cart,CartItem,Review
from store.serializers import ProductModel,ProductPromotionModel,PromotionModel,\
    ReviewModel,OrderModel,OrderItemMOdel,CartModel,CartItemModel,\
        CustomerModel,AddressModel,OrderModelAll,ProductModelAll
from user.models import ContentTypes
from user.serializers import ContentTypesModel

store_app=APIBlueprint('store', __name__, url_prefix='/store')

@store_app.get("/order" )
async def get_order():
    try: 
        orders=Order.query.order_by(Order.id).all()
    
        print(orders)
        return orders
    except Exception as e:
         return JSONResponse({'Message':str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        db.session.close()

# @store_app.get("/order/{order_id:int}")
# async def get_order(request:Request,order_id : int,session : Session):
#     try: 
#         order=await session.execute(select(Order).where(Order.id==order_id))
#         order=order.unique().scalars().first()
#         return OrderModelAll.from_orm(order)
#     except Exception as e:
#          return JSONResponse({'Message':str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     finally:
#         await session.close()

# @store_app.get("/product")
# async def get_order(request:Request,session : Session):
#     try: 
#         products=await session.scalars(select(Product).options(selectinload(Product.orders)).order_by(Product.id))
#         products=products.all()
#         return paginate(products)
#     except Exception as e:
#          return JSONResponse({'Message':str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     finally:
#         await session.close()

# @store_app.get("/product/{product_id:int}")
# async def get_order(request:Request,product_id : int,session : Session):
#     try: 
#         product=await session.execute(select(Product).where(Product.id==product_id))
#         product=product.unique().scalars().first()
#         return ProductModelAll.from_orm(product)
#     except Exception as e:
#          return JSONResponse({'Message':str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     finally:
#         await session.close()


# @store_app.get("/test")
# async def get_order(request:Request,session : Session):
#     try: 
#         await check_user_role(['superuser'],'store_order')
#         return JSONResponse({"Message":"Working Fine"},status_code=status.HTTP_200_OK)
#     except Exception as e:
#          return JSONResponse({'Message':str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     finally:
#         await session.close()

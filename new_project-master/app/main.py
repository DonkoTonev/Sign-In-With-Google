from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError
from .config import CLIENT_ID, CLIENT_SECRET
from fastapi.staticfiles import StaticFiles
from .db import users_collection, user_schema, CustomJSONEncoder
# from pymongo import MongoClient
from datetime import datetime
from bson.json_util import dumps


# app = FastAPI()
app = FastAPI(json_encoder=CustomJSONEncoder)
app.add_middleware(SessionMiddleware,
                   secret_key='wefuinruiof4hniofnrijhnkjnwkj')
app.mount("/static", StaticFiles(directory="static"), name="static")

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_url': 'http://localhost:8000/auth'
    }
)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    user = request.session.get('user')
    if user:
        return RedirectResponse('welcome')

    return templates.TemplateResponse(
        name="home.html",
        context={"request": request}
    )


@app.get('/welcome')
def welcome(request: Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse('/')

    return templates.TemplateResponse(
        name='welcome.html',
        context={'request': request, 'user': user}
    )



@app.get("/login")
async def login(request: Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)


# @app.get('/auth')
# async def auth(request: Request):
#     try:
#         token = await oauth.google.authorize_access_token(request)
#     except OAuthError as e:
#         return templates.TemplateResponse(
#             name='error.html',
#             context={'request': request, 'error': e.error}
#         )
#     user = token.get('userinfo')
#     if user:
#         request.session['user'] = dict(user)
#     return RedirectResponse('welcome')

@app.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return templates.TemplateResponse(
            name='error.html',
            context={'request': request, 'error': e.error}
        )

    user_info = token.get('userinfo')
    if user_info:
        # Check if the user already exists in the database
        existing_user = users_collection.find_one({"userId": user_info["sub"]})

        if existing_user:
            user_data = existing_user
        else:
            # User doesn't exist, create a new user record
            user_data = {
                "userId": user_info["sub"],
                "name": user_info["name"],
                "email": user_info["email"],
                "createdAt": str(datetime.now())
            }
            users_collection.insert_one(user_data)

        # Convert ObjectId to string before storing in the session
        user_data["_id"] = str(user_data["_id"])
        request.session['user'] = user_data
    return RedirectResponse('welcome')

@app.get('/logout')
def logout(request: Request):
    request.session.pop('user')
    return RedirectResponse('/')

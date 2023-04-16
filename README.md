**Simple chat**

# Installation

```sh
git clone https://github.com/ye11ow-banana/SimpleChat.git
```

Install dependencies to your virtual environment
```sh
pip install -r requirements.txt
```

Set environment variables to .env file
```sh
SECRET_KEY=
```

Run Django
```sh
python3 loaddata data.json
```
```sh
python3 manage.py migrate
```
```sh
python3 manage.py runserver
```

---

## API (urls)

Get Access token
```sh
data: {"username": "admin", "password": "admin"}
```
```sh
POST http://127.0.0.1:8000/auth/jwt/create/
```

In every request headers:
```sh
Authorization: Bearer <ACCESS_TOKEN>
```

### Tasks

Creation (if a thread with particular users exists - just return it.);
```sh
Example data: {"participants": [1, 2]}
```
```sh
POST http://127.0.0.1:8000/api/v1/chats/thread/create/
```

removing a thread;
```sh
DELETE http://127.0.0.1:8000/api/v1/chats/thread/<thread_id>/destroy/
```

retrieving the list of threads for any user;
```sh
GET http://127.0.0.1:8000/api/v1/chats/thread/list/
```

creation of a message;
```sh
Example data: {"text": "Some text from JWT token"}
```
```sh
POST http://127.0.0.1:8000/api/v1/chats/thread/<thread_id>/message/create/
```

retrieving message list for the thread;
```sh
GET http://127.0.0.1:8000/api/v1/chats/thread/<thread_id>/message/list/
```

marking the message as read;
```sh
PATCH http://127.0.0.1:8000/api/v1/chats/message/<message_id>/read/
```

retrieving a number of unread messages for the user.
```sh
GET http://127.0.0.1:8000/api/v1/chats/message/number-unread/
```
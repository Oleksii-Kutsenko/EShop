# E-shop
Simple shop test project. Shop sells places from the stock.

## Installation

- Clone the repository

```
git clone https://github.com/fronimus/E-Shop.git
cd E-Shop
```

- Create virtual environment and activate it

```
python -m venv venv
source venv/bin/activate
```

- Install dependencies

Microsoft Visual C++ 14.0 or greater is required. - https://visualstudio.microsoft.com/visual-cpp-build-tools/

```
pip install -r requirements.txt
``` 
- Set up environment and database
    1. Create sqlite db ```touch db.sqlite3```(linux) or ```New-Item db.sqlite3```(windows) 
    2. Open ```.env``` file and set secret ([how to do this ](https://stackoverflow.com/questions/34902378/where-do-i-get-a-secret-key-for-flask/34903502))
    3. Set URI for your db, for example (sqlite:////home/user/E-Shop/db.sqlite3)
    4. Export env vars ```. .env```
    5. Create migrations ```python -m flask db init ``` then ```python -m flask db migrate```
    5. Upgrade db ```python -m flask db upgrade```

- Register admin
    1. ```python -m flask shell```
    2. In shell
```python
from app.models import User
admin = User(username='myusername', is_admin=True)
admin.set_password('mypassword')
from app import db
db.session.add(admin)
db.session.commit()
```
- Run your app
```python -m flask run```


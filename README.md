# Test blog

## For start
Create virtualenv:
```commandline
virtualenv -p /path/to/your/python3/ env
```

Activate it:
```commandline
source env/bin/activate
```

Install requirements:
```commandline
pip install -r requirements.txt
```

Init and apply migrations to db:
```commandline
python myblog/manage.py migrate
```

And you already may run server:
```commandline
python myblog/manage.py runserver
```

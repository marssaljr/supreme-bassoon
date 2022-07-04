DATABASE=test coverage run --omit="*/venv/*,*/migrations/*,*/templatetags/*,manage.py,*/config/*" --source="." manage.py test && coverage html

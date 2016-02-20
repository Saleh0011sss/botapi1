
# How to Launc the application
$ python -m virtualenv env
Run application
$ env/bin/python app.py

# Install packages on azure
$ env/bin/pip install pymongo
$ env/bin/pip freeze > requirements.txt (to update the requirements)
if [ ! -d "/env" ]; then
    python -m virtualenv env # create the enviroment directory
fi

# Place your dependencies here
env/bin/pip install bottle
env/bin/pip install pymongo
env/bin/pip install pyTelegramBotAPI
env/bin/pip install logging

# Update the azure requirements folder after installing
env/bin/pip freeze > requirements.txt
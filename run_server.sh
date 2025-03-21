#!/bin/bash

# Create virtualenv (django_venv)
python3 -m venv django_venv
# Activate virtual environment
source django_venv/bin/activate
# Upgrade pip
pip install --upgrade pip
# Install using requirement.txt
pip install -r requirement.txt
# Virtual environment remains activated after installation
echo "Virtualenv django_venv is activated."
# cd to project directory
cd myproject
# db migration
python manage.py makemigrations
python manage.py migrate
# run server
python manage.py runserver
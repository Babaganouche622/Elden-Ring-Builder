import os
import unittest
import app

from datetime import date
from elden_ring_builder.extensions import app, db, bcrypt
from elden_ring_builder.models import Build, Weapon, User
"""
Run these tests with the command:
python -m unittest elden_ring_builder.main.tests
"""

#################################################
# Setup
#################################################

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

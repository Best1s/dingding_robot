"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import dingding_robot.views
import dingding_robot.config

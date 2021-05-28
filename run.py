#!/usr/bin/env python3
"""
run.py - Flask_Blog - adapted from Corey M Schafer's code found at:
        https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog/13-Deployment-Linode

Edit config.json to modify settings for flask

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""

from flaskblog import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

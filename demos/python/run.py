# -*- coding: utf-8 -*-
from app import create_app
from app.api import init_api

app = create_app()
init_api(app)


if __name__ == '__main__':
    app.run()

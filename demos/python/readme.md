# 目录结构
```
app 
    api                      api interface
    model                    database ORM
    static                   static file
    templates                template
    views                    view           
configuration                project configuration
cryptopay_sdk                signature sdk
requirements                 dependence
manage.py                    database initialization
run.py                       Application entrance
```


Development environment:
1. Install the virtual environment, switch to the root directory to execute: virtualenv venv
2. Enter the virtual environment: . venv/bin/activate
4. Installation dependence: pip install -r requirements/development.txt
6. Go to configurateion directory,config environment。
7. Enter manage.py into the database initialization, if the model has new, press the command and new。


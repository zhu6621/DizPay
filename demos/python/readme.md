# 目录结构
```
app 
    api                      api接口
    model                    数据库ORM
    static                   静态文件
    templates                前端模板
    views                    前端页面渲染           
configuration                项目配置
cryptopay_sdk                签名算法封装
requirements                 依赖
manage.py                    数据库初始化
run.py                       应用入口
```


开发环境:
1. 安装虚拟环境, 切换到根目录执行: virtualenv venv
2. 进入虚拟环境: . venv/bin/activate
4. 安装依赖: pip install -r requirements/development.txt
5. 生成依赖: pip freeze > requirements/development.txt
6. 进入configuration 进行项目配置，包括本地数据配置，app_id, app_key配置，支付网关接口环境配置。
7. 进入manage.py进数据库初始化，如果model有跟新，按命令跟新。

约定:
1. 日期时间都采用 UTC 标准
2. 接口处的日期时间采用时间戳
3. 钱相关的严禁使用浮点数

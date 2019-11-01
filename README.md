# myblog
基于flask和bootstrap的个人博客
## 部署
使用 nginx做反向代理，gunicorn作为wsgi server ，部署在搬瓦工服务器
## 访问地址
http://95.181.189.87
## 使用方法
- 首先建立一个.flaskenv的文件，定义
```bash
FLASK_APP=myblog
FLASK_ENV=development
# mysql 数据库的用户
BLOG_DB_USERNAME=xxx
# mysql数据库的密码
BLOG_DB_PASSWORD=xxx

```

调试时 也可以使用sqlite数据库， create_app 的时候选择development的配置

- 初始化数据库

```
flask initdb
# 生成虚拟数据，也可以跳过这一步
flask forge
# 设置管理员用户名和密码
flask setamdin
```

- 运行程序
```
flask run
```

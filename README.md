# Qiniu-ufop

本项目提供一个高效便捷的**七牛自定义数据处理**脚手架,以便开发人员专注数据处理业务逻辑.

## Quickstart
### 安装
通过pip安装项目

    pip install qiniu-ufop

### 开始项目
使用qiniu-ufop命令,快速生成项目

    qiniu-ufop createproject

通过createproject命令,qiniu-ufop在当前目录下生成了一个app.py文件.

### 编写业务代码
以下是一个简单示例:

    # app.py

    from qiniu_ufop import QiniuUFOP

    ufop = QiniuUFOP()

    @ufop.task(route=r"^(?:/(?P<name>\w+))?$")
    def debug(buffer, args, content_type):
        return "hello " + args.get("name", "world")

假设该自定义数据处理名称为*qiniu*,待处理的文件链接为*https://qbox.me/example.jpg*. 则调用链接是*https://qbox.me/example.jpg?qiniu/qq*,响应输出为*hello qq*

### 本地运行项目

    qiniu-ufop runserver --debug
    qiniu-ufop runworker

> 注意: 在windows下开发需额外安装`eventlet`,运行runworker时使用命令`qiniu-ufop runworker -P eventlet`

### 生成Dockerfile并发布

    qiniu-ufop createdockerfile > Dockerfile

## 使用
### 部署
### 配置

## 开发
数据处理器实际上是一个[celery任务](http://docs.celeryproject.org/en/latest/userguide/tasks.html),这个任务必须接受一个`route`参数,指明会路由到该处理器的cmd,如果全局只有一个处理器,可以使用`.*`或`^$`作为路由.

被装饰的处理起接受三个参数,第一个是待处理文件的`io.BytesIO`,第二个是路由匹配到的相关参数,第三个是文件的Content-Type.

处理器返回字符串,bytes,json或是一个`qiniu_ufop.Response`对象.

## 调试
### 本地调试处理程序
可通过qiniu-ufop对处理程序进行调试

    qiniu-ufop proccess [<cmd>] <filename>

> 注意:此处的cmd是不包括处理程序名的

命令的结果将直接打印再控制台上,如需持久化,可将输出流导向某个文件,例如

    qiniu-ufop proccess test.png > output.png

### 本地调试webserver
启动服务器及worker

    qiniu-ufop runserver --debug
    qiniu-ufop runworker

访问
> POST http://localhost:9100/handler?cmd=\<cmd\>&url=\<url\>

### 本地调试Docker

## 设计说明

## TODOS:
* 异常处理
* 重构manage
* 单元测试

## Changelog


Xavier-Lam@NetDragon

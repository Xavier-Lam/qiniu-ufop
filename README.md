# Qiniu-ufop

[![PyPI](https://img.shields.io/pypi/v/qiniu-ufop.svg)](https://pypi.org/project/qiniu-ufop)

本项目提供一个便捷高性能的**七牛自定义数据处理**脚手架,以便开发人员专注数据处理业务逻辑.

目前尚未编写单元测试,也没有完善的异常处理机制.采用Python 3.6进行开发,不确保其他版本运行正常.

项目官方站点 https://github.com/Xavier-Lam/qiniu-ufop

- [Quickstart](#Quickstart)
  - [安装](#安装)
  - [开始项目](#开始项目)
  - [编写业务代码](#编写业务代码)
  - [本地运行项目](#本地运行项目)
  - [生成Dockerfile并发布](#生成Dockerfile并发布)
  - [激活](#激活)
  - [注意](#注意)
- [开发](#开发)
- [使用](#使用)
  - [命令行工具](#命令行工具)
  - [一键部署](#一键部署)
  - [手工部署](#手工部署)
    - [生成镜像](#生成镜像)
    - [上载自定义处理程序](#上载自定义处理程序)
    - [配置](#配置)
- [调试](#调试)
  - [本地调试处理程序](#本地调试处理程序)
  - [本地调试webserver](#本地调试webserver)
  - [本地调试Docker](#本地调试Docker)
- [问题排查](#问题排查)
  - [日志查看](#日志查看)
  - [部署过程中遇到的异常](#部署过程中遇到的异常)
- [Cookbook](#Cookbook)
  - [使用git更新代码](#使用git更新代码)
- [TODOS:](#TODOS)

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

编写说明参见[开发](#开发) 章节

### 本地运行项目

    qiniu-ufop runserver --debug
    qiniu-ufop runworker

> 注意: 在windows下开发需额外安装`eventlet`,运行runworker时使用命令`qiniu-ufop runworker -P eventlet`

详见[调试](#调试)章节

### 生成Dockerfile并发布

    qiniu-ufop deploy -t <image-tag> -n <ufop-name> -v <version>

该命令为一键部署命令,一键部署需满足相关条件,请参阅[一键部署](#一键部署)章节.如需定制化部署,可参见[手工部署](#手工部署)章节

### 激活
在你的自定义处理的[版本列表](https://portal.qiniu.com/dora/ufopv2//index?region=all)中调整实例数,即可使用

### 注意
七牛有一个BUG,在代码中没办法取到正确的cpu核数
* 使用一键部署,框架会取一键部署的配置项flavor(实例类型,默认C1M1)作为CPU核数,开启相应数量的worker及web
* 自行部署时,请务必在环境变量(开发路径下的.env文件)中写入CPU核数`CPU_COUNT`或实例配置`FLAVOR`,才能开启正确数量的worker及web,否则,qiniu-ufop将默认取单核,也就是单实例运行web及worker

## 开发
数据处理器实际上是一个[celery任务](http://docs.celeryproject.org/en/latest/userguide/tasks.html),这个任务必须接受一个`route`参数,指明会路由到该处理器的cmd,如果全局只有一个处理器,可以使用`.*`或`^$`作为路由.理论上可以使用celery复杂的任务分发.

被装饰的处理起接受三个参数,第一个是待处理文件的`io.BytesIO`,第二个是路由匹配到的参数字典,第三个是文件的Content-Type.

处理器返回字符串,bytes,json或是一个`qiniu_ufop.Response`对象.

日志可直接输出stderr.

## 使用
### 命令行工具
可通过

    qiniu-ufop -h

看到详细说明

### 一键部署
一键部署假设用户
* 本地安装有docker环境
* 已安装并登陆qdoractl,qdoractl在PATH中
* 已注册自定义处理程序

        qiniu-ufop deploy -t <image-tag> -n <ufop-name> -v <version>

### 手工部署
[官方文档](https://developer.qiniu.com/dora/manual/1224/quick-start)

此章节假定用户已完成自定义数据处理程序的开发,本地安装有docker环境,并处在自定义处理程序目录下

#### 生成镜像
* 构建docker镜像

        docker build . -t <tag>

#### 上载自定义处理程序
* 下载[自定义数据处理命令行工具](https://developer.qiniu.com/dora/tools/1222/qdoractl)
* 使用accesskey及secretkey登陆
  
        qdoractl login -u <access key>
* 如果你尚未创建你的自定义处理程序,请创建

        qdoractl register <ufop> [-d <description>]
* 上载自定义处理程序

        qdoractl push <tag>

#### 配置
**[官方文档](https://developer.qiniu.com/dora/manual/1225/platform-user-guide)** **[自定义数据处理后台](https://`portal.qiniu.com/dora/ufopv2//index?region=all)**

其他依照官方文档配置,在高级配置中
* 健康配置Path请填写`/health`
* 日志路径添加
  * 任务处理异常日志 `/var/log/worker/`
  * web处理异常日志 `/var/log/server/`
  * supervisor日志 `/var/log/supervisor/`

## 调试
### 本地调试处理程序
可通过qiniu-ufop对处理程序进行调试

    qiniu-ufop process [<cmd>] <filename>

> 注意:此处的cmd是不包括处理程序名的

命令的结果将直接打印再控制台上,如需持久化,可使用output参数,例如

    qiniu-ufop process test.png -o output.png

### 本地调试webserver
启动服务器及worker

    qiniu-ufop runserver --debug
    qiniu-ufop runworker

访问
> POST http://localhost:9100/handler?cmd=\<cmd\>&url=\<url\>

或将文件作为body,POST到
> POST http://localhost:9100/handler?cmd=\<cmd\>

> 注意: 不是使用multipart/formdata进行文件上传

> 注意: 在windows下开发需额外安装`eventlet`,运行runworker时使用命令`qiniu-ufop runworker -P eventlet`
> 
> 否则会报`ValueError: not enough values to unpack (expected 3, got 0)`

### 本地调试Docker
在项目目录下

    qiniu-ufop dockerfile > Dockerfile
    docker pull ubuntu:18.04
    docker build . -t <tag>
    docker run --name <name> -p 9100:9100 -t <tag>

访问
> POST http://localhost:9100/handler?cmd=\<cmd\>

> 注意: 在使用virtualbox时 localhost应改为虚拟机ip

## 问题排查
### 日志查看
七牛的日志查看好像经常取不到日志,建议自行在处理程序中埋一个下载日志的方法,来获取日志.可以参看示例项目

### 部署过程中遇到的异常
在运行qdoractl push时,可能会遇到该异常,反正我是遇到了

    Get http://192.168.99.100:2376/v1.20/version: net/http: HTTP/1.x transport connection broken: malformed HTTP response "\x15\x03\x01\x00\x02\x02".

    * Are you trying to connect to a TLS-enabled daemon without TLS?

遇到上述异常,首先登陆docker宿主机

    docker-machine ssh

修改docker配置,设置`DOCKER_TLS=no`

    sudo vi /var/lib/boot2docker/profile

重启docker服务

    sudo /etc/init.d/docker restart

退出docker宿主机

    exit

unset本机环境变量DOCKER_TLS_VERIFY(以windows为例)

    set DOCKER_TLS_VERIFY=

再度执行部署(参见手工部署或一键部署)

## Cookbook
### 使用git更新代码
* 在工作路径下,生成ssh-key

        md .ssh
        ssh-keygen -f ./.ssh/id_rsa -t rsa -N ''

* 将生成的 ./.ssh/id_rsa.pub 加入git仓库的部署密钥中

* 修改Dockerfile,在cmd前加入

        RUN apt-get install git
        ADD ./.ssh /root/.ssh
        RUN chmod 400 /root/.ssh/id_rsa
        RUN ssh-keyscan github.com >> /root/.ssh/known_hosts
        RUN git clone your@repository

* 修改script.sh

        git pull origin master

> 注意: 由于将私钥加入了镜像,任何拿到你的镜像的用户,将可以获取到你的私钥

## TODOS:
* 异常处理
* 单元测试
* 测试异步

> 吐槽一下七牛的工单处理,我提了至少3个bug,要么装傻,要么说对不起,我们有问题,请你使用其他方法...另外文档自定义数据处理这块文档也比较糟糕.

> 有问题可以提issue我问我,star数上50再考虑单元测试吧~

Xavier-Lam@NetDragon

FROM ubuntu:18.04
LABEL maintainer="Xavier-Lam <Lam.Xavier@hotmail.com>"
LABEL description="本文件由qiniu-ufop自动生成,开发者可根据自身需求进行修改"
LABEL poweredby="qiniu-ufop <https://github.com/Xavier-Lam/qiniu-ufop>"

RUN mkdir /data
RUN mkdir -p /var/log

# 安装基本环境
RUN apt-get update
RUN apt-get install -y wget build-essential cmake python-dev python3-pip
RUN apt-get install -y redis-server
RUN pip3 install --upgrade pip
RUN pip3 install supervisor

# TODO: 开发者在此安装其他依赖
# ...

WORKDIR /data

# 安装qiniu-ufop
RUN pip install qiniu-ufop

# 拷贝文件
ADD . /data
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple/
RUN echo_supervisord_conf > /etc/supervisord.conf
RUN sed -i "s|/tmp/supervisord.log|/var/log/supervisor/log|g" /etc/supervisord.conf
ADD supervisor.conf /data/supervisor.conf
RUN cat supervisor.conf >> /etc/supervisord.conf
RUN mkdir -p /var/log/server/ /var/log/supervisor/ /var/log/worker/

# 设置环境变量
ENV C_FORCE_ROOT 1
# TODO: 开发者在此设置其他环境变量
# ...

# 运行
CMD /bin/bash -c "redis-server --save \"\" --appendonly no --daemonize yes && supervisord -n -c /etc/supervisord.conf"
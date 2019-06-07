# 本文件由qiniu-ufop自动生成
# 开发者可根据自身需求进行修改

FROM ubuntu:18.04
MAINTAINER Xavier-Lam <Lam.Xavier@hotmail.com>

RUN mkdir /data
RUN mkdir /var/log

# 安装基本环境
RUN sudo apt-get update
RUN sudo apt-get install -y wget build-essential cmake python-dev python-pip3
RUN sudo apt-get install -y redis-server
RUN sudo pip3 install --upgrade pip
RUN sudo pip3 install supervisor
RUN echo_supervisord_conf > /etc/supervisor.conf

# TODO: 开发者在此安装其他依赖
# ...

# 安装qiniu-ufop
RUN sudo pip install qiniu-ufop

# 拷贝文件
ADD {DIR} /data
ADD {DATADIR}/supervisor.conf /data/supervisor.conf

# 运行
WORKDIR /data
RUN cat supervisor.conf >> /etc/supervisor.conf
RUN sudo pip install -r requirements.txt
CMD source ./.env && redis-server --save "" --appendonly no --daemonize yes && supervisord -n
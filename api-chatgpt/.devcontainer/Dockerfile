# FROM python:3-slim
FROM python:3.9-slim

# ユーザ'vscode'を作成する
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

#RUN mkdir $HOME/.pip
#COPY conf/pip.conf $HOME/.pip/pip.conf

RUN apt-get update \
    && groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && apt-get -y install locales \
    && localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

RUN apt-get -y install curl git

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm
ENV PATH "/home/vscode/.local/bin:$PATH"

RUN apt-get install -y vim less gcc

# 以下 pip
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install openai
RUN pip install -U pylint
#RUN pip install flake8 autopep8
#RUN pip install python-dotenv fastapi uvicorn
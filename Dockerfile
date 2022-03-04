FROM alpine
LABEL AUTHOR="ClegeA <amlhbmcxMjM1NzRAMTYzLmNvbQ==>"
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
    && set -ex && apk update && apk upgrade \
    && apk add --update --no-cache  python3 py3-pip git  \
    && pip install --upgrade pip \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && pip install django \
    && cd / \
    && git clone https://gitee.com/jiang123574/json2srt.git
CMD ["python3","/json2srt/manage.py","runserver","0.0.0.0:8800"]
EXPOSE 8800
FROM debian:stable-slim
RUN set -x; buildDeps='wget locales' \
    && apt-get update \
    && apt-get install -y $buildDeps \
    && mkdir -p /data/XueQG/App \
    && mkdir -p /data/XueQG/Config \
    && cd /data/XueQG \
    && echo "zh_CN.UTF-8 UTF-8" >> /etc/locale.gen \
    && echo "Asia/Shanghai" > /etc/timezone && cp -a /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && locale-gen zh_CN.UTF-8 UTF-8 \
    && wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_88.0.4324.182-1_amd64.deb \
    && dpkg -i google-chrome-stable_88.0.4324.182-1_amd64.deb;apt-get -fy install;google-chrome --version \
    && rm -f google-chrome-stable_88.0.4324.182-1_amd64.deb \
    && apt-get clean
COPY upload /data/XueQG/
ENV LC_ALL=zh_CN.UTF-8
WORKDIR /data/XueQG
ENTRYPOINT ["./XueQG"]

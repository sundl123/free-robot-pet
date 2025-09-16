# free-robot-pet

<!-- omit in toc -->
<div align="center">
<img src="./assets/logo.png" alt="MCP Go Logo">


<strong>A free robot pet which runs on Raspberry Pi</strong>

<br>

<br>

</div>

## Introduction

1. 技术拆解: [喵星工程师：机器猫的制造日志](https://mp.weixin.qq.com/s/prqFh65NJwVt3SWsyr9jog)
2. 视频分享:[【手把手打造机器猫】](https://www.bilibili.com/video/BV1RG411e7cs/?share_source=copy_web&vd_source=981c39eaab5e0c91fb090a05f55c2d4a)

## Install Dependencies

```shell
pip insatll -r robot_pet/requirements.txt
```

If you want to generate new requirements.txt, do the following
```shell
cd robot_pet
pip install pipreqs
pipreqs . --encoding=utf-8 --force
```

## Usage 用法

```shell
# copy the config file template and edit it as you like
cp conf/config.yaml.example  conf/config.yaml

# text mode
python robot_pet --chat-type text

# audio mode
python robot_pet --chat-type audio

# robot car mode
python robot_pet --chat-type car
```

## 欢迎关注我

我是栋梁，欢迎关注我，学习更多AI干货知识

<img src="./assets/wechat.webp" alt="Wechat QR Code">

1. 微信公众号: 栋搞西搞
2. GitHub: https://github.com/sundl123/free-ai-coder
3. B站: https://space.bilibili.com/600455155
4. CSDN博客: https://blog.csdn.net/thomas20
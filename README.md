# csqunfeng，玩不起，放着就死了
不更了，反正龟④了
![1000000237](https://github.com/lswlc33/autoFunBlock/assets/86835895/08fb9b5a-0c52-4f63-b2f6-be95ea2fd787)


# 方块兽代挂


🖊 方块兽邀请链接：[链接](http://s.jqsjgwb.cn/wx/s?_co=3411241&_st=v11FksFriends&_v=v11&_chan=90585)  
💻 没地方挂机? 来试试: [挂机宝](https://www.beishaoidc.cn/aff/RQWPTPZP)  
❤ 赠我宝石: `3411241`

## 支持功能

> 自用脚本，功能仅为满足自身需求

-   自动矿洞加时 （低于 24 小时时,默认关）
-   自动喂养
-   乌龟挂机、监控
-   多开
-   使用 `python` 编写，支持跨平台
-   大逃杀自动投入（定投）、监控、场次记录

## 使用教程

### 1. 手动部署

> 安装 `python3.xx` 和 `request` 等库

-   1. 运行 `登录` 获取 `token` (会自动存入 `data/setting.ini`)
-   2. 运行 需要的脚本

-   手动修改 `data/setting.ini` 开启部分功能

> 在 `linux` 等无 `GUI` 系统可以使用 `screen` 维持进程

## 2. 使用打包好的 exe

-   1. 去 [Release](https://github.com/lswlc33/autoFunBlock/releases/latest) (稳定渠道) 或者 [Action](https://github.com/lswlc33/autoFunBlock/actions) (测试渠道) 下载打包好的 exe 文件
-   2. 运行 需要的脚本

## 模块介绍

## 登录

用于使用 `验证码` 登录方块兽，并往本地写入登录信息

## 乌龟-挂机

用于实现乌龟的信息实时查看

乌龟挂机和自动捡垃圾是基本功能

携带了乌龟自动喂养和矿洞自动加时

**出生平台**

![image](https://github.com/lswlc33/autoFunBlock/assets/86835895/392e325a-ea9b-40b4-a9e7-42689920cce9)


## 大逃杀-监控

实时查看大逃杀当前场次的信息

同时会在 `data/escape.csv` 里面记录场次信息

包括 `期数,时间,击杀房间,上局击杀房间,是否获胜,消耗宝石,获得宝石,我的宝石`

## 大逃杀-定投

自带多种模式的大逃杀定投

目前支持房间模式:

-   随机房间
-   固定房间
-   错开房间

目前支持房间模式:

-   固定宝石
-   指定随机宝石

## 贝壳-倒狗

-   自动获取当前求购和出售列表，当出售最高价低于求购最低价，自动买入卖出，赚取差价
-   自动购入或卖出价格过于离谱（求购价>0.01,出售价低于 0.001）
-   比较合理的交易失败处理

  ![image](https://github.com/lswlc33/autoFunBlock/assets/86835895/cec1a07c-b0b0-49aa-81b9-1cfbce527ed6)  
逆天平台早点倒闭

## 多开教程

-   1. 复制文件夹
-   2. 重复 `使用教程`

## 双端同开教程

该脚本为自用，那我自然是不允许**我**每天充电顶号重新验证码登陆的

使用 抓包工具 如 `黄鸟` 获取 `token` 手动填入配置文件即可实现手机与脚本同开

至于抓包的先决条件，如 root ，虚拟机则不多说了

## 禁止售卖，禁止商用

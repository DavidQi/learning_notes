# 相见恨晚的 asyncio 异步并发模块 [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)

> 一些精心挑选的基于 Python asyncio 框架的模块，以及其他资源的列表。

Python [asyncio](https://docs.python.org/3/library/asyncio.html) 是Python 3.4版本引入的标准库，
为编写单线程并发代码提供基础架构，通过使用协程、套接字和其他资源的 I/O 多路复用，运行网络客户端和服务器，以及其他相关的基元。

Asyncio 并不是一项崭新的技术，然而近些年来，尤其是2016年三月随着 Python 3.4 的一起发布，展现出良好的发展势头。
所以，在 Python 社区中搜寻最新最棒的库包还是有些难度的。如有遗漏，请补充更新或提出宝贵意见。

## 内容提要

* [Web框架](#Web框架)
* [消息队列](#消息队列)
* [数据库](#数据库)
* [网络](#网络)
* [测试](#测试)
* [Loops替代](#Loops替代)
* [杂项](#杂项)
* [文档书籍](#文档书籍)
* [观点议题](#观点议题)
* [本文出处](#本文出处)

***

## Web框架

*web 应用模块.*

* [aiohttp](https://github.com/KeepSafe/aiohttp) - 基于 asyncio 实现 Http 客户/服务  (PEP-3156).
* [sanic](https://github.com/channelcat/sanic) - 基于Python 3.5+ 的异步web 服务器，和Flask一样使用装饰器作为路由，支持Blueprint。非常快。
* [Kyoukai](https://github.com/SunDwarf/Kyoukai) - 基于Python 3.5+ 使用 asyncio 的异步 Web 框架
* [cirrina](https://github.com/neolynx/cirrina) - 另一个基于 aiohttp 的异步 Web 框架。
* [autobahn](https://github.com/crossbario/autobahn-python) - 通过 WebSocket and WAMP 实现客户端 和服务端通讯，支持 Twisted 和 Asyncio, for clients and servers.

  -- 科普：

    * Websocket是HTML5中的一种新协议，实现了浏览器和服务器间的全双工通信，能更好的节省服务器资源和带宽并达到实时通讯，它建立在 TCP 之上，同 HTTP 一样通过 TCP 来传输数据，但是它和 HTTP 最大不同是：
      WebSocket 是一种双向通信协议，在建立连接后，WebSocket 服务器和 Browser/Client Agent 都能主动的向对方发送或接收数据，就像 Socket 一样；
      WebSocket 需要类似 TCP 的客户端和服务器端通过握手连接，连接成功后才能相互通信。

    * WAMP （Web Application Messaging Protocol）是一个开放标准的 WebSocket 子协议， 用以在一个统一协议中提供两种应用程序消息传递模式：远程过程调用和发布/订阅。


## 消息队列

*用消息队列实现应用的模块*

* [aioamqp](https://github.com/Polyconseil/aioamqp) - 用 asyncio 实现 AMQP
* [aiozmq](https://github.com/aio-libs/aiozmq) - 整合了 Asyncio (pep 3156) 和 ZeroMQ
* [crossbar](https://github.com/crossbario/crossbar) - Crossbar.io 是一个针对分布式微服务应用，通过WAMP 实现的应用路由器。有人甚至说是 [Python Web 应用的未来](http://crossbario.com/blog/Is-Crossbar-the-future-of-Web-apps/)

## 数据库

*数据库模块*

* [asyncpg](https://github.com/MagicStack/asyncpg) - 一个基于 asyncio 的快速的 PostgreSQL 数据库模块
* [asyncpgsa] (https://github.com/CanopyTax/asyncpgsa) - 整合了 Asyncpg 和 sqlalchemy
* [aiopg](https://github.com/aio-libs/aiopg/) - 一个基于 asyncio 和 PostgreSQL 的数据库模块
* [aiomysql](https://github.com/aio-libs/aiomysql) - 一个基于 asyncio 和 MySQL 的数据库模块
* [aioodbc](https://github.com/aio-libs/aioodbc) - 一个基于 asyncio 和 ODBC 的数据库模块
* [motor](https://github.com/mongodb/motor) - 一个基于 asyncio 和 MongoDB 的数据库模块
* [asyncio-redis](https://github.com/jonathanslenders/asyncio-redis) - 基于 asyncio 的 Redis 客户端模块 (PEP 3156).
* [aiocouchdb](https://github.com/aio-libs/aiocouchdb) - 建立在aiohttp (asyncio) 之上的 CouchDB 客户端
* [aioes](https://github.com/aio-libs/aioes) - Asyncio 兼容的 elasticsearch 驱动.
* [peewee-async](https://github.com/05bit/peewee-async) - 基于 [peewee](https://github.com/coleifer/peewee) 和 aiopg 实现 ORM.

## 网络

*网络通讯库*

* [AsyncSSH](https://github.com/ronf/asyncssh) - 基于 SSHv2 协议，提供异步通讯

## 测试

*Libraries to test asyncio based applications.*

* [aiomock](https://github.com/nhumrich/aiomock/) - 支持 async 方式的 mock 模块
* [asynctest](https://github.com/Martiusweb/asynctest/) -  asyncio 增强的 unittest 标准模块
* [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio) - Pytest 的 asyncio 支持.

## Loops替代

*替代实现 asyncio 默认的loop*

* [uvloop](https://github.com/MagicStack/uvloop) - 基于libuv 超级快速的实现 asyncio event loop
* [curio](https://github.com/dabeaz/curio) - 一个协程并发库.

## 杂项

*其他模块*

* [aiofiles](https://github.com/Tinche/aiofiles/) - asyncio 的文件操作

## 文档书籍

*asyncio 相关的文档、书籍、博客等*

* [Official asyncio documentation](https://docs.python.org/3/library/asyncio.html) - Asynchronous I/O, event loop, coroutines and tasks.
* [Short well-written intro to asyncio](http://masnun.com/2015/11/13/python-generators-coroutines-native-coroutines-and-async-await.html) - Generators, Coroutines, Native Coroutines and async/await.
* [Async Through the looking Glass](https://hackernoon.com/async-through-the-looking-glass-d69a0a88b661) - Nice writing about it's worth using asyncio or not for specific use-cases.
* [Asynchronous Python](https://hackernoon.com/asynchronous-python-45df84b82434) - Introduction into asynchronous programming with Python.

## 观点议题

*People has given awesome talks about asyncio.*

* [Topics of Interest (Python Asyncio)](https://www.youtube.com/watch?v=ZzfHjytDceU) - Keynote by David Beazley.

## 本文出处
本文译自：[Awesome asyncio](https://github.com/timofurrer/awesome-asyncio)


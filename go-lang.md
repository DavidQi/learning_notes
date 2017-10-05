# 够浪 Notes

### GoLang 特点
 * 静态语言， 在定义变量时必须指定变量类型，如果赋值的时候类型不匹配，就会报错

### 安装：
```shell
sudo add-apt-repository ppa:gophers/archive
sudo apt-get update

sudo apt-get install golang-1.8
sudo apt-get install golang-1.8-go

sudo ln /usr/lib/go-1.8/bin/go /usr/bin/go1.8
sudo ln /usr/lib/go-1.8/bin/gofmt /usr/bin/gofmt
```

### Python vs GoLang

|   |  Python         |    GoLang       |
|---|-----------|-----------|
|data   |   None    | nil   |
|       |int      |  int, int8, int16, int32, int64         |
|   |   float       |   float. float32, float64 |
|   | b''           |   []byte          |
|   | tuple (immutable)        |   array (mutable, fixed size)  |
|   | list          |   slice           |
|   | dictionary    |   maps            |
| class  | class class_name(base_name):        |   type struct_name struct{...}          |
|concurrency|async def coroutine_name():  await... |  go func_name(c <-chan)|



|Type |长度可变|元素可变|元素可寻址|查找会改变长度|共享底层元素| len()| cap()| close()|delete()|make()|
|---|----|----|----|----|----|---|---|---|---|---|
|string| | | | | Y| Y|||||
|array| |Y|Y| ||Y|Y|
|slice| Y|Y|Y||Y|Y|Y|||Y|
|map| Y|Y|||Y|Y|||Y|Y|
|channel| Y|||Y| Y|Y|Y|Y||Y|

new只分配内存，make用于slice，map，和channel的初始化，并且不返回指针


channel有四个操作：

* 创建：c = make(chan int)
* 发送：c <- 1
* 提取：i <- c
* 关闭：close(c)


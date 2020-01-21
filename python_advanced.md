# Python 进阶


## python with语句 与contextmanager 上下文管理器

[有一篇详细的介绍](http://effbot.org/zone/python-with-statement.htm)

如果有一个类包含  `__enter__` 方法和 `__exit__` 方法，像这样：
```python
class  controlled_execution:
        def__enter__(self):
            set things up
            return thing
        def__exit__(self, type, value, traceback):
            tear things down
```
那么它就可以像这样和with一起使用：
```python
with controlled_execution() as thing:
         some code
```
当with语句被执行的时候，python对表达式进行求值，对求值的结果（叫做“内容守护者”）调用`__enter__`方法，并把`__enter__`方法的返回值赋给as后面的变量。然后python会执行接下来的代码段，并且无论这段代码干了什么，都会执行“内容守护者”的`__exit__`方法。

作为额外的红利，`__exit__`方法还能够在有exception的时候看到exception，并且压制它或者对它做出必要的反应。要压制exception，只需要返回一个true。

比如，下面的`__exit__`方法吞掉了任何的TypeError，但是让所有其他的exceptions通过：
```python
def __exit__(self, type, value, traceback):
        return isinstance(value, TypeError)
```
在Python2.5中，file object拥有__enter__和__exit__方法，前者仅仅是返回object自己，而后者则关闭这个文件：
```python
    >>> f = open("x.txt")
    >>> f
    <open file 'x.txt', mode 'r' at 0x00AE82F0>
    >>> f.__enter__()
    <open file 'x.txt', mode 'r' at 0x00AE82F0>
    >>> f.read(1)
    'X'
    >>> f.__exit__(None, None, None)
    >>> f.read(1)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: I/O operation on closed file
```
这样要打开一个文件，处理它的内容，并且保证关闭它，你就可以简简单单地这样做：
```python
with open("x.txt") as f:
    data = f.read()
    do something with data
```
数据库的连接也可以和with一起使用：
```python
with sqlite.connect("somedb") as conn:
    conn.execute("insert into sometable values (?,?)",("foo","bar"))
```
在这个例子中，commit()是在所有with数据块中的语句执行完毕并且没有错误之后自动执行的，如果出现任何的异常，将执行rollback()操作，再次提示异常。

Sample code of with statement:
```python
class controlled_execution(object):
    def __init__(self, filename):
        self.f, self.filename = None, filename

    def __enter__(self):
        try:
            self.f = open(self.filename, 'r')
            return self.f.read()
        except IOError ,e:
            print 'Error %s' % str(e)
            #return None

    def __exit__(self, type, value, traceback):
        if self.f:
            print 'type:%s, value:%s, traceback:%s' %(str(type), str(value), str(traceback))
            self.f.close()

def test3(filename):
    with controlled_execution(filename) as thing:
        if thing:
            print thing
```

@contextmanager

编写__enter__和__exit__仍然很繁琐，因此Python的标准库contextlib提供了更简单的写法
```python
from contextlib import contextmanager

@contextmanager
def controlled_execution(filename):
    f = open(filename, 'r')
    yield f
    f.close()
```

在某段代码执行前后需要加入自动执行特定代码的时候，也可以用@contextmanager实现。例如：
```python
from contextlib import contextmanager

@contextmanager
def tag(name):
    print("<%s>" % name)
    yield
    print("</%s>" % name)

with tag("title"):
    print("hello world!")
```

contextlib.closing
如果一个对象没有实现上下文，我们就不能把它用于with语句。这个时候，可以用closing()来把该对象变为上下文对象。例如：
```python
from contextlib import closing

with closing(open(filename, 'r')) as f:
    for line in f:
        print(line)
```
closing也是一个经过@contextmanager装饰的generator， 它的作用就是把任意对象变为上下文对象，并支持with语句。


## Singleton 单态模式的作用与实现

### 什么是 Singleton 单态模式

Singleton是一种创建型模式，指某个类采用Singleton模式，则在这个类被创建后，只可能产生一个实例供外部访问，并且提供一个全局的访问点，一般用于Activity的控制层

全局对象和Singleton模式有本质的区别，因为大量使用全局对象会使得程序质量降低，而且有些编程语言根本不支持全局变量。最重要的是传统的全局对象并不能阻止一个类被实例化多次。

### Singleton 单态模式的作用

因为使用 Singleton 限制了实例的个数，可以节省内存，有利于垃圾回收 (garbage collection)

### Singleton 单态模式的应用

　　单例模式应用的场景一般发现在以下条件下：

　　（a）资源共享的情况下，避免由于资源操作时导致的冲突， 性能损耗或资源消耗等。如日志文件，应用配置。

　　（b）控制资源的情况下，只允许使用一个公共访问点，不能通过其他途径访问该实例，方便资源之间的互相通信。如线程池等。


1. Task Manager
2. Recycle Bin
3. Counter
4. logger
5. configuration
6. DB connection
7. File System Operation
8. Pool
9. Load-Balancer
10. Token generator


### 建立 Singleton 单态模式的方法

__Pyhton:__

1. 传统

    ```Python
    class Alone:
        singleton = None
        def __init__(self):
            if not Alone.singleton:
                Alone.singleton = Alone()
            else:
                return Alone.singleton
    ```


2. 新型

    ```python
        class Singleton(object):
           _singleton = None
           def __new__(cls, *args, **kw):
               if not cls._singleton:
                   cls._singleton = object.__new__(cls, *args, **kw)
               return cls._singleton
    ```

3. 装饰

    ```python
    ### as decorator
    class singleton(object):
            def __init__(self, cls):
                    self.cls = cls
                    self.ins = None
            def __call__(self, *args, **kwds):
                     if not self.ins:
                          self.ins = self.cls( *args, **kwds)
                     return self.ins

    @singleton
    class DB:
            conn = None
            def get_conn(self):
                    if not self.conn:
                          self.conn = MySQLdb.connect(...)
                    return self.conn
    ```

4. 元类

    ```python
    class Singleton(type):
        def__call__(cls, *args, **kwargs):
            if not hasattr(cls, '_instance'):
                cls._instance = super(Singleton, cls).call(*args, **kwargs)
            return cls._instance

    class Foo():
        __metaclass__ = Singleton
    ```


__PHP:__

```PHP
class Alone{
    private static $singleton;
    private __construct() {
        if(!self::$singleton){
            self::$singleton = new Alone();
        }
        return self::$singleton;
    }
}
```



## 浅析python的metaclass

### I. metaclass的作用是什么？（感性认识）
metaclass能有什么用处，先来个感性的认识：

1. 你可以自由的、动态的修改/增加/删除 类的或者实例中的方法或者属性
2. 批量的对某些方法使用decorator，而不需要每次都在方法的上面加入@decorator_func
3. 当引入第三方库的时候，如果该库某些类需要patch的时候可以用metaclass
4. 提供接口注册，接口格式检查等
5. 自动委托(auto delegate)
6. 可以用于序列化(参见yaml这个库的实现，我没怎么仔细看）
7. more...

### II. metaclass的相关知识
1. what is metaclass?

    1.1 在wiki上面，metaclass是这样定义的：In object-oriented programming,
    a metaclass is a class whose instances are classes.
    Just as an ordinary class defines the behavior of certain objects,
    a metaclass defines the behavior of certain classes and their instances.

    也就是说metaclass的实例化结果是类，而class实例化的结果是instance。我是这么理解的：
    metaclass是类似创建类的模板，所有的类都是通过他来create的(调用`__new__`)，这使得你可以自由的控制
    创建类的那个过程，实现你所需要的功能。

    1.2 metaclass基础
    * 一般情况下, 如果你要用类来实现metaclass的话，该类需要继承于type，而且通常会重写type的`__new__`方法来控制创建过程。
    当然你也可以用函数的方式（下文会讲）
    * 在metaclass里面定义的方法会成为类的方法，可以直接通过类名来调用

2. 如何使用metaclass

    * 用类的形式

      - 类继承于type, 例如： class Meta(type):pass

      - 将需要使用metaclass来构建class的类的`__metaclass__`属性（不需要显示声明，直接有的了）赋值为Meta（继承于type的类）

    * 用函数的形式
      - 构建一个函数，例如叫metaclass_new, 需要3个参数：name, bases, attrs，

        - name: 类的名字
        - bases: 基类，通常是tuple类型
        - attrs: dict类型，就是类的属性或者函数

      - 将需要使用metaclass来构建class的类的__metaclass__属性（不需要显示声明，直接有的了）赋值为函数metaclas_new

3. metaclass 原理

    3.1 basic

    metaclass的原理其实是这样的：当定义好类之后，创建类的时候其实是调用了type的`__new__`方法为这个类分配内存空间，创建
    好了之后再调用type的`__init__`方法初始化（做一些赋值等）。所以metaclass的所有magic其实就在于这个`__new__`方法里面了。
    说说这个方法：`__new__`(cls, name, bases, attrs)
    - cls: 将要创建的类，类似与self，但是self指向的是instance，而这里cls指向的是class
    - name: 类的名字，也就是我们通常用 `类名.__name__` 获取的。
    - bases: 基类
    - attrs: 属性的dict。dict的内容可以是变量(类属性），也可以是函数（类方法）。

    所以在创建类的过程，我们可以在这个函数里面修改name，bases，attrs的值来自由的达到我们的功能。这里常用的配合方法是
    getattr 和 setattr（just an advice)

    3.2 查找顺序

    再说说关于`__metaclass__`这个属性。这个属性的说明是这样的：
    This variable can be any callable accepting arguments for name, bases, and dict. Upon class creation, the callable is used instead of the built-in type(). New in version 2.2.(所以有了上面介绍的分别用类或者函数的方法）

    The appropriate metaclass is determined by the following precedence rules:
    If `dict['__metaclass__']` exists, it is used.
    Otherwise, if there is at least one base class, its metaclass is used (this looks for a `__class__` attribute first and if not found, uses its type).
    Otherwise, if a global variable named `__metaclass__` exists, it is used.
    Otherwise, the old-style, classic metaclass (types.ClassType) is used.

    这个查找顺序也比较好懂，而且利用这个顺序的话，如果是old-style类的话，可以在某个需要的模块里面指定全局变量
    `__metaclass__ = type` 就能把所有的old-style 变成 new-style的类了。(这是其中一种trick)

### III. 例子
针对第二点说的metaclass的作用，顺序来给些例子：

1. 可以自由的、动态的修改/增加/删除 类的或者实例中的方法或者属性

   ```python
    #!/usr/bin/python
    #coding :utf-8

    def ma(cls):
        print 'method a'

    def mb(cls):
        print 'method b'

    method_dict = {
        'ma': ma,
        'mb': mb,
    }

    class DynamicMethod(type):
        def __new__(cls, name, bases, dct):
            if name[:3] == 'Abc':
                dct.update(method_dict)
            return type.__new__(cls, name, bases, dct)

        def __init__(cls, name, bases, dct):
            super(DynamicMethod, cls).__init__(name, bases, dct)


    class AbcTest(object):
        __metaclass__ = DynamicMethod
        def mc(self, x):
            print x * 3

    class NotAbc(object):
        __metaclass__ = DynamicMethod
        def md(self, x):
            print x * 3

    def main():
        a = AbcTest()
        a.mc(3)
        a.ma()
        print dir(a)

        b = NotAbc()
        print dir(b)

    if __name__ == '__main__':
        main()
    ```
    通过DynamicMethod这个metaclass的原型，我们可以在那些指定了__metaclass__属性位DynamicMethod的类里面，
    根据类名字，如果是以'Abc'开头的就给它加上ma和mb的方法(这里的条件只是一种简单的例子假设了，实际应用上
    可能更复杂）,如果不是'Abc'开头的类就不加. 这样就可以打到动态添加方法的效果了。其实，你也可以将需要动态
    添加或者修改的方法改到__new__里面，因为python是支持在方法里面再定义方法的. 通过这个例子，其实可以看到
    只要我们能操作__new__方法里面的其中一个参数attrs，就可以动态添加东西了。


2. 批量的对某些方法使用decorator，而不需要每次都在方法的上面加入@decorator_func
这个其实有应用场景的，就是比如我们cgi程序里面，很多需要验证登录或者是否有权限的，只有验证通过之后才
可以操作。那么如果你有很多个操作都需要这样做，我们一般情况下可以手动在每个方法的前头用@login_required
类似这样的方式。那如果学习了metaclass的使用的话，这次你也可以这样做:

   ```python
    #!/usr/bin/python
    #coding :utf-8
    from types import FunctionType

    def login_required(func):
        print 'login check logic here'
        return func


    class LoginDecorator(type):
        def __new__(cls, name, bases, dct):
            for name, value in dct.iteritems():
                if name not in ('__metaclass__', '__init__', '__module__') and\
                    type(value) == FunctionType:
                    value = login_required(value)

                dct[name] = value
            return type.__new__(cls, name, bases, dct)


    class Operation(object):
        __metaclass__ = LoginDecorator

        def delete(self, x):
            print 'deleted %s' % str(x)


    def main():
        op = Operation()
        op.delete('test')

    if __name__ == '__main__':
        main()
    ```
    这样子你就可以不用在delete函数上面写@login_required, 也能达到decorator的效果了。不过可读性就差点了。

3. 当引入第三方库的时候，如果该库某些类需要patch的时候可以用metaclass

   ```python
    #!/usr/bin/python
    #coding :utf-8

    def monkey_patch(name, bases, dct):
        assert len(bases) == 1
        base = bases[0]
        for name, value in dct.iteritems():
            if name not in ('__module__', '__metaclass__'):
                setattr(base, name, value)
        return base

    class A(object):
        def a(self):
            print 'i am A object'


    class PatchA(A):
        __metaclass__ = monkey_patch

        def patcha_method(self):
            print 'this is a method patched for class A'

    def main():
        pa = PatchA()
        pa.patcha_method()
        pa.a()
        print dir(pa)
        print dir(PatchA)

    if __name__ == '__main__':
        main()
    ```

4. 提供接口注册，接口格式检查等, 这个功能可以[参考这篇文章](http://mikeconley.ca/blog/2010/05/04/python-metaclasses-in-review-board/)


5. 自动委托(auto delegate)

    [网上的例子](http://marlonyao.iteye.com/blog/762156)

### IV. 总结
1. metaclass的使用原则：

    If you wonder whether you need them, you don't (the people who actually need them know with certainty that they need them, and don't need an explanation about why). --Tim Peters
    也就是说如果你不知道能用metaclass来干什么的话，你尽量不要用，因为通常metaclass的代码会增加代码的复杂度，
    降低代码的可读性。所以你必需权衡metaclass的利弊。

2. metaclass的优势在于它的动态性和可描述性.

    metaclass属于元编程(metaprogramming)的范畴，所谓元编程就是让程序来写(generate/modify)程序，这通常依赖于语言及其运行时系统的动态特性(其实像C
    这样的语言也可以进行元编程)。正如楼主所说，元编程的一个用途就是“可以用另外的函数代码生成,而无需每次手动编写“，在python中我们可以做得更多。

    比如上面例子中的`self.delegate.__getitem__(i)`这样的代码，它可以用另外的函数代码生成,而无需每次手动编写）, 它能把类的动态性扩展到极致。

    我们为什么要修改class？那当然是为了改变它的行为，或者为了创建出独一无二的类。实际中常常需要为class动态添加方法。比如一个数据库表A有
    字段name, address等，表B有name, phone等，你希望A的模型类有find_by_address、find_by_name_and_address等方法，希望B的模型类有
    find_by_name、find_by_phone等方法，但是又不想手写这些方法(其实不可能手写，因为这种组合太多了)，这时你可以在A、B共同的metaclass中定义一个自动添
    加方法的子程序，当然你也可以重写`__getattr__`之类的接口来hook所有find_by_XXX函数调用，这就是时间换空间了，想象你要执行find_by_XXX一百万
    次。也可以比较一下在c++/java中如何应对这种需求。

    对于python而言，metaclass -> class -> instance的关系, metaclass 使程序员可以干涉class 的创建过程，并可以在任何时候修改这样的class (包括修改metaclass)，由于class 的意义是为instance 集合
    持有“方法”，所以修改了一个 class 就等于修改了所有这些 instance 的行为，这是很好的service。

    metaclass也有自己的metaclass（你可以称之为metametaclass、metametametaclass等等）

### V. 补充

1. 注意metaclass的 `__new__` 和 `__init__` 的区别。

   ```python
    class DynamicMethod(type):
        def __new__(cls, name, bases, dct):  # cls=DynamicMethod
        def __init__(cls, name, bases, dct): # cls=你创建的class对象
   ```
    这意味着在`__new__`中我们通常只是修改dct，但是在`__init__`中，我们可以直接修改创建好的类，所以我认为这两个接口的主要区别有2点：
    - 调用时机不同(用处请发散思维)
    - `__new__`能做到比`__init__`更多的事情。比如有时候想改生成的类型名字，或者改类型的父类。:)不过的确大多数场合用`__init__`就够用了。
    - 在`__init__`中控制类生成的过程有一点要注意：在`__init__()`的最后一个参数(attrs)中，对于类中定义的函数类型的属性，比如：

    ```python
    def abc(self):
         pass
    ```
    仍然具有以下的key->value形式：
    ```python
    "abc":<function object>
    ```
    但是在生成的类中，"abc"对应的属性已经从一个function变成了一个unbind method：
    ```python
    self.abc --> unbind method
    ```
    不过实际使用中影响不大。

2. 参考资料:
 * [Metaclass Programming In Python](http://gnosis.cx/publish/programming/metaclass_1.html)
 * [Python中用MetaClass实现委托、不可变集合](http://marlonyao.iteye.com/blog/762156)
 * [Metaclass](http://en.wikipedia.org/wiki/Metaclasses#Python_example)
 * [Other](http://jianpx.iteye.com/blog/908121)


### VI. MetaClass Example
[Chinese:](http://blog.jobbole.com/21351/)

[English:](http://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python)

实际中常常需要为class动态添加方法。比如一个数据库表A有字段name, address等，表B有name, phone等，你希望A的模型类有
find_by_address、find_by_name_and_address等方法，希望B的模型类有find_by_name、find_by_phone等方法，但是又不想手写这些方法(其实不可能手
写，因为这种组合太多了)，这时你可以在A、B共同的metaclass中定义一个自动添加方法的子程序，当然你也可以重写`__getattr__`之类的接口来hook所有
find_by_XXX函数调用，这就是时间换空间了，想象你要执行find_by_XXX一百万次。
```python
class MyMeta(type):
    def __call__(cls, *args, **kwds):
        print '__call__ of ', str(cls)
        print '__call__ *args=', str(args)
        return type.__call__(cls, *args, **kwds)

    def __new__(meta, name, bases, dct):
        print '-----------------------------------'
        print "Allocating memory for class", name
        print meta
        print bases
        print dct
        return super(MyMeta, meta).__new__(meta, name, bases, dct)

    def __init__(cls, name, bases, dct):
        print '-----------------------------------'
        print "Initializing class", name
        print cls
        print bases
        print dct
        super(MyMeta, cls).__init__(name, bases, dct)

class MyKlass(object):
    __metaclass__ = MyMeta
    def __init__(self, a, b):
        print 'MyKlass object with a=%s, b=%s' % (a, b)

class Car(object):
    _MAX_VELOCITY = 100.0
    def __init__(self, initialVelocity):
        self._velocity = initialVelocity

    @property
    def velocity(self):
        return self._velocity

    def accelerate(self, acceleration, deltaTime):
        self._velocity += acceleration*deltaTime
        if self._velocity > self.__class__._MAX_VELOCITY:
            self._velocity = self.__class__._MAX_VELOCITY

car = Car(10.0)
print(car.velocity)
car.accelerate(100.0, 1.0)
print(car.velocity)


class CarMeta(type):
    def __new__(cls, name, bases, attrs):
        return type.__new__(cls, name, bases, attrs)
    @staticmethod
    def createCarClass(carType, maxVelocity):
        return CarMeta('Car_' + carType, (Car,), {'_MAX_VELOCITY':maxVelocity})

Car_Corolla = CarMeta.createCarClass('Corolla', 80.0)
car = Car_Corolla(10.0)
print(car.velocity)
car.accelerate(100.0, 1.0)
print(car.velocity)


class Car(object):
    def setA(self):
        print 'From Car'

class Corolla(object):
    _MAX_VELOCITY = 80.0
    def setB(self):
        print('From Corolla')

class CarMeta(type):
    def __new__(cls, name, bases, attrs):
        return type.__new__(cls, name, bases, attrs)

    @staticmethod
    def createCarClass(carType):
        return CarMeta('Car_' + carType, (Car, globals()[carType]), {})

Car_Corolla = CarMeta.createCarClass('Corolla')
o = Car_Corolla()
print o._MAX_VELOCITY
o.setA()
o.setB()
```

## Become A Pyhton Expert
[《Expert Python programming》](https://www.safaribooksonline.com/library/view/expert-python-programming/9781847194947/)

[Reference](http://my.oschina.net/taisha/blog?catalog=125240)

1.  Keep Code Simple
    减少代码，能减少生成的代码，因此能减少执行时间

2.  使用List Comprehensions构造List，快12倍

3.  使用enumerate来获取index，快20%
    使用enumerate减少了索引计算语句，性能有20%提升

4.  使用Generator处理循环/序列，节省内存
    List Comprehensions节省CPU， Generator节省内存

5.  使用multiprocessing 实现并发 和 asyncio (Pyhton 3.4+) 异步协同

    The multiprocessing package offers both local and remote concurrency, effectively side-stepping the Global Interpreter Lock by using subprocesses instead of threads. A prime example of this is the Pool object which offers a convenient means of parallelizing the execution of a function across multiple input values, distributing the input data across processes (data parallelism).

    使用 multiprocessing 扩展模块和 Generator 可以实现简单的并发操作

    * multiprocessing 示例
      ```python
        from multiprocessing import Process

        def coroutine(n):
             for i in range(3):
                       print 'c%d' %n
                       yield i

        for i in range(3):
            p = Process(target=coroutine, args=(i, ))
            p.start()
            p.join()
      ```
    * asyncio 示例 for MP3 download
      ```python
        import asyncio
        from concurrent.futures import ProcessPoolExecutor
        import aioftp

        async def get_mp3(host, port=21, user='login', pwd='password'):
            async with aioftp.ClientSession(host, port, user, pwd) as client:
                for filepathname, info in (await client.list(recursive=True)):
                    if info["type"] == "file" and filepathname.suffix == ".mp3":
                        await client.download(filepathname)

        loop = asyncio.get_event_loop()
        with concurrent.futures.ProcessPoolExecutor(max_workers=3, ) as executor:
            tasks = (loop.run_in_executor(executor, watch_it, i)
                             for i in ['server1.com', 'server2.com', 'server3.com'])
            loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
      ```

6.  使用itertools迭代

    itertools模块

    itertools模块采用C语言编写，覆盖了大部分迭代模式， 主要有islice、tee和groupby

    * Islice模式用来对子序列进行迭代
      ```python
        import itertools
        for x in itertools.islice('1234567890', 2, 5): #创建一个迭代下标范围为[2, 5)的迭代器
        print(x)
        3
        4
        5

        for x in itertools.islice('1234567890', 5):   #创建一个迭代头五个字符的迭代器
        1
        2
        3
        4
        5
      ```
    * Tee模式用来从一个迭代器上创建多个独立的迭代器迭代
      ```python
        import itertools
        a, b = itertools.tee(‘abcdefghijklmnopqrstuvwxyz’, 2)  #创建两个迭代器a, b， 用来迭代字符串
      ```
    * Groupby创建一个忽略连续重复字符的迭代器
      ```python
        import itertools
        for name, group in itertools.groupby(‘abbccc’):
            pass
        a, <迭代器for a>
        b, <迭代器for bb>
        c, <迭代器for ccc>
      ```
7.  使用Decorator模式

    * Decorator使代码更加易读、灵活[参考链接]
        * 用于参数检查
        * 用于缓冲
        * 用于代理
        * 用于上下文提供

        三篇很好的文章：
        [参考链接](http://www.cnblogs.com/huxi/archive/2011/03/01/1967600.html)
        [参考链接](http://blog.csdn.net/thy38/archive/2009/08/21/4471421.aspx)
        [参考链接](http://www.codecho.com/understanding-python-decorators/)

    * Decorator语法

        * 不带参数的Decorator
          ```python
            def decorator(func):
                return func

            @decorator():
            def example(num):
                print(num)

            example()

            等价于
            def example(num):
                print(num)
            dec = decorator(example)

            dec(num)
          ```
        * 带参数的Decorator

          ```python
            def decorator(logflags=True):
                if logflags == True:
                    def _decorator(func):
                        print(func.__name__)
                        return func
                    return _decorator
                else:
                    return func

            @decorator(logflags=True):
            def example(num):
                print(num)

            example()

            #等价于
            def example(num):
                print(num)
            tmp = decorator(logflags=True)
            dec = tmp(example)

            dec(num)
          ```
    一般多层嵌套的装饰器，建议加下划线的方式命名。每多嵌套一层，便多一个下划线。

8.  使用with替代try…finally

    try…finally主要用于以下场景：

    * Closing a file
    * Releasing a lock
    * Making a temporary code patch
    * Running protected code in aspecial environment

    由于try…finally结构写起来丑陋，因此使用with来代替try…finally

    使用with示例

    ```python
    fd = open(‘readme.txt’, ‘r)
    try:
        for line in fd:
             print line
    finally:
        fd.close()

    可以写作
    with open(‘readme.txt’, ‘r) as fd:
    for line in fd:
         print line
    ```
    定义支持with的类
    ```python
    class test():
        def __enter__(self):
             print(‘enter context’)

        def __exit__(self, exp_type, exp_value, exp_tb):
             print(‘exit context’)

    with test() as t:
    print(t)
    ```
    当with中没有异常抛出时，传入`__exit__`的3个参数为None
    当有异常抛出时，`__exit__`函数应该捕获该异常进行处理，不再抛出

9. @contextmanager使用示例

    使用@contextmanager装饰的方法，会自动将方法中yield前面的语句放入`__enter__`中执行，后面的语句放入`__exit__`中执行。 在with中执行时， yield表达式作为提交给with的表达式结果

    ```python
    import logging
    from contextlib import contextmanager

    @contextmanager
    def logged(klass):
    # logger
        def _log(f):
            def __log(*args, **kw):
                logging.ERROR('%s, %s, %s' % (f.__name__, args, kw))
                return f(*args, **kw)
            return __log

        #遍历类中的所有方法，并用__log方法装饰后，代替原来的方法
        for attribute in dir(klass):
            #遍历非私有方法
            if attribute.startswith('_'):
                continue
            #取得方法名(attrbute)对应的方法对象(element)
            element = getattr(klass, attribute)
            #使用__log封装该方法，并取名为__logged_attribute
            setattr(klass, '__logged_%s' % attribute, element)
            #将原有的attribue方法，替换为封装后的方法
            setattr(klass, attribute, _log(element))

        # let's work 执行到这里，返回给with语句，等待with语句执行完毕，再执行下面的语句
        yield klass

        # let's remove the logging
        for attribute in dir(klass):
            #遍历所有的__logged_开头，封装过的方法
            if not attribute.startswith('__logged_'):
                continue
            element = getattr(klass, attribute)
            #将方法改名（去掉__logged_头）
            setattr(klass, attribute[len('__logged_'):], element)
            #删除__logged_头的方法
            delattr(klass, attribute)

    class One(object):
        def _private(self):
            pass
        def one(self, other):
            self.two()
            other.thing(self)
            self._private()
        def two(self):
            pass

    class Two(object):
        def thing(self, other):
            other.two()

    with logged(One):  #返回yield klass中的klass
        one = One()
        two = Two()
        one.one(two)
    ```
10. Decorator模式和Proxy模式不同之处

    Decorator只用来修饰某个方法，而Proxy模式代理的是一个功能（可能涉及到多个方法）。

    Decorator一般专用于方法，而Proxy用于类


## Python Scenerio UnitTest

#### Way I:
```python
import unittest

class TestSequense(unittest.TestCase):
    pass

def test_generator(a, b):
    def test(self):
        self.assertEqual(a,b)
    return test

if __name__ == '__main__':
    for t in l:
        test_name = 'test_%s' % t[0]
        test = test_generator(t[1], t[2])
        setattr(TestSequense, test_name, test)
    unittest.main()
```

#### Way II:
```python
import unittest2
# Python patterns, scenario unit-testing
from python_patterns.unittest.scenario import ScenarioMeta, ScenarioTest

class TestIsNumeric(unittest2.TestCase):
    __metaclass__ = ScenarioMeta

    class is_numeric_basic(ScenerioTest):
        scenarios = [
            dict(val="1", expected=True),
            dict(val="-1", expected=True),
            dict(val=unicode("123" * 9999), expected=True),
            dict(val="Bad String", expected=False),
            dict(val="Speaks Volumes", expected=False)
        ]
        scenarios += [(dict(val=unicode(x), expected=True),
                       "check_unicode_%s" % x) for x in range(-2, 3)]

        def __test__(self, val, expected):
            actual = is_numeric(val)
            if expected:
                self.assertTrue(actual)
            else:
                self.assertFalse(actual)
```

## Python 资源大全中文版
[Python 资源大全中文版](https://github.com/DavidQi/awesome-python-cn)


## Run a Python script as daemon service
[More details](http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/)

1. Write/Create a shell script as below, named as my_service.sh
```shell
#!/bin/sh

### BEGIN INIT INFO
# Provides:          myservice
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Put a short description of the service here
# Description:       Put a long description of the service here
### END INIT INFO

# Change the next 3 lines to suit where you install your script and what you want to call it
DIR=/path/of/the/python/script
DAEMON=$DIR/name_of_script.py
DAEMON_NAME=myservice

# Add any command line options for your daemon here
DAEMON_OPTS=""

# This next line determines what user the script runs as.
# Root generally not recommended but necessary if you are using the Raspberry Pi GPIO from Python.
DAEMON_USER=root

# The process ID of the script when it runs is stored here:
PIDFILE=/var/run/$DAEMON_NAME.pid

. /lib/lsb/init-functions

do_start () {
    log_daemon_msg "Starting system $DAEMON_NAME daemon"
    start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER --startas $DAEMON -- $DAEMON_OPTS
    log_end_msg $?
}
do_stop () {
    log_daemon_msg "Stopping system $DAEMON_NAME daemon"
    start-stop-daemon --stop --pidfile $PIDFILE --retry 10
    log_end_msg $?
}

case "$1" in

    start|stop)
        do_${1}
        ;;

    restart|reload|force-reload)
        do_stop
        do_start
        ;;

    status)
        status_of_proc "$DAEMON_NAME" "$DAEMON" && exit 0 || exit $?
        ;;

    *)
        echo "Usage: /etc/init.d/$DAEMON_NAME {start|stop|restart|status}"
        exit 1
        ;;

esac
exit 0

```
2. Copy the file my_service.sh to folder `/etc/init.d`, and make both Python and shell scripts executable.
```shell
sudo cp my_service.sh /etc/init.d
sudo chmod 755 my_service.py name_of_script.py
```
3. Add/Update in symbolic links to the /etc/rc?.d in order to run the init script at the boot/default times
 ```shell
 sudo update-rc.d myservice.sh defaults
 ```
4. Test it with following commands
 ```shell
 sudo /etc/init.d/myservice.sh start
 sudo /etc/init.d/myservice.sh status
 sudo /etc/init.d/myservice.sh stop
 ```

## Other

#### Python built-in Function example code: map, reduce, zip, filter

The map, reduce, filter, and zip built-in functions are handy functions for processing sequences. These are related to functional programming languages. The idea is to take a small function you write and apply it to all the elements of a sequence. This saves you writing an explicit loop. The implicit loop within each of these functions may be faster than an explicit for or while loop.

* map ( function , sequence , [ sequence... ] ) → list
    Create a new list from the results of applying the given function to the items of the given sequence . If more than one sequence is given, the function is called with multiple arguments, consisting of the corresponding item of each sequence. If any sequence is too short, None is used for missing value. If the function is None, map will create tuples from corresponding items in each list, much like the zip function.

    Example:
    ```python
    >>> map(lambda a: a+1, [1,2,3,4])
    [2, 3, 4, 5]
    >>> map(lambda a, b: a+b, [1,2,3,4], (2,3,4,5))
    [3, 5, 7, 9]
    >>> map(lambda a, b: a + b if b else a + 10, [1,2,3,4,5], (2,3,4,5))   ＃ the second iterable list is one item short
    [3, 5, 7, 9, 15]
    >>> map(None, [1,2,3,4,5], [1,2,3])
    [(1, 1), (2, 2), (3, 3), (4, None), (5, None)]
    ```
* reduce(function, sequence[, initial]) -> value

    Apply a function of two arguments cumulatively to the items of a sequence, from left to right, so as to reduce the sequence to a single value.
    For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates ((((1+2)+3)+4)+5).  If initial is present, it is placed before the items of the sequence in the calculation, and serves as a default when the sequence is empty.

    Example:
    ```python
    >>> reduce(lambda x, y: x+y, range(0,10))
    45
    >>> reduce(lambda x, y: x+y, range(0,10), 10)
    55
    ```
* filter(function or None, sequence) -> list, tuple, or string

    Return those items of sequence for which function(item) is true.  If function is None, return the items that are true.  If sequence is a tuple
    or string, return the same type, else return a list.

    Example:
    ```python
    >>> filter(lambda d: d != 'a', 'abcd')　　＃ filter out letter 'a'。
    'bcd'
    >>> def d(x):　＃ not using lambda function, instead using a predefined function
     　　　　　return True if x != 'a' else False
    >>> filter(d, 'abcd')
    'bcd'
    ```

* zip(seq1 [, seq2 [...]]) -> [(seq1[0], seq2[0] ...), (...)]

    Return a list of tuples, where each tuple contains the i-th element from each of the argument sequences.  The returned list is truncated
    in length to the length of the shortest argument sequence.

    Example:
    ```python
    zip( range(5), range(1,20,2) )

    [(0, 1), (1, 3), (2, 5), (3, 7), (4, 9)]
    ```

#### 打包python程序，
##### Way I. 得到自己的egg
[Reference](http://my.oschina.net/taisha/blog/60165)

经常接触Python的同学可能会注意到，当需要安装第三方python包时，可能会用到easy_install命令。easy_install是由PEAK(Python Enterprise Application Kit)开发的setuptools包里带的一个命令，它用来安装egg包。egg包是目前最流行的python应用打包部署方式。如何制作和安装egg包？下面我就简单的分析了一下。

1. 安装setuptools
   首先要安装setuptools工具。Debian/Ubuntu下可以直接使用apt安装：
    ```shell
        $ sudo apt-get install python-setuptools
    ```

   手工安装的话，有两种方式：

   * 通过引导程序 ez_setup.py 来安装。这个引导程序会联网下载最新版本setuptools来安装，同时也可以更新本地的setuptools。
    ```shell
    $ wget http://peak.telecommunity.com/dist/ez_setup.py
    $ sudo python ez_setup.py
    # 更新setuptools：:
    $ sudo python ez_setup.py -U setuptools
    ```
   * 或者下载setuptools的egg包来安装。下载完毕以后通过sh安装。
    ```shell
    $ wget http://pypi.python.org/packages/2.6/s/setuptools/setuptools-0.6c11-py2.6.egg
    $ sudo sh setuptools-0.6c11-py2.6.egg
    ```
   现在就可以使用easy_install命令来安装其他的egg包了。

2. 制作自己的egg包

  总是安装别人的egg包，是不是也想制作自己的egg包呢？好，接下来我们就自己制作一个简单的egg包。 首先建立工程目录egg-demo,初始化一个setup.py文件：
    ```shell
    $ mkdir egg-demo
    $ cd egg-demo
    $ touch setup.py
    $ ls
    setup.py
    ```
  下面主要就是填充setup.py。setup.py其实是python工具包distutils的配置文件，setuptools就是基于distutils来做的。 在setup.py中通过setup函数来配置打包信息。首先要引入setuptools的函数setup。setuptools的setup其实就是distutils的setup函数，填写setup.py为以下内容：
    ```python
    $ cat setup.py
    #!/usr/bin/env python
    #-*- coding:utf-8 -*-

    from setuptools import setup

    setup()
    ```
  写到这里，一个空的egg配置文件就写好了。我们可以使用下面命令生成egg包：
    ```shell
        $ python setup.py bdist_egg
    ```
  下面看看究竟生成了什么：
    ```shell
    $ ls -F
    build/ dist/ setup.py UNKNOWN.egg-info/
    ```
  可以看到多了三个文件夹。而在dist文件夹下，有一个egg文件：UNKNOWN-0.0.0-py2.6.egg。 产蛋成功！先看看这个egg文件是什么格式的：
    ```shell
    $ file dist/UNKNOWN-0.0.0-py2.6.egg
    dist/UNKNOWN-0.0.0-py2.6.egg: Zip archive data, at least v2.0 to extract
    ```
  噢，原来就是一个zip压缩包呀！好，再来看看内部构造：
    ```shell
    $ unzip -l dist/UNKNOWN-0.0.0-py2.6.egg
    Archive:  dist/KNOWN-0.0.0-py2.6.egg
      Length      Date    Time    Name
    ---------  ---------- -----   ----
          120  2010-12-06 17:04   EGG-INFO/SOURCES.txt
            1  2010-12-06 17:04   EGG-INFO/top_level.txt
            1  2010-12-06 17:04   EGG-INFO/zip-safe
            1  2010-12-06 17:04   EGG-INFO/dependency_links.txt
          227  2010-12-06 17:04   EGG-INFO/PKG-INFO
    ---------                     -------
          350                     5 files
    ```
  只有一个EGG-INFO文件夹，内含五个egg信息文件，没了。 这个egg名称未知，版本0.0.0。这是因为我们在setup里什么也没有设置。 显然，这个egg什么也不能做。 下面给它加点料。 在setup.py中，setup函数接收一系列属性作为配置参数。

  * name name是egg包的名称，也是寻找要打包的文件夹的名称，默认是UNKNOWN。
  * version 版本号，默认0.0.0
  * packages 这里要用到setuptools的另一个函数find_packages，顾名思义，find_packages用来将指定目录下的文件打包。
  * zip_safe 默认是False，这样在每次生成egg包时都会检查项目文件的内容，确保无误。

  还有一些描述性的属性，如description，long_description，author，author_email，license，keywords，platform，url等。 填充setup.py文件如下：:

        $ cat setup.py
    ```python
    #!/usr/bin/env python
    #-*- coding:utf-8 -*-

    from setuptools import setup, find_packages

    setup(
            name = "demo",
            version="0.1.0",
            packages = find_packages(),
            zip_safe = False,

            description = "egg test demo.",
            long_description = "egg test demo, haha.",
            author = "amoblin",
            author_email = "amoblin@ossxp.com",

            license = "GPL",
            keywords = ("test", "egg"),
            platforms = "Independant",
            url = "",
            )
    ```
  在egg-demo目录下建立和上述name名称相同的目录demo，demo目录下写__init__.py文件：
    ```shell
        $ mkdir demo
        $ cat demo/__init__.py
    ```
    ```python
    #!/usr/bin/env python
    #-*- coding:utf-8 -*-

    def test():
        print "Hello, I'm amoblin."

    if __name__ == '__main__':
        test()
    ```
  再次生成egg包以后查看egg包信息：
    ```shell
    $ python setup.py bdist_egg
    $ unzip -l dist/demo-0.1.0-py2.6.egg
    Archive:  dist/demo-0.1.0-py2.6.egg
      Length      Date    Time    Name
    ---------  ---------- -----   ----
          121  2010-12-06 17:30   demo/__init__.py
          344  2010-12-06 17:46   demo/__init__.pyc
          137  2010-12-06 17:46   EGG-INFO/SOURCES.txt
            5  2010-12-06 17:46   EGG-INFO/top_level.txt
            1  2010-12-06 17:46   EGG-INFO/zip-safe
            1  2010-12-06 17:46   EGG-INFO/dependency_links.txt
          227  2010-12-06 17:46   EGG-INFO/PKG-INFO
    ---------                     -------
          836                     7 files
    ```
  可以看到，多了一个文件夹demo，里面有我们写的__init__.py。 奉行敏捷原则，先安装了体验一下再说：
    ```shell
    $ sudo python setup.py install
    running install
    install_dir /usr/local/lib/python2.6/dist-packages/
    ...
    creating /usr/local/lib/python2.6/dist-packages/demo-0.1.0-py2.6.egg
    Extracting demo-0.1.0-py2.6.egg to /usr/local/lib/python2.6/dist-packages
    demo 0.1.0 is already the active version in easy-install.pth

    Installed /usr/local/lib/python2.6/dist-packages/demo-0.1.0-py2.6.egg
    Processing dependencies for demo==0.1.0
    Finished processing dependencies for demo==0.1.0
    ```
  OK!安装完毕！接下来我们就可以直接通过import来使用啦！
    ```shell
    $ python -c "from demo import test;test()"
    Hello, I'm amoblin.
    ```
  成功输出！这说明安装正确。我们的一个egg包诞生了。 一般情况下，我们的源程序都放在src目录下，所以接下来将demo文件夹移动到src里。但这样也要修改setup.py文件，修改find_packages函数中参数为'src'，同时增加package_dir参数：
    ```shell
    packages=find_packages('src'),
    package_dir = {'':'src'}
    ```
  这样告诉setuptools在src目录下找包，而不是原来默认的工程根目录。

3. egg文件卸载

  以python2.6版本为例，egg文件一般安装在/usr/local/lib/python2.6/dist-packages/目录下，该目录下还有一个easy-install.pth文件，用于存放安装的egg信息。:
    ```shell
    $ cd /usr/local/lib/python2.6/dist-packages
    $ cat easy-install.pth|grep demo
    ./demo-0.1.0-py2.6.egg
    $ ls -F|grep demo
    demo-0.1.0-py2.6.egg/
    ```
  卸载egg文件很简单，首先将包含此egg的行从easy-install.pth中删除，然后删除egg文件夹即可。

##### Way II. pip install from Github or Nexus repository manager Server
1. setup.py 文件

        $ cat setup.py
    ```python
    #!/usr/bin/env python
    #-*- coding:utf-8 -*-

    from setuptools import setup, find_packages
    
    with open('README.md', 'r') as f:
        long_description = f.read()

    setup(
            name = "demo",
            version="0.1.0",
            packages = find_packages(),
            zip_safe = False,
            install_requires = ['numpy', 'pandas', ],

            description = "test demo.",
            long_description = long_description,
            long_description_content_type = 'text_markdown'
            author = "David Qi",
            author_email = "david.qi@github.com",
            url = 'https://github.com/davidqi/demo_package',

            license = "GPL",
            keywords = ("test", "egg"),
            platforms = "Independant",
            )
    ```

2. build packages

        This command will create folders 'dist' and 'demo.egg-info'. The package will be dist/demo-0.1.0.tar.gz

    ```shell
    $ sudo pip3 install --upgrade pip setuptools
    $ python3 setup.py sdist
    ```

3, deploy the built package into Github or Nexus Server

4, pip install the package from Github repo or Nexus repository manager Server


    ```shell
    $ pip3 install git+ssh://git@github.com/davidqi/demo_package.git --user
    ```
    
        Or
        
    ```shell
    $ pip3 -i http://mynexus:8081/repository/pypi-dev/simple --trust-host mynexus:8081 install demo_package --user
    ```
    
4.1, setup /etc/pip.conf

    ```shell
    $ cat /etc/pip.conf
    [global]
    index=http://mynexus:8081/repository/pypi-dev/simple
    index-url=http://mynexus:8081/repository/pypi-dev/simple
    trusted-host=mynexus:8081
    $
    ```
    
      and then
      
    ```shell
    $ pip3 install demo_package --user
    ```


#### python 抽象类、抽象方法的实现
由于 Python 没有[抽象类和接口的概念](#Abstract_vs_Interface)， 所以要实现类似功能需要用内置的abc 类库 (为什么非要用抽象类、抽象方法呢？？)
```python
from abc import ABCMeta, abstractmethod


# 抽象类
class Abstract(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.variable = ''

    @abstractmethod
    def _do_func(self):
        pass

    def __str__(self):
        return str(self.variable)

    def __repr__(self):
        return repr(self.variable)


# 抽象类的实现
class Implement(Abstract):
    def __init__(self, a, b):
        super(Implement, self).__init__()
        self.impl = self._do_func(a, b)

    def _do_func(self, a, b):
        return a + b
```


#### Abstract_vs_Interface

Abstract:
- Not all methods have to be abstract
- Abstract methods are declared but not defined
- Can declare varibles or concret methods
- A class can inherit only one abstract class
- Methods and virables can be public, private or protect

Interface:
- All methods are abstract by default
- All methods are declared but not defined
- Can not declare varibles or concrete methods in interface, except constants
- A class can implenment multiple interface, and mutiple interface inherit is possible
- All methods are public

#### pass by value vs pass by reference

Pass By Reference :
- In Pass by reference address of the variable is passed to a function. Whatever changes made to the formal parameter will affect to the actual parameters
- Same memory location is used for both variables.
- it is useful when you required to return more then 1 values

Pass By Value:
- In this method value of the variable is passed. Changes made to formal will not affect the actual parameters.
- Different memory locations will be created for both variables.
- Here there will be temporary variable created in the function stack which does not affect the original variable.


## [相见恨晚的Python 第三方模块]()

## [asyncio 异步并发模块]()
   Python 3.4 以后的版本开始加入asyncio 异步并发模块。建议使用Pyhton 3.5 版本


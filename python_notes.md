# Python Notes

## Basic Concept for Computer programming

#### Abstract_vs_Interface

Abstract:
- Not all methods have to be abstract
- Abstract methods are declared but not defined
- Can declare variables or concrete methods
- A class can inherit only one abstract class
- Methods and variables can be public, private or protect

Interface:
- All methods are abstract by default
- All methods are declared but not defined
- Can not declare variables or concrete methods in interface, except constants
- A class can implement multiple interface, and multiple interface inherit is possible
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


## Basic Knowledge of Python

Python 是一种面向对象的编程语言。

Python 没有[抽象类和接口的概念](#Abstract_vs_Interface)，因为Python 是一种动态语言，动态语言不需要预先确定对象的声明。
C++/Java/Go 等静态语言出于编译的需要，对于类型处理要预先定义，就是需要一个确定类型声明，所以才需要定义 abstract，interface，才会出现implement 的概念。
但这并不表示Python 不能使用 abstract 和 interface。有时为了保证传入对象的正确性，比如在做框架时，使用interface 做一些约定，还是很有必要，因为interface 有时其实代表的是一种标准。
Python 的抽象基类由abc模块构成，包含了一个叫做 ABCMeta 的 metaclass。这个 metaclass 由内置的 isinstance() 和 issubclass() 特别处理，并包含一批基础抽象基类。

python 也不强迫必须用面向对象的方法来写程序，允许用面向过程的方式来写模块、函数等。

### locals(), globals() & vars()
    Each of these return a dictionary:
    * globals() always returns the dictionary of the module namespace
    * locals() always returns a dictionary of the current namespace
    * vars() returns either a dictionary of the current namespace (if called with no argument) or the dictionary of the argument.

    For example:
    ```python
    class Test(object):
        def __init__(self):
            self.s = 'test'
        def setV(self):
            vars(self)[self.s] = 'great'
            globals()[self.s] = 'GREAT'
        def getV(self):
            print self.test
            return vars(self)[self.s]
    o =  Test()
    o.setV()
    o.getV()
    test
    o.test
    ```

### 1. 经典对象（classic class）
“经典”往往是对旧事物的尊称，既然从2.2版开始推出新型对象，肯定是有种种好处的，所以该尽量用[新型对象](#新型对象).

在2.1及其之前版本的python，只能用经典对象这种对象模型来编程。在2.2和2.3版本的python，经典对象也是默认的对象模型。

#### 1.1 经典对象的一些特征：
* 可以象调用函数一样的来调用一个对象。一旦调用，该对象的一个实例就被建立。
* 可以随意地为对象内部的属性命名。
* 属性可以是数据类型，也可以是函数类型。
* 若属性（attribute）是函数类型，那么就把它看做对象的一个方法（method）。
* Python 为函数规定了一种特殊的命名方式，用前后两个下划线来包围函数名，例如：`__methodName__`。
* 对象可以继承。

#### 1.2 对象声明
声明对象的语法：
```python
class classname[(base-classes)]:
    statement(s)
```

classname是函数名。
base-classes的值必须为对象，用逗号分隔，它相当于java中的超类（superclass）。继承关系可以被传递，如果c1是c2的子类，c2是c3的子类，那么c1也是c3的子类。

内建函数issubclass(C1, C2)可以判断继承关系，若c1是c2的子类，那么函数返回true。由于任何类都被看作是自身的子类，所以若有类C，那么issubclass(C,C)返回true。


#### 1.3 对象正文
##### 1.3.1    对象内部的属性
在对象内部调用其属性，直接写其属性名称即可，如：
```python
class C:
    x = 23
    y = x + 22                  # must use just x, not C.x
```
但若在对象内部定义了方法，要在方法中调用对象中的其它属性，需要写属性的全名，如：
```python
class C:
    x = 23
    def amethod(self):
        print C.x      # must use C.x, not just x
```
当对象被声明的时候，其中的一些属性已经被隐式声明了。
`__name__`：类的名称

`__base__`：tuple对象，放置对象的所有基类

`__dict__`：dict对象，放置对象的所有属性

例如：对象C内部有属性S，那么`C.S=x` 等价于`C.__dict__['S']=x`

##### 1.3.2    对象内部的函数
对象内部的函数写法与普通的函数写法差不多，不过函数的第一个参数要写为self，如：
```python
class C:
    def hello(self):
        print "Hello"
```
##### 1.3.3    私有变量
私有变量的声明，只需在变量名前面加两个下划线，如类C的内部有私有变量user，应声明为：__user。

事实上，当python编译的时候，会把__user改为_C__user（即_ClassName__VariableName的格式）。

无论是否在对象内部，以一个下划线开头的变量，都被看作私有变量。

#### 1.4     实例
回顾一下前面的“经典对象的一些特征”中的第一点：“你可以象调用函数一样的来调用一个对象”。创建实例的时候，就是如此创建：
```python
anInstance = C( )
```

##### 1.4.1   `__init__`
如果一个对象的内部，有或继承有`__init__`方法，那么当这个对象被调用（用java上的词可以叫实例化）时，`__init__`方法会自动地被调用。

`__init__`方法不能有返回值，如果一定需要跳出或返回，也只能返回None。例如：
```python
class C:
    def __init__(self):
        return 'sss'
a = C()
```
python会报错：
```python
Traceback (most recent call last):
  File "<pyshell#26>", line 1, in -toplevel-
    a = C();
TypeError: __init__() should return None
```
`__init__`方法的主要目的，是为了在创建对象实例的时候，对对象的属性赋值。这么做可以增加程序的可读性。如果对象内部没有`__init__`，那么你调用对象的时候就不能带上任何的参数。

##### 1.4.2    实例中的属性
用点（.）来访问实例中的属性。
即使一个对象已经被实例化，仍可以个实例增加任意的属性，并对其赋值。
```python
class C: pass
z = C()
z.x = 23
```
实例被创建以后，该实例会被自动加上两个属性：

`__class__`：实例所属的对象

`__dict__`：实例的所有属性（实例自身的属性和其所属对象的属性）  如：
```python
class C:
    def __init__(self, n):
        self.x = n
a = C(234)
a.y=213213
a.__dict__
>>> {'y': 213213, 'x': 234}
```
##### 1.4.3   工厂函数
遥想一下，设计模式中被用得最多得工厂模式（Factory），它被用于创建对象的实例。在python当中，最直接的用来实现工厂模式的方式，似乎是用`__init__`来返回不同的实例，但是，unfortunately，`__init__`最多也只能返回None。所以要实现工厂模式，最佳的方式就是专门写一个函数，用来返回不同的实例，这类函数，可以称之为工厂函数（Factory Function）。

如下例，appropriateCase就是一个工厂函数。
```python
class SpecialCase:
    def amethod(self): print "special"

class NormalCase:
    def amethod(self): print "normal"

def appropriateCase(isnormal=1):
    if isnormal: return NormalCase(  )
    else: return SpecialCase(  )

aninstance = appropriateCase(isnormal=0)
aninstance.amethod()
```
#### 1.5     属性引用
假设x是对象C的实例，当引用x.name的时候，是如何来查找它的值呢？用最简单的话来概括，就是，由小到大由近到远，依次查找name的值。

再说得具体一些，是按下面的方式查找：

* 若x.name是`x.__dict__` 中的key，那么返回`x.__dict__['name']`` （查找自身）
* 否则，查找`C.__dict__`中的key，是则返回`C.__dict__['name']`` （查找所属对象）
* 否则，查找C的基类，在`C.__bases__`中继续按上面的两步查找（查找所属对象的基类）
* 否则，抛出异常：AttributeError

#### 1.6     方法的绑定与非绑定（Bound and Unbound）
上面讲了属性的引用，方法的绑定与非绑定实际上涉及到的是方法引用的问题。方法实际上使用函数来实现。当方法被引用时，并非直接返回其对应的函数，而是将这个函数，载入到了bound或者unbound方法上。

bound 和 unbound的区别在于：bound将特定的函数，与特定的实例相关联；而unbound则相反。

若没有同名属性，直接用函数名（函数名后不带括号），可以观察到其绑定状态。

假设有对象C和实例x：
```python
class C:
       a = 1
       def g(self): print "method g in class C"
x = C()
print x.g
>>> <bound method C.g of <__main__.C instance at 0x00BA2F58>>
print C.g
>>> <unbound method C.g>
```
上面的执行结果表明：x.g被绑定到了C.g()函数上，所以执行x.g()会有结果返回；而C.g没有被绑定，所以执行C.g()没有结果。

##### 1.6.1    细说非绑定
若处于非绑定状态，当一个函数被引用的时候，实际返回的是unbound方法，该方法内部载有该函数。Unbound方法有三个只读属性
* im_class：被引用函数所在的对象
* im_func：被引用的函数
* im_self：总是为None

非绑定的方法也可以被调用，需要把im_class对象的实例名做为第一个参数，那么就会返回im_func的函数了。

例如上面的C.g()没有结果，但可以执行C.g(x)，x为C的实例，就可以得到C.g()函数的正确执行结果了。

##### 1.6.2    细说绑定
当执行x.g()时，返回的是bound 方法。bound方法和unbound方法类似，也有三个只读属性：im_class，im_func，im_self，但不同之处在于：im_self的值为x。

#### 1.7     继承与重载
Python 支持多重继承，经典类在类多重继承的时候采用从左到右深度优先原则匹配方法，而新式类是采用C3算法(有别于广度优先)进行匹配。具体会在[Python 的继承](#Python的继承)中讨论

从前面说到的“属性引用”的查找方法，不难看出python继承的实现方式。若x为C的实例，当调用x.g()的时候，python先看`x.__dict__`中有没有g，没有就查找`C.__dict__`，若再没有就查找`C.__base__`有没有g。`C.__base__`中放置了C的基类，就实现了对象的继承。用这样的机制，也同样实现了重载。

##### 1.7.1    超类代理
在子类中，有可能要用到超类的属性，那么就要使用到超类代理机制，实际上是用unbound方式调用超类的函数。例如：
```python
class Base:
    def greet(self, name): print "Welcome ", name
class Sub(Base):
    def greet(self, name):
        print "Well Met and",
        Base.greet(self, name)
x = Sub()
x.greet('Alex')
```
超类代理常用于`__init__`方法中，因为在python中，子类的`__init__`方法中并不会自动地调用其超类中的`__init__`方法，所以需要利用这种超类代理机制手动调用一下。


### 2. 新型对象 （New-Style Classes）
在python的2.2和2.3版中，若对象直接或间接地继承了python的内建类型的对象，那么它就是新型对象。

#### 2.1     内建类型：object
从python的2.2开始，object是一种内建类型，它也是所有其它内建类型和新型对象的超类。

继承object的对象，需要重载下面方法：
```python
    __new__
    __init__
    __delattr__
    __getattribute__
    __setattr__
    __hash__
    __repr__
    __str__
 ```
#### 2.2     类级方法（Class-Level Methods）
类级方法是新型对象的特征之一，有两类：静态方法和对象方法。

##### 2.2.1    静态方法（Static methods）
静态方法不存在bound和unbound的问题，可以直接调用。用staticmethod声明一个静态方法，如：
```python
class AClass(object):
    def a_static(): print 'a static method'
    astatic = staticmethod(a_static)
anInstance = AClass()
AClass.astatic()
```

##### 2.2.2    类方法（Class methods）
可以在类的内部和类的实例上调用类方法。用classmethod声明，如：
```python
class ABase(object):
    def aclassmet(cls):
        print 'a class method for', cls.__name__
    aclassmet = classmethod(aclassmet)
class ADeriv(ABase):
    pass

bInstance = ABase()
dInstance = ADeriv()
ABase.aclassmet()               # prints: a class method for ABase
bInstance.aclassmet()           # prints: a class method for ABase
ADeriv.aclassmet()              # prints: a class method for ADeriv
dInstance.aclassmet()           # prints: a class method for ADeriv
```
类方法的第一个参数，就是调用这个方法的对象。

##### 2.2.3  静态方法和类方法详解
    [静态方法和类方法详解](#静态方法和类方法详解)


#### 2.3     新型对象
新型对象也具有所有经典对象的特征，但它们还有更为独特的特征，`__init__`和`__new__`

##### 2.3.1    `__init__`
一个新型对象C，它会直接或间接地继承object中的`__init__`方法，如果你不在C当中重载`__init__`方法的话，你传递给C的`__init__`方法任何参数都会被python忽略。

为了避免乱传参数，建议：即使不想在`__init__`做任何事，也该重载`__init__`方法，如：
```python
class C(object):
       def __init__(self): pass
```
这样，如果错误地向`__init__`传递了参数，python就会抛出一个异常。

#### 2.3.2    `__ new__`
所有新型对象都有一个静态方法：`__new__`。假设有一个新型对象C，现在你要创建C的一个实例x，那么你会写：
```python
x = C(23)
```
执行过程是：python首先调用C中的`__new__`方法，`__new__`会返回一个实例，若检测过后该实例的确是C的实例，那么`__init__`会被调用，若`__new__`返回的实例不是C的实例，那么这个实例将不会被初始化(`__init__`)。这一过程和下面的代码等价：
```python
x = C.__new__(C, 23)
if isinstance(x, C):
    C.__init__(x, 23)
```
你也可以自己在C的内部重载它的`__new__`方法，这种重载不需要用staticmethod来声明。
`__new__`方法可以用来返回不同的实例，可以用这种方式来实现Factory工厂模式，还可以实现singleton单态模式。
```python
class Singleton(object):
    _singletons = {}
    def __new__(cls, *args, **kwarg):
        if not cls._singletons.has_key(cls):
            cls._singletons[cls] = object.__new__(cls)
        return cls._singletons[cls]
```
#### 2.4     新型对象的实例
经典对象的实例中的所有特性，在新型对象的实例中也同样具备，新型对象实例还具备一些与之不同的特性。

##### 2.4.1    `__slots__`
`__slots__`的作用和`__dict__`一样，用来存放实例的所有方法和属性。`__dict__`是字典（dict）类型，而`__slots__`是元组（tuple）类型，所以用`__slots__`会更节约内存，这也是使用它的唯一目的。要注意的是，一旦使用`__slots__`，那么原先的`__dict__`就没有作用了。

如果一个对象会同时产生百万级数目的实例，用`__slots__`会起到节约内存的目的，如果只是几千个实例，那么没必要。

还需要注意的是：实例中的`__slots__`不会被子类继承(????)。示例：
```python
class OptimizedRectangle(Rectangle):
    __slots__ = 'width', 'heigth'

class C(object):
  __slots__ = ['a']
class D(C):
  __slots__ = ['b']
d = D()
d.a = d.b = 2
```
##### 2.4.2    __getattribute__ & __getattr__
对实例属性的引用，都通过object中`__getattribute__`方法来实现。你也可以重载该方法来获得某些特殊的效果。例如，你不想list中的append方法被调用，就可以这样：
```python
class listNoAppend(list):
    def __getattribute__(self, name):
        if name == 'append': raise AttributeError, name
        return list.__getattribute__(self, name)
```
那么，每当x.append被调用的时候，都会出现异常。

##### 2.4.3    属性（properties）
这里说的“属性”，是和方法相对的。在对象内部定义属性的时候，用python的内建类型：property。示例如下：
```python
class Rectangle(object):
    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth
    def getArea(self):
        return self.width * self.heigth
    area = property(getArea, doc='area of the rectangle')
```
上例中，area就是Rectangle的属性，由于只定义了get方法，所以它是只读属性。doc是属性的docstring参数，docstring的作用非常类似于注释，但和注释相比，它可以在运行时被使用，这时它的一大优点。
使用property的语法如下：
```python
attrib = property(fget=None, fset=None, fdel=None, doc=None)
```
属性操作代码示例
* 读取
```python
n = x.attrib
```
返回property中fget函数值
* 赋值
```python
x.attrib = 54
```
将值传入perperty中fset函数
* 删除
```python
del x.attrib
```
调用fdel函数

在经典对象模型中，如果要实现上面的代码，要这样写：
```python
class Rectangle:
    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth
    def getArea(self):
        return self.width * self.heigth
    def __getattr__(self, name):
        if name=  ='area': return self.getArea(  )
        raise AttributeError, name
    def __setattr__(self, name, value):
        if name=  ='area':
            raise AttributeError, "can't bind attribute"
        self.__dict__[name] = value
```

Another Example:
```class Person(object):
    def __init__(self, name):
        self._name = name
    def getName(self):
        print('fetch...')
        return self._name
    def setName(self, value):
        print('change...')
        self._name = value
    def delName(self):
        print('remove...')
        del self._name
    name = property(getName, setName, delName, "name property docs")

bob = Person('Bob Smith')
print(bob.name)
bob.name = 'Robert Smith'
print(bob.name)
del bob.name
print('-'*20)
sue = Person('Sue Jones')
print(sue.name)
print(Person.name.__doc__)
```

Also can use decorator:
```
class Person(object):
    def __init__(self, name):
        self._name = name
    @property
    def name(self):
        "name property docs"
        print('fetch...')
        return self._name
    @name.setter
    def name(self, value):
        print('change...')
        self._name = value
    @name.deleter
    def name(self):
        print('remove...')
        del self._name

bob = Person('Bob Smith')
print(bob.name)
bob.name = 'Robert Smith'
print(bob.name)
del bob.name
print('-'*20)
sue = Person('Sue Jones')
print(sue.name)
print(Person.name.__doc__)
```

##### 2.4.4    Descriptors
Descriptors provide an alternative way to intercept attribute access; they are strongly related to the properties discussed in the prior section.

Descriptors are created as independent classes, and they are assigned to class attributes just like method functions.

The descriptor protocol is simply a set of methods a class must implement to qualify as a descriptor. There are three of them:
 * `__get__(self, instance, owner)`  --  accesses a value stored in the object and returns it.
 * `__set__(self, instance, value)`  --  sets a value stored in the object and returns nothing.
 * `__delete__(self, instance)` --  deletes a value stored in the object and returns nothing.

Like any other class attribute, they are inherited by sub-classes and instances.
```python
class Name(object):
    "name descriptor docs"
    def __get__(self, instance, owner):
        print('fetch...')
        return instance._name
    def __set__(self, instance, value):
        print('change...')
        instance._name = value
    def __delete__(self, instance):
        print('remove...')
        del instance._name

class Person(object):
    name = Name()
    def __init__(self, p_name):
        self._name = p_name

bob = Person('Bob Smith') # bob has a managed attribute
print(bob.name) # Runs Name.__get__
bob.name = 'Robert Smith' # Runs Name.__set__
print(bob.name)
del bob.name
print('-'*20)
sue = Person('Sue Jones')
print(sue.name)
print(Name.__doc__)
```

##### 2.4.5    Per-instance methods
[Look Here](http://docstore.mik.ua/orelly/other/python/0596001886_pythonian-chp-5-sect-2.html)

#### 2.5     新型对象中的继承
在继承这一方面，和经典对象相比，新型对象最大区别就是可以继承自内建类型的对象，而且python中是允许多重继承的。

新式类是采用C3算法(有别于广度优先)进行匹配

##### C3和广度优先的区别:
举个例子就完全明白了:
```
    A
   / \
  B   D
  |   |
  C   E
   \ /
    F
class A(object):pass
class B(A):pass
class C(B):pass
class D(A):pass
class E(D):pass
class F(C, E):pass
```
按照广度优先遍历,F的MRO序列应该是[F,C,E,B,D,A]
但是C3是[F,E,D,C,B,A]
意思是你可以当做C3是在一条链路上深度遍历到和另外一条链路的交叉点,然后去深度遍历另外一条链路,最后遍历交叉点

##### 2.5.1    方法的解析顺序
当存在继承关系的时候，python会到一个对象的基类（base class）中去查找方法或属性，特别是当存在多重继承关系的时候，查找的顺序是怎样的呢？这种查找顺序，被称为解析顺序（resolution order）。

假设有类A，它直接继承自B和C（顺序为：B，C），B和C又都继承自D。

经典对象模型的解析顺序是：左边优先，再深度优先。所以它的解析顺序是：先A-B-D-C-D。

新型对象模型的即席顺序是：A-B-C-D-object

写程序的时候，经典对象模型的这种解析顺序可能会产生一些问题，所以新型对象中更改了解析顺序，会先解析同级的基类。

##### 2.5.2    超类调用
当重载（override）一个方法的时候，我们往往会对超类的同名方法做一些操作，但在多重继承的情况下，python目前的方法解析顺序并不完美。

看下面代码：
```python
class A(object):
    def met(self):
        print 'A.met'

class B(A):
    def met(self):
        print 'B.met'
        A.met(self)
class C(A):
    def met(self):
        print 'C.met'
        A.met(self)
class D(B,C):
    def met(self):
        print 'D.met'
        B.met(self)
        C.met(self)

d=D()
d.met()
代码执行结果如下：
D.met
B.met
A.met
C.met
A.met
```
可以看到，A中的met被调用了两次。如果才能保证超类中的同名方法只被调用一次呢？这可以用python2.2中的super来解决，super是一种新的内建类型。调用super(aclass, obj)会返回obj的超类。

上面的代码可以做如下的修改：
```python
class A(object):
    def met(self):
        print 'A.met'
class B(A):
    def met(self):
        print 'B.met'
        super(B, self).met(  )
class C(A):
    def met(self):
        print 'C.met'
        super(C, self).met(  )
class D(B,C):
    def met(self):
        print 'D.met'
        super(D, self).met(  )
```

##### 2.5.3 总结
    由于Python 继承的特点，
    1. 尽量避免多重继承
    2. super使用一致
    3. 不要混用经典类和新式类
    4. 调用父类的时候注意检查类层次


#### 2.6 Comparation : Using Super() in Inheritance & Using ParentName.Func() in Inheritance
```python
class A(object):
    def __init__(self, s=''):
        print("Start A")
        super(A,self).__init__()
        print('Running A.__init__')
        print("End A")

class B(A):
    def __init__(self, s):
        print("Start B")
        super(B,self).__init__(s)
        print('Running B.__init__')
        #A.__init__(self)
        print("End B")

class T(object):
    def __init__(self):
        print("Start T")
        print('Running T.__init__')
        super(T,self).__init__()
        print("End T")

class C(T):
    def __init__(self):
        print("Start C")
        print('Running C.__init__')
        super(C,self).__init__()
        print("End C")

class D(B,C):
    def __init__(self):
        print("Start D")
        print('Running D.__init__')
        super(D,self).__init__('test')
        print("End D")

foo=D()
```

##### 2.5.4  Use parent class decorators in a child class

* Way I:
```python
def deco( func ):
    print repr( func )
    def wrapper( self ):
        self.do_something()
        return func( self )
    return wrapper

class A:
    def do_something( self ):
        # Do something
        print 'A: Doing something generic for decoration'

    @deco
    def do_some_A_thing ( self ):
        # Do something
        print 'A: Doing something generic'

class B ( A ):
    @deco
    def do_some_B_thing( self ):
        # Do something
        print "B: Doing something specific"

a = A()
b = B()
a.do_some_A_thing()
b.do_some_B_thing()
<function do_some_A_thing at 0x9a516f4>
<function do_some_B_thing at 0x9a51c6c>
A: Doing something generic
A: Doing something generic for decoration
B: Doing something specific
A: Doing something generic for decoration
```

* Way II:
```python
class A(object):
    def _deco(func):
        print repr( func )
        def wrapper(self, *args, **kwargs):
            self.do_something(*args)
            return func(self, *args, **kwargs)
        return wrapper

    def do_something(self):
        # Do something
        print 'A: Doing something generic for decoration'

    @_deco
    def do_some_A_thing ( self ):
        # Do something
        print 'A: Doing something generic'

   #no more uses of _deco in this class
    _deco = staticmethod(_deco)
   # this is the key. it must be executed after all of the uses of _deco in
   # the base class. this way _deco is some sort weird internal function that
   # can be called from within the class namespace while said namespace is being
   # created and a proper static method for subclasses or external callers.


class B(A):
    @A._deco
    def do_some_B_thing( self ):
        # Do something
        print "B: Doing something specific"
a = A()
b = B()
a.do_some_A_thing()
b.do_some_B_thing()
```


## 静态方法和类方法详解

### @staticmethod vs @classmethod

Python 除了拥有实例方法外，还拥有静态方法和类方法，跟Java相比需要理解这个类方法的含义。
```python
class Foo(object):
    def test(self): #定义了实例方法
        print("object")
    @classmethod
    def test2(cls): #定义了类方法
        print("class")
    @staticmethod
    def test3(): #定义了静态方法
        print("static")
```
实例方法访问方式：
```python
ff=Foo()
ff.test()//通过实例调用
Foo.test(ff)//直接通过类的方式调用，但是需要自己传递实例引用
```
类方法访问方式：
```python
ff=Foo()
ff.test2()//通过实例调用
Foo.test2();
```
如果Foo有了子类并且子类覆盖了这个类方法，最终调用会调用子类的方法并传递的是子类的类对象。
```python
class Foo2(Foo):
    @classmethod
    def test2(self):
        print(self)
        print("foo2 object")
f2=Foo2()
print(f2.test2())

输出结果：
<class '__main__.Foo2'>
foo2 object
```
静态方法调用方式：
```python
ff=Foo()
ff.test3()//使用实例调用
Foo.test3()//直接静态方式调用
```
### 总结:
其实通过以上可以看出：

实例方法，类方法，静态方法都可以通过实例或者类调用，只不过实例方法通过类调用时需要传递实例的引用（python 3可以传递任意对象，其他版本会报错）。

三种方法从不同层次上来对方法进行了描述：实例方法针对的是实例，类方法针对的是类，他们都可以继承和重新定义，静态方法也能继承(NND)，可以认为是全局函数。

Python文档里有一句话：Static methods in Python are similar to those found in Java or C++.

所以把python的static method理解成为c++/java的类的static方法就差不多了。一个staticmethod和一个普通的global method没有太大的区别，放在类里面主要基于模块化的考虑。

classmethod是python独特的特性，在c++/java里面找不到对应的版本。它和staticmethod相似，不需要访问instance variable。由于其将class作为第一个参数，所以基类和继承类可借此实现不同的行为。例如设计一个基类，包含一个统计类的对象个数的factory方法：
```python
class A(object):
    cnt = 0
    @classmethod
    def count(cls):
        cls.cnt += 1
        return cls()

class B(A):
    pass

class C(B):
    pass
```
所有的继承类都具备了计数功能的count方法。这个功能是没办法用staticmethod来完成的。

通过继承得到的staticmethod和其基类的方法完全相同，所以根本没有办法对其基类和继承类的对象分别进行计数（其实返回不同的对象也是不可能的）。
```python
#Another example:
class Foo1:
    str = "I'm a static method, Foo1."
    @staticmethod
    def bar():
        print Foo1.str
Foo1.bar()

class Foo11(Foo1):
    str = "I'm a static method, Foo11."
Foo11.bar()

class Foo2:
    str = "I'm a class method."
    @classmethod
    def bar(cls):
        print cls.str
Foo2.bar()

class Foo21(Foo2):
    str="I'm class method Foo21"
Foo21.bar()
```





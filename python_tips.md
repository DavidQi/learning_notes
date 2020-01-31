# Python Tips

## pythonic examples，意思是这些例子是属于python转用的写法
[More examples](http://www.siafoo.net/article/52)

##### 1. 百分号的使用：

通常我们都是这样格式化字符串的:
```python
print 'hello world programme by %s' % 'python'
```

有一种用dict来格式化的%，可读性非常高。
代码如下：
```python
#包含字符串
value = {'what': 'hello, world', 'language': 'python'}
print '%(what)s, %(language)s' % value
#也可以包含int的
value = {'name': 'jianpx', 'age': 23}
print '%(name)s 's age is  %(age)i' % value
```

__Python 3 之后的版本建议使用内置函数 format()__

##### 2. 用两个元素之间有对应关系的list构造一个dict：

运用zip可以非常简单的实现：
```python
names = ['jianpx', 'yue']
ages = [23, 40]
m = dict(zip(names,ages))
```

##### 3. 交换两个值：
在其他语言可能要一个临时变量和三句话：
```python
temp = a
a = b
b = tem
```
但是在python，一句就ok了，而且不需要临时变量：
`a,b = b,a`
右边的b,a 其实可以理解成一个tuple。

##### 4. 数量多的字符串相连用join：
python字符串效率问题之一就是在连接字符串的时候使用‘+’号，例如 s = 's1' + 's2' + 's3' + ...+'sN'，总共将N个字符串连接起来，但是使用+号的话，python需要申请N-1次内存空间，然后进行字符串拷贝。原因是字符串对象PyStringObject在python当中是不可变对象，所以每当需要合并两个字符串的时候，就要重新申请一个新的内存空间（大小为两个字符串长度之和）来给这个合并之后的新字符串，然后进行拷贝。所以用+号效率非常低。建议在连接字符串的时候使用字符串本身的方法join（list），这个方法能提高效率，原因是它只是申请了一次内存空间，因为它可以遍历list中的元素计算出总共需要申请的内存空间的大小，一次申请完。

所以上面的例子可以写成
```python
s = ''.join(['s1','s2',....,'sN'])
```
##### 5. 判断一个key是否在一个dict里面：
```python
if key in dict_example:
    do something
```
In fact has_key() was removed in Python 3.x. 现在不用这样写了。
```python
if dict_example.has_key(key):
    do something
```


##### 6. 去掉list中的重复元素：
```python
old_list = [1,1,1,3,4]
new_list = list(set(old_list))
new_list_sorted = sorted(lst_new, key=old_list.index)
```

##### 7. set vs list
如果对两个都没有重复元素的列表对象，要判断某个元素是否在列表里面的话，当这个列表很大的时候，用set 会比list 的性能要好，因为对于list，本身允许重复元素存在，所以它不是用hash实现的，但是set不一样，它不允许重复元素，看了python源代码，从set的实现源码setobject.c 中查找key的函数的接口可以看出它真的使用hash去实现的。
```python
static setentry *
set_lookkey(PySetObject *so, PyObject *key, register long hash)
```
所以对于in操作，set的实现是计算这个元素的hash值然后判断，理论上可以达到O(1)

##### 8. 读文件操作：
用with关键字可以这样简写了，
```python
with open('filename','r') as f:
    for line in f:
        print line
```

##### 9. 用 enumerate 函数帮输出数组的index和值：
```python
l = [1,3,4]
for index, value in enumerate(l):
    print '%d, %d' % (index, value)
```
##### 10. 关于使用map、filter、reduce的例子网上很多，这里不细说了，它们的使用也是pythonic的examples
In Python 3.x, map() and filter() return iterators. And removed reduce().

##### 11. 分隔一个字符串，去里面的元素，但是空白字符串不要：
例如，
```python
names = 'jianpx, yy, mm, , kk'

name_list = names.split(',')
result = []
for name in name_list:
    if name:
        result.append(name)
```
现在用List Comprehensions 是这样写的：
```python
result = [name for name in names.split(',') if name.strip()]
```
##### 12. 模拟c语言中的  a?b:c
在python里面可以这样做：
```python
return_value = True if a == 1 else False
```

##### 13. 用Decorator抽离公用代码或者解耦
例如要对一个函数做cache，对一个操作限制权限，如果需求随时可能变化，就是说有可能不需要做cache或者不需要做权限的时候，你如果把实现放到这些函数体里面，那么这时你必须把这些代码删除，而且要很小心。但是如果你用Decorator去做的话， 只要删除函数头顶上的@那一行就可以了。Django经常用这种方法做权限控制。
熟悉decorator的应该都很容易理解。

##### 14. 用list的slice 将list的元素倒序并且生成到新的list:
```python
a = [1,2,3,4]
c = 'abcdef'
aa= a[::-1]
cc = c[::-1]
```
如果不用生成新的list，直接调用a.reverse()就得了。但是字符串类型没有reverse的方法.
关于list的slice特性， 其实也许很多人平时只是用list[start:end] 这样的， 这个意思是从start开始，每个元素都放到新
的list里面， 直到end。但是其实还可以每个N个元素才取一次的， 这种情况要3个参数: list[start:end:step]
step就是间隔了。

##### 15.   a = [i for i in range(5)]   和  a = (i for i in range(5))
虽然看上去是一样都生成了5个元素，但是前者是一个list对象， 如果遍历的话 for item in a 就会一下子返回全部元素然后再遍历， 而后者是个Generator，
用for item in a遍历是每次只是返回一个元素， 这样的好处是省内存（在list很大的情况下）。

##### 16. python的all函数可以简化逻辑表达式很多”与“的时候的写法，比如：
```python
a, b, c = True, False, True
if a and b and c:
    return True
else:
    return False
可以简化成:
return all([a, b, c])
```
由此可以看到all()函数的作用是判断当且仅当参数里面都为真的时候返回真， 否则返回假。与之对应的函数是any()
```python
numbers = [1,10,100,1000,10000]
if any(number < 10 for number in numbers):
    print 'Success'

numbers = [1,2,3,4,5,6,7,8,9]
if all(number < 10 for number in numbers):
    print 'Success!'
```

### Python Knowledge in a word
1. repr和str的区别

    repr创建一个字符串，以合法的python表达式的形式来表示值

    str转换为用户更易理解的形式的字符串,str是一种类型

    例如
    ```python
    print repr(1000L)
    >>> 1000L
    print str(1000L)
    >>> 1000
    ```
2. input 和raw_input

    input会假设用户输入的是合法的python表达式，

    raw_input会把用户所有的输入当做原始的数据，即字面上的

    __Python 3 之后只有input__

3. None，python中Null对象

4. python中布尔值为False的对象有None,False,值为0的数，整型 浮点 长整型0，0.0+0.0j，“”，[],(),{}z

    没有__nonzero__（）方法的对象默认值是true

5. 标准类型对象身份比较运算符 is,is not

6. python会缓存简单整数

7. Python的长整型能表达的数值仅仅与你的机器支持的虚拟内存大小有关，与编译语言的长整型概念不一样

8. 对整数的除法默认为地板除，浮点数执行真正的除法，//整除运算符

9. divmod返回（商，余）coerce(num1,num2)将num1,num2转换为同一类型

10. 整数进制转换hex oct bin

11. ASCII转换ord(chr) chr(num) unichr(num)

12. random模块中的randrange(start,stop,step)随即返回之间的一项，uniform()和randint()一样，不过返回的是两者之间的一个浮点数，choice()随机返回序列中的一个元素

13. “string”.translate(string.maketrans('',''),del=' ')根据给出的表转换string字符，del是过滤的字符

14. 那些可以改变对象值的可变对象的方法是没有返回值的, 如列表

15. dict()创建字典，参数是可迭代的，那么每个可迭代的元素必须成对出现

16. hash()可以用来判断某个对象是否可以做一个字典的键，字典的键必须是可哈希的

17. 字典常用方法dict.clear(), get(key,default=None), has_key(key), items(), keys(), values(), iteritems(), iterkeys(), itervalues(), setdefault(key,default=None), update(dict2), iteritems(), iterkeys(), itervalues().
 返回惰性赋值的迭代器，以节省内存 数据集很大的情况下

18. 字典必须每个键只能对应一个项，当键存在冲突，取最近的

19. 集合对象是一组无序排列的课哈希的值

20. copy()方法比调用相应的工厂函数复制对象的副本要快

21. 直接迭代序列比通过索引迭代要快

22. Pyhron 2 的 xrange()类似range()返回一个可迭代对象，用在for循环中. Python 3 后统一使用 range()

23. 迭代器限制：不能向后移动，不能回到开始，也不能复制一个迭代器，想再次迭代同一个对象，只能创建另一个迭代器对象

24. itertools模块提供了各种有用的迭代器

25. 字典和文件是两个可迭代的Python数据类型，字典的迭代器会遍历它的键

26. 在迭代可变对象的时候修改它们并不是个好主意

27. iter() 和实现`__iter__() __next__()`来创建迭代器

28. 生成器表达式是列表解析的一个扩展，在内存使用上更有效

29. sum(),max()参数可以使生成器如：

    max(len(x.strip()) for i in f)

30. sys.argv命令行参数列表，第一个元素时程序的名称

31. os中文件目录访问函数和os.path中的路径访问函数

32. 永久性存储模块pickle marshal可以用来转换存储Python对象，数据的序列化。shelve功能能更完善

33. `__init__.py`中加入`__all__`变量导入子包时指定导入的模块472

34. 实例的`__dict__`仅有实例属性，没有类属性和特殊属性500

35. 类和实例都是名字空间，类是类属性的名字空间，实例则是实例属性的名字空间

36. 任何对实例属性的赋值都会创建一个实例属性（如果不存在）并对其赋值。使用实例属性来改变类属性是很危险的。修改类属性应该使用类名

37. `__base__`类属性 包含其父类的集合的元祖

38. 重写`__init__`不会覆盖自动调用基类的`__init__ `p383

39. 从标准类型中派生类

    不可变类型的例子

    ```python
    class RoundFloat(float):
    　　def __new__(cls,val):
    　　　return super(RoundFloat,cls).__new__(cls,round(val,2))
    ```
40. issubclass()判断一个类是否是另一个类的子类

41. isinstance()判断一个对象是否是另一个类的实例

42. hasattr(),getattr(),setattr(),delattr()

43. super(type[,obj]) super是一个工厂函数，它创造了一个super object，为一个给定的类使用`__mro__`去查找相应的父类

44. vars([obj])返回对象存储于`__dict__`的属性和值的字典，没有参数和locals()一样

45. 实现授权关键点是覆盖`__getattr__()`方法，在代码中包含一个对getattr()内建函数的调用，其工作方式是当搜索一个属性时，任何局部的对象首先被找到，如果搜索失败了，则`__getattr__()`会被调用

46. 新式类：`__getattribute__()`与`__getattr__()`的不同之处在于，当属性被访问时，它就一直可以被调用，而不限于不能找到的情况

47. 新式类：`__slots__`类属性 类变量 是一个序列，有实例属性构成，任何试图创建一个不在`__slots_`_中的名字的实例属性都将导致Attribute异常，防止用户随心所欲的添加实例属性，节约内存

48. 描述符：表示对象属性的一个代理。描述符实际上可以是任何至少实现了三个特殊方法`__get__()、__set__() __delete__()`中的一个，这三个特殊方法充当描述符协议的作用。

49. property(fget=None,fset=None,fdel=None,doc=None)

50. 元类 `__metaclass__` 来定义某些类是如何被创建的，从根本上赋予你如何创建类的控制权。元类一般用于创建类

51. callable()确定一个对象是否可以通过函数操作符来（()）调用

52. compile('code str','存放代码对象的文件的名字，通常为空串','eval/single/exec')允许在运行时刻迅速生成代码对象（字节代码预编译），然后就可以用exec 语句或内建函数eval()来执行这些对象或者对他们进行求值

53. input()相当于eval(raw_input())


### python中检测某个变量是否有定义
* 第一种方法：
```python
'var' in locals().keys()
```
* 第二种方法：
```python
'var' in dir()
```
* 第三种方法：
```python
try:
    print(var)
except NameError:
    print('var not defined')
```
* 第四种方法 for object：
```python
hasattr(objectname, 'var')
```

### 5 ways to convert dict to obj in Python :
* 第一种方法：
```python
d = {'d': ['hi', {'foo': 'bar'}], 'a': 1, 'b': {'c': 2, 'f': {'test': 'result'}, }}
x = type('new_dict', (object,), d)
```
* 第二种方法：
```python
class Xobj(object):
    """
    Simple convert the first layer dictionsy to object
    Same as
    x = type('new_dict', (object,), d)
    """
    def __init__(self, d):
        self.__dict__.update(d)
```
* 第三种方法：
```python
def obj_dic(d):
    """
    :param d: dictionary like {'d': ['hi', {'foo': 'bar'}], 'a': 1, 'b': {'c': 2}}
    :return: object
    """
    top = type('new', (object,), d)
    seqs = tuple, list, set, frozenset
    for i, j in d.items():
        if isinstance(j, dict):
            setattr(top, i, obj_dic(j))
        elif isinstance(j, seqs):
            setattr(top, i, type(j)(obj_dic(sj) if isinstance(sj, dict) else sj for sj in j))
        else:
            setattr(top, i, j)
    return top
```
*  第四种方法：
```python
import json
from argparse import Namespace


def json_convert_dict_to_object(d):
    """
    :param d: dictionary like {'d': ['hi', {'foo': 'bar'}], 'a': 1, 'b': {'c': 2, 'f': {'test': 'result'}, }}
    :return: object
    """
    return json.loads(json.dumps(d), object_hook=lambda x: Namespace(**x))
```
*  第五种方法： Final
```python
import bunch  # for Python2
import munch  # for Python3

x2 = bunch.bunchify(d)
x3 = munch.munchify(d)
```

### Using variable names for python functions
```python
def func_1(v):
    print(v)

def func_2(*args):
    pass

def run_functions(f_name, *args):
    return getattr(self, 'func_' + f)(*args)

for i in ['1', '2']:
    run_functions(i, 'test')
```

### 依序遍历0到100闭区间内所有的正整数，如果该数字能被3整除，则输出该数字及‘*’标记；如果该数字能被5整除，则输出该数字及‘#’标记；如果该数字既能被3整除又能被5整除，则输出该数字及‘*#’标记。
```python
for i in range(1, 101):
    print(str(i)+('*' if i % 3 ==0 else '')+('#' if i % 5 ==0 else ''))
```
Or one-line
```
['Fizz'*(not i%3) + 'Buzz'*(not i%5) or str(i) for i in range(1, 101)]
```

### 计算items 出现次数 in a list
```python
from collections import Counter


l = [4, 2, 5, 2, 5, 1, 8, 4, 89, 3, 6, 72, 56, 24, 6, 3, 2, 6, 27, 9, 2, 5, 8, 9,
    1, 6, 3, 1, 0, 99, 3, 67, 2, 6, 1, 6, 3, 9, 6, 8, 3, 1]

def count_by_dict(l):
    r = {}
    for i in l:
        if i in r:
            r[i] += 1
        else:
            r[i] = 1
    return sorted(r, key=r.get, reverse=True)[0]


def count_by_tuple(l):
    return sorted(((i, l.count(i)) for i in set(l)), key=lambda x: x[1], reverse=True)[0][1]


def count_by_one_line(l):
    return max(((i, l.count(i)) for i in set(l)), key=lambda x:x[1])[1]


def count_by_counter(l):
    c = Counter()
    for i in a:
        c[i] += 1
    return c.most_common()
```

[Look here to see the performance](https://gist.github.com/DavidQi/2fa30eba8d5f0c08a8a6b36d0eff1670)

### 八皇后问题
[Eight queens puzzle](https://en.wikipedia.org/wiki/Eight_queens_puzzle)

```python
from itertools import permutations


def eight_queens_puzzle(queens=8):
    cols = range(queens)
    for vec in permutations(cols):  # Create an 8×8 chessboard
        if 8 == len(set(vec[i] + i for i in cols)) == len(set(vec[i] - i for i in cols)):
            print('\n'.join('- ' * i + 'Q ' + '- ' * ((queens - 1) - i) for i in vec), end='\n\n')
```

### 最长共有字串
To get the max sub string in 2 strings

```python
def get_max_substr(s_short, s_long) :
    if s_short in s_long :
        return s_short
    s1 = get_max_substr(s_long, s_short[:-1])
    s2 = get_max_substr(s_long, s_short[1:])
    if len(s1) > len(s2) :
        return s1
    else:
        return s2
```

### 一组列表中的共有元素
To find intersection of N given list:

```python
def get_intersection_in_lists(input_list=[[1, 2, 3, 4, 5],[2, 3, 4, 5, 6],[3, 4, 5, 6, 7]]):
    return set.intersection(*map(set, input_list))
```

### 最简单的列表反转方法
The simplest way to reverse a list using slice:
```python
a = '12345'
print(a[::-1])
```

### McDonald’s Nuggets
McDonald’s sells Chicken McNuggets in packages of 6, 9 or 20 McNuggets. Thus, it is possible, for example,
to buy exactly 15 McNuggets (with one package of 6 and a second package of 9), but it is not possible to buy
exactly 16 McNuggets, since no non- negative integer combination of 6's, 9's and 20's add up to 16.
To determine if it is possible to buy exactly n McNuggets, one has to find non-negative integer values of
a, b, and c such that 6a+9b+20c=n
Write a function, called McNuggets that takes one argument, n, and returns True if it is possible
to buy a combination of 6, 9 and 20 pack units such that the total number of McNuggets equals n,
and otherwise returns False. Hint: use a guess and check approach.

```python
def mc_nuggets(n):
    return n >= 0 and (n == 0 or mc_nuggets(n-6) or mc_nuggets(n-9) or mc_nuggets(n-20))
```

### 有两个序列a,b，大小都为n,序列元素的值任意整形数，无序； 要求：通过交换a,b中的元素，使[序列a元素的和]与[序列b元素的和]之间的差最小。

```python
def mean_1(sorted_list):
    if sorted_list:
        if len(sorted_list) > 2:
            big = sorted_list.pop()
            small = sorted_list.pop()
            big_list, small_list = mean_1(sorted_list)
            big_list.append(small)
            small_list.append(big)
            big_list_sum = sum(big_list)
            small_list_sum = sum(small_list)
            if big_list_sum > small_list_sum:
                return big_list, small_list
            else:
                return small_list, big_list
        elif len(sorted_list) > 1:
            return [[i] for i in sorted_list]
        else:
            return sorted_list, []


def mean_2(sorted_list):
    l_s, l_b, ls_sum, lb_sum = [], [], 0, 0
    for i in range(0, len(sorted_list), 2):
        if lb_sum > ls_sum:
            l_s.append(sorted_list[i+1])
            ls_sum += sorted_list[i+1]
            l_b.append(sorted_list[i])
            lb_sum += sorted_list[i]
        else:
            l_s.append(sorted_list[i])
            ls_sum += sorted_list[i]
            l_b.append(sorted_list[i+1])
            lb_sum += sorted_list[i+1]
    return l_s, l_b


def mean_3(sorted_list):
    l_s, l_b, ls_sum, lb_sum = [sorted_list[-2]], [sorted_list[-1]], sorted_list[-2], sorted_list[-1]
    ll = len(sorted_list)-2
    for i in range(0, ll//2):
        if (lb_sum - ls_sum) > sorted_list[ll-i-1]:
            l_s.append(sorted_list[ll-i-1])
            ls_sum += sorted_list[ll-i-1]
            l_b.append(sorted_list[i])
            lb_sum += sorted_list[i]
        else:
            if lb_sum > ls_sum:
                l_s.append(sorted_list[ll-i-1])
                ls_sum += sorted_list[ll-i-1]
                l_b.append(sorted_list[i])
                lb_sum += sorted_list[i]
            else:
                l_s.append(sorted_list[i])
                ls_sum += sorted_list[i]
                l_b.append(sorted_list[ll-i-1])
                lb_sum += sorted_list[ll-i-1]
    return l_s, l_b

tests = [[1, 2, 3, 4, 5, 6, 700, 800],
         [10001, 10000, 100, 90, 50, 1],
         list(range(1, 11)),
         [12312, 12311, 232, 210, 30, 29, 3, 2, 1, 1],
         [93, 91, 90, 82, 81, 74, 74, 74, 74, 68, 60, 57, 49, 48, 48, 45, 36, 35, 29, 22]
        ]


def get_distance(l1, l2):
    return abs(sum(l1)-sum(l2))


def final_com(tests):
    for l in tests:
        l.sort()
        print()
        print('Source List:\t', l)
        m11, m12 = mean_1(l)
        print('Result List 1:\t', m11, m12)
        print('Distance 1:\t', get_distance(m11, m12))
        r11, r12 = mean_2(l)
        print('Result List 2:\t', r11, r12)
        print('Distance 2:\t', get_distance(r11, r12))
        r21, r22 = mean_3(l)
        print('Result List 3:\t', r21, r22)
        print('Distance 3:\t', get_distance(r21, r22))
        print('-*'*40)
```

### Balance Number
平衡点问题

平衡点：比如int[] numbers = {1,3,5,7,8,25,4,20}; 25前面的总和为24，25后面的总和也是24，25这个点就是平衡点；

假如一个数组中的元素，其前面的部分等于后面的部分，那么这个点的位序就是平衡点

要求：返回任何一个平衡点

* 使用sum函数累加所有的数。使用一个变量st来累加序列的前部。直到满足条件st<(total-number)/2;

```python
def get_banlance_number(lst_numbers):
    t, st = sum(lst_numbers), 0
    for i, v in enumerate(lst_numbers):
        if st < (t-v)/2:
            st += v
        else:
            return i
```

### Dominate Point
支配点问题：

支配数：数组中某个元素出现的次数大于数组总数的一半时就成为支配数，其所在位序成为支配点；

比如int[] a = {3,3,1,2,3};3为支配数，0，1，4分别为支配点；

要求：返回任何一个支配点

* 具体方法是：将序列排序，取中位数——注意，如果一个大于整体的一半，那么排序之后支配数一定在中间。（原因请参考《编程之美》), 然后验证是否正确。（因为题目说了，可能会不存在）

```python
def find_dominate_point(lst_numbers):
    # lst_numbers = [1,3,4,3,3]
    # calculate
    lst_numbers.sort()
    lens = len(lst_numbers)
    candidate = lst_numbers[lens//2]

    # validate
    validator = 0
    for number in lst_numbers:
        if number == candidate:
            validator += 1

    # print answer
    if validator >= lens/2:
        return lst_numbers[lens//2]
    else:
        return None
```

### 使用heapq实现小顶堆（TopK大）、大顶堆（BtmK小）
需1求：给出N长的序列，求出TopK大的元素，使用小顶堆，heapq模块实现。
```python
import heapq
import random


class TopkHeap(object):
    def __init__(self, k):
        self.k = k
        self.data = []

    def Push(self, elem):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0]
            if elem > topk_small:
                heapq.heapreplace(self.data, elem)

    def TopK(self):
        return [x for x in reversed([heapq.heappop(self.data) for x in range(len(self.data))])]


def main():
    list_rand = random.sample(range(1000000), 100)
    th = TopkHeap(3)
    for i in list_rand:
        th.Push(i)
    print(th.TopK())
    print(sorted(list_rand, reverse=True)[0:3])
```

上面的用heapq就能轻松搞定。

变态的需求来了：给出N长的序列，求出BtmK小的元素，即使用大顶堆。

heapq在实现的时候，没有给出一个类似Java的Compartor函数接口或比较函数，开发者给出了[原因见这里：](http://code.activestate.com/lists/python-list/162387/)

于是，人们想出了[一些很NB的思路：](http://stackoverflow.com/questions/14189540/python-topn-max-heap-use-heapq-or-self-implement)

来概括一种最简单的：
    将push(e)改为push(-e)、pop(e)改为-pop(e)。
    也就是说，在存入堆、从堆中取出的时候，都用相反数，而其他逻辑与TopK完全相同，经过测试，是完全没有问题的，这思路太Trick了…… 看代码：

```python
class BtmkHeap(object):
    def __init__(self, k):
        self.k = k
        self.data = []

    def Push(self, elem):
        # Reverse elem to convert to max-heap
        elem = -elem
        # Using heap algorighem
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0]
            if elem > topk_small:
                heapq.heapreplace(self.data, elem)

    def BtmK(self):
        return sorted([-x for x in self.data])
```

### n 的约数 Factors
```python
def get_factors(n):
    r = []
    for i in range(2, int(n**0.5)+1):  # not include 1 and itself, int(n**0.5) 表示不大于n的平方根的最大整数
        if n % i == 0 and i not in r:
            r.append(i)
            x = n / i
            r.append(x) if x not in r else 0
    return r
```
### 一个字串内是否由一个更短的字串重复n次而构成的，判断或者得到它
思路：如果一个字串内是否由一个更短的字串重复n次而构成，那么子字串的长度必然为字串长度的约数。
所以得到字串长度的所有约数，然后按照约数获取各个子字串并比较

```python
def get_substring(s):
    r, k = [], len(s)
    for i in get_factors(k):
        l = [s[j:j+i] for j in range(0, k, i)]
        r.append(l[0]) if len(set(l)) == 1 else 0
    return r


def is_multiple(s):
    k = len(s)
    for i in get_factors(k):
        ss = ''
        for j in range(0, k, i):
            if ss == '':
                ss = s[j:j+i]
                continue
            if ss != s[j:j+i] :
                ss = ''
                break
        if ss:
            return True
    return False

s = ['testtest', 'bcdbcdbcde', 'testedtested', 'aaaaaaaaaa']
for i in s:
    print(get_substring(i))
    print(is_multiple(i))
```

### python traversal binary tree
* Breadth first search (BFS)
* Depth first search (DFS)

[my binary tree](https://gist.github.com/DavidQi/f79cbe8c828a9b2a83faca747f54297b)

```python
class BinaryTree(object):
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def traverse_BFS(self, tree):
        this_level = [tree]
        while this_level:
            next_level = []
            for n in this_level:
                print(n.data)
                if n.left:
                    next_level.append(n.left)
                if n.right:
                    next_level.append(n.right)
            print()
            this_level = next_level
        return

    def recursive_BFS(self, this_level):
        next_level = []
        for n in this_level:
            print(n.data)
            if n.left:
                next_level.append(n.left)
            if n.right:
                next_level.append(n.right)
        print()
        if next_level:
            self.recursive_BFS(next_level)

    def recursive_DFS(self, tree):
        nodes = []
        if tree:
            nodes.append(tree.data)
            nodes.extend(self.recursive_DFS(tree.left))
            nodes.extend(self.recursive_DFS(tree.right))
        return nodes

    def basic_DFS(self, tree):
        if tree:
            yield tree.data
            for node_data in self.basic_DFS(tree.left):
                yield node_data
            for node_data in self.basic_DFS(tree.right):
                yield node_data


from collections import deque


def print_level_order(node, queue=deque()):
    if node:
        print(node.data)
        [queue.append(n) for n in [node.left, node.right] if n]
        if queue:
            print_level_order(queue.popleft(), queue)
    return


def create_tree(array):
    if array:
        mid = (len(array))//2
        node = BinaryTree(array[mid])
        node.left = create_tree(array[:mid])
        node.right = create_tree(array[mid+1:])
        return node
    return

t = BinaryTree(1, BinaryTree(2, BinaryTree(4, BinaryTree(7))), BinaryTree(3, BinaryTree(5), BinaryTree(6)))
t1 = create_tree(range(9))

t.traverse_BFS(t)
print_level_order(t1)
```

### 二分搜索 binary search
Must be sorted seq/list
[二分搜索 binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm)
```python
def binary_search(seq, p, start_position, end_position):
    pivot = seq[p]
    seq[p], seq[end_position] = seq[end_position], seq[p]
    p_pos = start_position
    for i, val in enumerate(seq[start_position : end_position]):
        if val <= pivot:
            seq[i], seq[p_pos] = seq[p_pos], seq[i]
            p_pos += 1
    seq[p_pos], seq[end_position] = seq[end_position], seq[p_pos]
    return p_pos


def binary_search_re(seq, p, start_position, end_position):
    if start_position > end_position:
        return -1
    mid = start_position + (end_position - start_position) // 2
    # Why not use mid = (end_position + start_position) // 2 ???
    # 在极端情况下，(a + b) 存在着溢出的风险，进而得到错误的mid结果，导致程序错误。
    # 而这个不存在溢出的问题。
    if seq[mid] > p:
        return binary_search_re(seq, p, start_position, mid - 1)
    if seq[mid] < p:
        return binary_search_re(seq, p, mid + 1, end_position)
    return mid
```

### Sort  一些排序方法
```python
"""Sort Sequence.
Usage:
    test_docopt.py [-q | -i | -b | -s | -m | -h | -hy | --shell] <sequence>
    test_docopt.py (-h | --help)


Options:
    -h --help     Show this screen.
"""
from docopt import docopt
import sys, getopt, random
from heapq import *


def bubble_sort(seq):
    for i in range(len(seq)):
        for j in range(len(seq)-i-1):
            if seq[j] > seq[j+1]:
                seq[j], seq[j+1] = seq[j+1], seq[j]
    return seq


def insertion_sort(seq):
    for i in range(1, len(seq)):
        pos, tmp = i, seq[i]
        for j in range(i-1, -1, -1):
            if seq[j] > tmp:
                seq[j+1] = seq[j]
                pos = j
        seq[pos] = tmp
    return seq


def selection_sort(seq):
    for i in range(len(seq)):
        min_index = i
        for j in range(i, len(seq)):
            if seq[j] < seq[min_index]:
                min_index = j
        seq[i], seq[min_index] = seq[min_index], seq[i]
    return seq


def quick_sort(seq):
    if len(seq) < 2:
        return seq
    else:
        return quick_sort([x for x in seq[1:] if x < seq[0]]) + [seq[0]] + quick_sort([x for x in seq[1:] if x > seq[0]])


def shell_sort(seq):
    incr = len(seq)//2
    while incr >= 1:
        for i in range(incr, len(seq)):
            tmp = seq[i]
            pos = i
            for j in range(i-incr, -1, -incr):
                if seq[j] > tmp:
                    seq[j+incr] = seq[j]
                    pos = j
            seq[pos] = tmp
        incr = incr//2
    return seq


def merge_sort(seq):
    if len(seq) <= 1:
        return seq

    middle = len(seq) // 2
    lst_left = merge_sort(seq[0:middle])
    lst_right = merge_sort(seq[middle:])
    return merge(lst_left, lst_right)


def merge(lst_left, lst_right):
    result, left, right = [], 0, 0
    while left < len(lst_left) and right < len(lst_right):
        if lst_left[left] <= lst_right[right]:
            result.append(lst_left[left])
            left += 1
        else:
            result.append(lst_right[right])
            right += 1

    result += lst_left[left:]
    result += lst_right[right:]
    return result


def heap_sort(seq):
    h = [heappush(h, value) for value in seq]
    return [heappop(h) for i in range(len(h))]


def heapify_sort(seq):
    return heapify(seq)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    if arguments.get('-q', Flase):
        print(quick_sort(arguments['<sequence>']))
    if arguments.get('-i', Flase):
        print(insertion_sort(arguments['<sequence>']))
    if arguments.get('-b', Flase):
        print(bubble_sort(arguments['<sequence>']))
    if arguments.get('-s', Flase):
        print(selection_sort(arguments['<sequence>']))
    if arguments.get('-m', Flase):
        print(merge_sort(arguments['<sequence>']))
    if arguments.get('-h', Flase):
        print(heap_sort(arguments['<sequence>']))
    if arguments.get('-hy', Flase):
        print(heapify_sort(arguments['<sequence>']))
    if arguments.get('--shell', Flase):
        print(shell_sort(arguments['<sequence>']))

```


### Lozanić's triangle
sometimes called [Losanitsch's triangle](http://en.wikipedia.org/wiki/Lozani%C4%87's_triangle), is a triangular array of binomial coefficients in a manner very similar to that of Pascal's triangle. It is named after the Serbian chemist Sima Lozanić, who researched it in his investigation into the symmetries exhibited by rows of paraffins.

```python
import sys

pascal_array = []


def run_lozanic(row, position):
    if row == 1 or position == 1 or row == position or (row == 3 and position == 2):
        return 1
    elif (row == 4 and (position == 2 or position == 3)) or (row == 5 and (position == 2 or position == 4)):
        return 2
    elif row == 5 and position == 3:
        return 4
    else:
        if row % 2 != 0:
            if position == 2:
                return run_lozanic(row - 1, position)
            elif position == row - 1:
                return run_lozanic(row - 1, position - 1)
            elif position % 2 == 0:
                return run_lozanic(row - 1, position - 1) + run_lozanic(row - 1, position) - \
                       get_pascal((row//2 - 1), (position - 1)//2)
            else:
                return run_lozanic(row - 1, position - 1) + run_lozanic(row - 1, position)
        else:
            return run_lozanic(row - 1, position - 1) + run_lozanic(row - 1, position)


def get_pascal(n, p):
    if pascal_array:
        return pascal_array[n][p]
    else:
        create_pascal(n)
        return pascal_array[n][p]


def create_pascal(n):
    for i in range(n + 1):
        row = []
        for j in range(i + 1):
            if j == 0 or j == i:
                row.append(1)
            else:
                row.append(pascal_array[i-1][j-1] + pascal_array[i-1][j])
        pascal_array.append(row)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1].isdigit() and int(sys.argv[1]) > 0:
        rows = int(sys.argv[1]) + 1
        create_pascal(rows)
        for i in range(1, rows):
            l = [run_lozanic(i, j) for j in range(1, i + 1)]
            print(l)
        else:
            print('Please input the number you want')
```

| HTTP Method | Explain | Entire Collection (e.g. /customers) | Specific Item (e.g. /customers/{id}) |
| ------------- |:-------------:| -----:| -----:|
| POST | Create | 201 (Created), 'Location' header with link to /customers/{id} containing new ID. |
404 (Not Found), 409 (Conflict) if resource already exists..|
| GET | Read | 200 (OK), list of customers. Use pagination, sorting and filtering to navigate big lists. |
200 (OK), single customer. 404 (Not Found), if ID not found or invalid.|
| PUT | Update/Replace | 
405 (Method Not Allowed), unless you want to update/replace every resource in the entire collection.|
200 (OK) or 204 (No Content). 404 (Not Found), if ID not found or invalid.|
| PATCH | Update/Modify | 405 (Method Not Allowed), unless you want to modify the collection itself. |
200 (OK) or 204 (No Content). 404 (Not Found), if ID not found or invalid.|
| DELETE | Delete | 405 (Method Not Allowed), unless you want to delete the whole collection—not often desirable.|
200 (OK). 404 (Not Found), if ID not found or invalid.|

### An exapmle of REST API using Python & flask

Server Side:

```python
from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser

fk = Flask(__name__)
api = Api(fk)

books = [
    {
        "category": "tech",
        "ISBN": abc100,
        "title": "REST API using Python & Flask"
    },
    {
        "category": "tech",
        "ISBN": xyz200,
        "title": "java10"
    },
    {
        "category": "novel",
        "ISBN": LMN300,
        "title": "Go with Wind"
    }
]

class Book(Resource):
    def get(self, category):
        for book in books:
            if(category == book["category"]):
                return book, 200
        return "category not found", 404

    def post(self, category):
        parser = RequestParser()
        parser.add_argument("ISBN")
        parser.add_argument("title")
        args = parser.parse_args()

        for book in books:
            if(category == article["category"]):
                return "category  {} already exists".format(category), 400

        book = {
            "category": category,
            "ISBN": args["ISBN"],
            "title": args["title"]
        }
        books.append(book)
        return book, 201

    def put(self, category):
        parser = RequestParser()
        parser.add_argument("ISBN")
        parser.add_argument("title")
        args = parser.parse_args()

        for book in books:
            if(category == article["category"]):
                article["ISBN"] = args["ISBN"]
                article["title"] = args["title"]
                return book, 200

        book = {
            "category": category,
            "ISBN": args["ISBN"],
            "title": args["title"]
        }
        books.append(book)
        return book, 201

    def delete(self, category):
        global books
        books = [book for book in books if book["category"] != category]
        return "{} is deleted.".format(category), 200

api.add_resource(Article, "/category/<string:category>")

fk.run(debug=True,port=8080)
```

Client Side:
```python
import requests

headers = {
    'content-type': "application/json",
    'x-apikey': "560bd47058e7ab1b2648f4e7",
    'cache-control': "no-cache"
    }

def get():
    url = "https://www.domian.com/rest/books/category"
    response = requests.request("GET", url, headers=headers)
    print(response.text)

def post():
    url = "https://www.domian.com/rest/books/category"
    payload = json.dumps( {"category": "xyz","ISBN": "abcxyz" ,title:"Test for posting"} )
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

def put():
    url = "https://www.domian.com/rest/books/category/560bd66201e7ab1b2648f4e7"
    payload = "{\"ISBN\":\"abcxyz007\"}"
    response = requests.request("PUT", url, data=payload, headers=headers)
    print(response.text)

def del():
    url = "https://www.domian.com/rest/books/category/560bd66201e7ab1b2648f4e7"
    response = requests.request("DELETE", url, headers=headers)
    print(response.text)
```                    
                    

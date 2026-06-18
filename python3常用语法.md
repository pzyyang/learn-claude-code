# Python 3 常用语法速查（面向 Java 开发者）

> 以 Java 为参照，快速掌握 Python 3 常用语法。重点关注两者差异。

---

## 目录

1. [基本语法差异](#1-基本语法差异)
2. [变量与类型系统](#2-变量与类型系统)
3. [字符串操作](#3-字符串操作)
4. [集合类型](#4-集合类型)
5. [控制流](#5-控制流)
6. [函数](#6-函数)
7. [类与面向对象](#7-类与面向对象)
8. [文件操作](#8-文件操作)
9. [异常处理](#9-异常处理)
10. [导入系统](#10-导入系统)
11. [常用内置函数](#11-常用内置函数)
12. [推导式](#12-推导式)
13. [装饰器](#13-装饰器)
14. [上下文管理器](#14-上下文管理器)
15. [生成器与迭代器](#15-生成器与迭代器)
16. [并发编程](#16-并发编程)
17. [类型注解进阶](#17-类型注解进阶)
18. [常用标准库速查](#18-常用标准库速查)
19. [Python vs Java 对照表](#19-python-vs-java-对照表)

---

## 1. 基本语法差异

### 代码块：缩进代替大括号

```python
# Python: 缩进定义代码块（通常4个空格）
def greet(name):
    if name:
        print(f"Hello, {name}")  # 缩进表示属于 if 块
    else:
        print("Hello, World")
# Java: 大括号定义代码块
# void greet(String name) {
#     if (name != null) {
#         System.out.println("Hello, " + name);
#     } else {
#         System.out.println("Hello, World");
#     }
# }
```

### 语句结束：不需要分号

```python
x = 1        # Python: 不需要分号
y = 2        # 换行即语句结束
x = 1; y = 2 # 同行多条语句用分号分隔（不推荐）
# Java: int x = 1;
#       int y = 2;
```

### 注释

```python
# 单行注释（Java: // 单行注释）

"""
多行注释（文档字符串）
可作为模块/类/函数的文档
相当于 Java 的 /** ... */ Javadoc
"""
```

---

## 2. 变量与类型系统

### 动态类型（Duck Typing）

```python
# Python: 变量没有固定类型，运行时确定（"鸭子类型"）
x = 1           # x 现在是 int
x = "hello"     # x 现在是 str，合法！
x = [1, 2, 3]   # x 现在是 list
# Java: int x = 1;
#       x = "hello";  // 编译错误！Java 是静态类型

# 检查类型（相当于 Java 的 instanceof）
if isinstance(x, list):
    print("x 是列表")

if isinstance(x, (int, float)):  # 可以检查多个类型
    print("x 是数字")
```

### 类型注解（Type Hints，Python 3.5+）

```python
# 类型注解是可选的，运行时不做类型检查（需要 mypy 等工具做静态检查）
name: str = "Alice"                        # Java: String name = "Alice";
age: int = 30                              # Java: int age = 30;
scores: list[int] = [90, 85, 92]           # Java: List<Integer> scores = Arrays.asList(90, 85, 92);
config: dict[str, str] = {"key": "value"}   # Java: Map<String, String> config = Map.of("key", "value");

# 可选类型（相当于 Java 的 Optional / @Nullable）
from typing import Optional
result: Optional[str] = None               # Java: Optional<String> result = Optional.empty();
# Python 3.10+ 简写：
result: str | None = None                  # 更推荐
```

### None vs null

```python
# Python 的 None（相当于 Java 的 null）
x = None                    # Java: Object x = null;
if x is None:               # 检查 None 用 is，不用 ==
    print("x is None")
if x is not None:           # Java: if (x != null)
    print("x is not None")
```

### 基本类型

```python
# 数字
i: int = 42                # 整数（任意精度，无 long/int 之分）
f: float = 3.14            # 浮点数（双精度，相当于 Java double）
b: bool = True             # 布尔值（首字母大写！相当于 Java boolean）
c: complex = 1 + 2j        # 复数（Java 没有内置复数类型）

# Python 没有 char 类型，单个字符也是 str
ch = 'a'                   # 这实际上是长度为 1 的 str
```

### 变量作用域

```python
# 函数内要修改外部变量需声明 global
count = 0                  # 模块级变量（相当于 Java static 字段）

def increment():
    global count           # 声明要修改的是外部变量（无此声明则创建局部变量）
    count += 1

# 闭包中修改外层变量用 nonlocal
def outer():
    x = 0
    def inner():
        nonlocal x         # 声明要修改外层函数变量
        x += 1
    return inner
```

---

## 3. 字符串操作

### 字符串定义

```python
# 单引号或双引号均可（和 JavaScript 类似）
s1 = 'hello'
s2 = "hello"

# 多行字符串（相当于 Java 15+ Text Block: """..."""）
s3 = """第一行
第二行
第三行"""

# f-string 格式化（Python 3.6+，推荐！）
name = "Alice"
age = 30
msg = f"Hello, {name}. You are {age} years old."   # Java: String.format() 或 "Hello, " + name
msg = f"明年 {age + 1} 岁"                           # 可以在 {} 里写表达式
msg = f"{name=}"                                     # 输出: name='Alice'（调试用）

# 其他格式化方式
msg = "Hello, {}. You are {} years old.".format(name, age)   # str.format()
msg = "Hello, %s. You are %d years old." % (name, age)        # 旧式 % 格式化
```

### 常用字符串方法

```python
s = "  Hello, World  "

s.strip()           # "Hello, World"  — 去首尾空白（Java: trim()）
s.upper()           # "  HELLO, WORLD  " — 全大写（Java: toUpperCase()）
s.lower()           # "  hello, world  " — 全小写（Java: toLowerCase()）
s.replace("Hello", "Hi")  # "  Hi, World  " — 替换（Java: replace()）
s.split(",")        # ["  Hello", " World  "] — 分割（Java: split()）
s.startswith("  He")  # True — 前缀判断（Java: startsWith()）
s.endswith("d  ")   # True — 后缀判断（Java: endsWith()）
s.find("World")     # 9 — 查找子串位置（Java: indexOf()），找不到返回 -1
s.count("l")        # 3 — 统计出现次数
",".join(["a", "b", "c"])  # "a,b,c" — 连接（Java: String.join()）

# 切片（Python 独有特性，极其强大）
s = "0123456789"
s[0:5]      # "01234" — 从索引0到4（不含5）
s[:5]       # "01234" — 从开头到4
s[5:]       # "56789" — 从5到末尾
s[-3:]      # "789"  — 最后3个字符
s[::2]      # "02468" — 每隔2个字符
s[::-1]     # "9876543210" — 反转字符串！
```

---

## 4. 集合类型

### 列表 List（相当于 Java ArrayList）

```python
# 创建
lst = [1, 2, 3, 4, 5]          # Java: new ArrayList<>(Arrays.asList(1, 2, 3, 4, 5))
lst = list(range(5))            # [0, 1, 2, 3, 4]  — range 生成序列
lst = [0] * 5                   # [0, 0, 0, 0, 0]  — 重复元素

# 访问和切片
lst[0]                          # 1 — 索引（Java: list.get(0)）
lst[-1]                         # 5 — 倒数第一个
lst[1:4]                        # [2, 3, 4] — 切片（Java: subList(1, 4)）
lst[::2]                        # [1, 3, 5] — 步进切片

# 修改
lst.append(6)                   # [1, 2, 3, 4, 5, 6] — 末尾添加（Java: add()）
lst.insert(0, 0)                # [0, 1, 2, 3, 4, 5, 6] — 指定位置插入
lst.extend([7, 8])              # — 合并另一个列表（Java: addAll()）
lst.remove(3)                   # — 按值删除（Java: remove(Object)）
popped = lst.pop()              # — 弹出末尾（Java: remove(size()-1)）
popped = lst.pop(0)             # — 弹出索引0
del lst[0]                      # — 按索引删除

# 查找
len(lst)                        # 长度（Java: size()）
3 in lst                        # 是否存在（Java: contains()）
lst.index(3)                    # 索引位置（Java: indexOf()）
lst.count(3)                    # 出现次数

# 排序
lst.sort()                      # 原地排序（Java: Collections.sort()）
lst.sort(reverse=True)          # 降序
sorted_lst = sorted(lst)        # 返回新列表，不修改原列表
sorted_lst = sorted(lst, key=lambda x: x.age)  # 自定义排序键
```

### 元组 Tuple（不可变序列）

```python
# 创建 — 元组创建后不可修改
t = (1, 2, 3)                   # EP: (1, 2, 3)，可省略括号
t = 1, 2, 3                     # 一样
t = (1,)                        # 单元素元组必须有逗号！
x, y, z = t                     # 解包赋值（unpacking）

# 常用于多返回值
def get_coordinates():
    return 10, 20               # 返回元组 (10, 20)

x, y = get_coordinates()        # x=10, y=20
```

### 字典 Dict（相当于 Java HashMap）

```python
# 创建
d = {"name": "Alice", "age": 30}                    # Java: Map.of("name", "Alice", "age", 30)
d = dict(name="Alice", age=30)                       # 另一种创建方式
d = {k: v for k, v in [("a", 1), ("b", 2)]}         # 字典推导式

# 访问和修改
d["name"]                     # "Alice" — 取值，key 不存在会报 KeyError
d.get("name")                 # "Alice" — 安全取值（Java: getOrDefault()）
d.get("email", "unknown")     # "unknown" — 提供默认值
d["email"] = "a@b.com"       # 设置值（Java: put()）
d.setdefault("count", 0)     # 如果 key 不存在则设置默认值
del d["count"]                # 删除 key
d.pop("name")                 # 删除并返回值
d.update({"city": "NY"})     # 合并另一个 dict（Java: putAll()）

# 遍历
for key in d:                          # 遍历 key（Java: keySet()）
    print(key, d[key])

for key, value in d.items():           # 遍历 key, value（Java: entrySet()）
    print(key, value)

for value in d.values():               # 遍历 value（Java: values()）
    print(value)

# 合并字典（Python 3.9+）
d1 = {"a": 1}
d2 = {"b": 2}
merged = d1 | d2                       # {"a": 1, "b": 2}（Java 无对应简洁语法）
d1 |= d2                               # d1 现在是 {"a": 1, "b": 2}
```

### 集合 Set（相当于 Java HashSet）

```python
# 创建
s = {1, 2, 3}                            # 集合字面量（Java 10+: Set.of(1,2,3)）
s = set([1, 2, 2, 3])                    # {1, 2, 3} — 自动去重
empty = set()                            # 空集合（不能用 {}，那是空 dict！）

# 操作
s.add(4)                                 # 添加（Java: add()）
s.remove(2)                              # 删除，不存在报错
s.discard(2)                             # 安全删除，不存在不报错
3 in s                                   # 是否存在（Java: contains()）

# 集合运算
a = {1, 2, 3}
b = {2, 3, 4}
a | b        # {1, 2, 3, 4} — 并集（Java: Sets.union()）
a & b        # {2, 3}       — 交集（Java: Sets.intersection()）
a - b        # {1}          — 差集
a ^ b        # {1, 4}       — 对称差
```

---

## 5. 控制流

### 条件判断

```python
if condition:
    do_something()
elif other_condition:         # Python 用 elif，Java 用 else if
    do_other()
else:
    do_default()

# Python 没有 switch-case（Python 3.10 引入了 match-case）
match value:
    case 1:
        print("one")
    case 2 | 3:               # 匹配多个值
        print("two or three")
    case _:                   # 默认匹配（相当于 Java default）
        print("other")
```

### 循环

```python
# for 循环（Python 的 for 等同于 Java 的 for-each）
for item in [1, 2, 3]:                        # Java: for (int item : Arrays.asList(1,2,3))
    print(item)

for i in range(5):                            # 0, 1, 2, 3, 4（Java: for (int i=0; i<5; i++)）
    print(i)

for i in range(2, 10, 2):                     # 2, 4, 6, 8（start, stop, step）
    print(i)

for index, item in enumerate(lst):             # 同时获取索引和值
    print(f"{index}: {item}")

for key, value in dict.items():               # 遍历字典
    print(f"{key}: {value}")

# while 循环（和 Java 一样）
while condition:
    do_something()

# break / continue（和 Java 一样）
for item in lst:
    if condition:
        break       # 跳出循环
    if skip:
        continue    # 跳过本次迭代

# for-else / while-else（Python 独有：循环正常结束执行 else）
for item in lst:
    if found:
        break
else:                           # 如果循环没有被 break 中断则执行
    print("未找到")
```

### 真值判断

```python
# Python 中以下值被视为 False（"假值" / "Falsy"）
# None, False, 0, 0.0, "", [], {}, set(), ()
# 其他值都为 True

if lst:          # 列表非空（Java: if (list != null && !list.isEmpty())）
    process(lst)

if not s:        # 空字符串
    print("empty")

# 三元运算符
value = a if condition else b    # Java: value = condition ? a : b;
```

---

## 6. 函数

### 函数定义

```python
# 基本定义
def add(a: int, b: int) -> int:        # Java: int add(int a, int b)
    """两数相加（docstring，相当于 Javadoc）"""
    return a + b

# 多返回值（实际上返回元组）
def min_max(lst: list[int]) -> tuple[int, int]:   # Java 需要定义 Pair 类或返回数组
    return min(lst), max(lst)

# 默认参数（Java 需要方法重载实现）
def greet(name: str = "World") -> str:
    return f"Hello, {name}"

greet()             # "Hello, World"
greet("Alice")      # "Hello, Alice"

# 关键字参数 — 调用时可以指定参数名（Java 无此特性）
def create_user(name: str, age: int, email: str = ""):
    pass

create_user(age=30, name="Bob", email="bob@test.com")  # 可以按任意顺序传参
```

### 可变参数（*args / **kwargs）

```python
# *args: 接收任意数量的位置参数（打包为 tuple）
def sum_all(*args: int) -> int:  # Java: int sumAll(int... args)
    return sum(args)

sum_all(1, 2, 3, 4, 5)  # 15

# **kwargs: 接收任意数量的关键字参数（打包为 dict）
def build_config(**kwargs):  # Java: 通常传 Map
    return kwargs

build_config(host="localhost", port=8080, debug=True)
# {"host": "localhost", "port": 8080, "debug": True}

# 解包运算符（函数调用时使用）
vals = [1, 2, 3]
sum_all(*vals)              # * 解包列表为位置参数

config = {"host": "x", "port": 80}
build_config(**config)      # ** 解包字典为关键字参数
```

### lambda 匿名函数（相当于 Java 箭头函数）

```python
# lambda 参数: 返回值（只能写单行表达式）
add = lambda a, b: a + b               # Java: (a, b) -> a + b
square = lambda x: x ** 2              # Java: x -> x * x

# 常用作回调
lst.sort(key=lambda x: x.name)         # 自定义排序键
filtered = list(filter(lambda x: x > 0, lst))  # 过滤
mapped = list(map(lambda x: x * 2, lst))       # 映射
```

---

## 7. 类与面向对象

### 类定义

```python
class Animal:                                        # Java: class Animal
    """动物基类"""

    # 类变量（相当于 Java static 字段）
    species_count: int = 0

    # 构造函数（相当于 Java 的 constructor，__init__ 不是构造器而是初始化器）
    def __init__(self, name: str, age: int = 0):
        # self = 实例本身（相当于 Java 的 this，但必须显式声明为第一个参数）
        self.name = name              # 实例变量（不需要事先声明）
        self._age = age               # _ 前缀表示"受保护"（约定，非强制）
        self.__secret = None          # __ 前缀会触发名称改写（name mangling）
        Animal.species_count += 1     # 访问类变量

    # 实例方法
    def speak(self) -> str:            # Java: public String speak()
        return f"{self.name} says..."

    # 属性（Property）— 相当于 Java 的 getter/setter，但调用时像访问字段
    @property
    def age(self) -> int:
        """年龄 getter（调用: obj.age 而不是 obj.age()）"""
        return self._age

    @age.setter
    def age(self, value: int):
        """年龄 setter（调用: obj.age = 5 而不是 obj.setAge(5)）"""
        if value < 0:
            raise ValueError("年龄不能为负数")
        self._age = value

    # 魔术方法（magic methods）— 运算符重载 / 特殊行为
    def __str__(self) -> str:           # 相当于 Java 的 toString()
        return f"Animal({self.name})"

    def __repr__(self) -> str:          # 调试用字符串表示
        return f"Animal(name={self.name!r}, age={self._age!r})"

    def __eq__(self, other) -> bool:    # 相当于 Java 的 equals()
        if not isinstance(other, Animal):
            return False
        return self.name == other.name

    def __lt__(self, other) -> bool:    # 相当于 Java 的 compareTo()（用于排序）
        return self._age < other._age

    # 类方法（相当于 Java 的 static 方法）
    @classmethod
    def get_count(cls) -> int:          # cls = 类本身（类似 Java Class<T> 对象）
        return cls.species_count

    # 静态方法（不需要访问类或实例）
    @staticmethod
    def is_animal(name: str) -> bool:  # Java: public static boolean isAnimal(String name)
        return bool(name)
```

### 继承

```python
class Dog(Animal):                     # Java: class Dog extends Animal
    """狗，继承自动物"""

    def __init__(self, name: str, breed: str = "混血"):
        super().__init__(name)          # 调用父类构造器（Java: super(name)）
        self.breed = breed

    def speak(self) -> str:             # 重写（Java: @Override public String speak()）
        return f"{self.name} says: Woof!"
```

### 多继承（Java 没有，Java 用 interface）

```python
class Flyable:
    def fly(self):
        return "flying"

class Swimmable:
    def swim(self):
        return "swimming"

class Duck(Animal, Flyable, Swimmable):  # 多继承！（Java 做不到）
    pass
```

### 抽象类（ABC）

```python
from abc import ABC, abstractmethod

class Shape(ABC):                             # Java: abstract class Shape
    @abstractmethod                            # Java: public abstract double area();
    def area(self) -> float:
        pass                                  # 抽象方法体为空
```

### Dataclass（类似 Java record / Lombok @Data）

```python
from dataclasses import dataclass, field

@dataclass                             # 装饰器：自动生成 __init__/__repr__/__eq__
class User:
    name: str
    age: int
    email: str = ""                   # 带默认值的字段必须在最后
    tags: list[str] = field(default_factory=list)  # 可变默认值必须用 default_factory

# 使用
user = User(name="Alice", age=30)
print(user)                           # User(name='Alice', age=30, email='', tags=[])
```

---

## 8. 文件操作

### 路径操作（pathlib，推荐）

```python
from pathlib import Path

# 创建路径（相当于 Java 的 java.nio.file.Path）
p = Path("/Users/me/file.txt")       # Java: Path.of("/Users/me/file.txt")
p = Path.cwd() / "subdir" / "file"   # / 运算符连接路径！
home = Path.home()                    # 用户目录

# 路径信息
p.name                                # "file.txt" — 文件名
p.stem                                # "file" — 不含后缀
p.suffix                              # ".txt" — 后缀
p.parent                              # Path("/Users/me") — 父目录
p.parts                               # ("/", "Users", "me", "file.txt") — 分段

# 文件读写（一行搞定）
content = p.read_text()               # 读全部文本（Java: Files.readString()）
content = p.read_text(encoding="utf-8")
p.write_text("Hello, World!")         # 写文本（Java: Files.writeString()）
lines = p.read_text().splitlines()    # 读所有行（Java: Files.readAllLines()）

# 目录操作
p.mkdir()                             # 创建目录（父目录不存在报错）
p.mkdir(parents=True, exist_ok=True)  # 递归创建，已存在不报错

# 遍历目录
for child in p.iterdir():             # 遍历直接子项
    print(child)

for f in p.glob("*.py"):              # glob 模式匹配
    print(f)

for f in p.rglob("**/*.txt"):         # 递归 glob
    print(f)

# 判断
p.exists()                            # 是否存在
p.is_file()                           # 是否为文件
p.is_dir()                            # 是否为目录

# 解析
p.resolve()                           # 绝对路径（解析符号链接）
p.is_relative_to(Path.cwd())          # 是否在工作目录下（安全检查用）
```

### 传统 open() 方式

```python
# 推荐：使用 with 确保文件自动关闭（相当于 Java try-with-resources）
with open("file.txt", "r") as f:
    content = f.read()                # 读取全部
    # 自动关闭，不需要 f.close()

with open("file.txt", "w") as f:
    f.write("Hello")                  # 写入（覆盖模式）

with open("file.txt", "a") as f:
    f.write("append line\n")          # 追加模式

# 模式："r" 读, "w" 写（覆盖）, "a" 追加, "rb" 二进制读, "wb" 二进制写
```

---

## 9. 异常处理

```python
# 基本结构（try-except-finally，类似 Java try-catch-finally）
try:
    result = risky_operation()
    file = open("data.txt")
except FileNotFoundError as e:               # Java: catch (FileNotFoundException e)
    print(f"文件未找到: {e}")
except (ValueError, TypeError) as e:         # 捕获多种异常
    print(f"值或类型错误: {e}")
except Exception as e:                       # 捕获所有异常（Java: catch (Exception e)）
    print(f"未知错误: {type(e).__name__}: {e}")
    raise                                    # 重新抛出（Java: throw e）
else:                                        # Python 特有：无异常时执行
    print("操作成功")
finally:                                     # 总是执行（和 Java 一样）
    file.close()

# 自定义异常
class MyError(Exception):                    # Java: class MyError extends Exception
    pass

raise MyError("something went wrong")        # Java: throw new MyError("...")
```

---

## 10. 导入系统

```python
# 基本导入
import os                                    # 导入整个模块（Java: 同名包下的类自动可见）
from pathlib import Path                     # 导入特定类/函数
from pathlib import Path, PurePath           # 导入多个
from anthropic import Anthropic              # 第三方库

# 别名
import numpy as np                           # Java: 无直接对应，类似 import fully.qualified 然后自己缩略
from datetime import datetime as dt

# 相对导入（包内使用）
from . import sibling_module                 # 同级模块
from ..parent_package import something       # 上级模块

# 条件导入
try:
    import readline                          # 可选依赖
except ImportError:
    pass                                     # 没有也不报错

# 导入所有（不推荐）
from module import *                         # 把 module 的所有公共名称导入当前命名空间
```

---

## 11. 常用内置函数

```python
# 类型转换
int("42")                                    # Java: Integer.parseInt("42")
float("3.14")                                # Java: Double.parseDouble("3.14")
str(42)                                      # Java: String.valueOf(42)
bool(1)                                      # True（非空即有值即为 True）
list("abc")                                  # ['a', 'b', 'c']
tuple([1, 2, 3])                             # (1, 2, 3)
dict([("a", 1), ("b", 2)])                   # {'a': 1, 'b': 2}
set([1, 2, 2, 3])                            # {1, 2, 3}
bytes("hello", "utf-8")                      # 字符串转字节

# 序列操作
len(lst)                                     # 长度（Java: size() / length）
max(lst)                                     # 最大值
min(lst)                                     # 最小值
sum(lst)                                     # 求和
sorted(lst)                                  # 排序（返回新列表）
reversed(lst)                                # 反转（返回迭代器）
enumerate(lst)                               # (index, value) 对
zip(lst1, lst2)                              # 打包两个列表
range(start, stop, step)                     # 数字序列

# 过滤/映射
filter(lambda x: x > 0, lst)                 # 过滤（Java: Stream.filter）
map(lambda x: x * 2, lst)                    # 映射（Java: Stream.map）

# 判断
all(condition(x) for x in lst)               # 全满足？（Java: Stream.allMatch）
any(condition(x) for x in lst)               # 任一满足？（Java: Stream.anyMatch）
isinstance(obj, SomeClass)                   # Java: obj instanceof SomeClass
issubclass(Dog, Animal)                      # Java: Animal.class.isAssignableFrom(Dog.class)
hasattr(obj, "name")                         # 是否有某属性（反射）
getattr(obj, "name", default)                # 获取属性（反射）
callable(obj)                                # 是否可调用

# 输入输出
print("Hello", end="")                       # 不换行输出
name = input("Enter name: ")                 # Java: Scanner.nextLine()
```

---

## 12. 推导式

```python
# 列表推导式（最常用，相当于 Java Stream map/filter/collect）
squares = [x**2 for x in range(10)]                         # [0, 1, 4, 9, ...81]
evens = [x for x in range(20) if x % 2 == 0]                # 带过滤
labels = [f"item_{i}" for i in range(5)]                    # 带变换
# Java: IntStream.range(0, 10).map(x -> x*x).boxed().toList()

# 嵌套推导式
matrix = [[i * j for j in range(3)] for i in range(3)]
# [[0, 0, 0], [0, 1, 2], [0, 2, 4]]

# 字典推导式
squares_map = {x: x**2 for x in range(5)}                   # {0:0, 1:1, 2:4, 3:9, 4:16}
# Java: IntStream.range(0, 5).boxed().collect(toMap(x->x, x->x*x))

# 集合推导式
unique_lengths = {len(word) for word in words}              # 去重

# 生成器表达式（懒加载，节省内存）
sum(x**2 for x in range(1000000))        # 不需要创建 100 万元素的列表！
```

---

## 13. 装饰器

```python
# 装饰器 = 包装函数的函数（类似 Java 的 AOP 或 @Annotation + Proxy）

# 使用内置装饰器
@staticmethod                                       # 静态方法（不需要 self/cls）
@classmethod                                        # 类方法（需要 cls）
@property                                           # 属性 getter（obj.x 而非 obj.x()）
@abstractmethod                                     # 抽象方法

# 自定义装饰器
def log(func):
    """记录函数调用的装饰器"""
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"返回 {result}")
        return result
    return wrapper

@log                                                # 使用装饰器
def add(a, b):
    return a + b

add(1, 2)                                           # 自动打印日志
# 等价于：add = log(add)

# 带参数的装饰器（三层嵌套）
def repeat(n: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def hello():
    print("Hello")

hello()                                             # 打印三次 Hello
```

---

## 14. 上下文管理器

```python
# with 语句 = Java try-with-resources（自动管理资源生命周期）

# 文件操作（最常用）
with open("file.txt") as f:
    content = f.read()
# f 自动关闭，即使发生异常也会关闭

# 线程锁
import threading
lock = threading.Lock()

with lock:                    # 等价于 lock.acquire(); ...; lock.release()
    shared_data += 1

# 自定义上下文管理器
class MyContext:
    def __enter__(self):
        print("进入上下文")     # 相当于 Java try-with 的初始化
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("退出上下文")     # 相当于 Java try-with 的 finally

with MyContext() as ctx:
    print("执行操作")
# 输出：进入上下文 / 执行操作 / 退出上下文

# 用 contextlib 创建（更简洁）
from contextlib import contextmanager

@contextmanager
def my_context():
    print("setup")
    yield                                   # 在这里暂停，执行 with 块
    print("teardown")

with my_context():
    print("work")
```

---

## 15. 生成器与迭代器

```python
# 生成器函数（使用 yield 而非 return）
def countdown(n: int):
    """倒计时生成器"""
    while n > 0:
        yield n                              # 暂停并产生值（Java 无直接对应）
        n -= 1

for num in countdown(5):                     # 5, 4, 3, 2, 1
    print(num)

# 生成器表达式（懒加载列表推导式）
squares = (x**2 for x in range(10))          # 注意 () 而不是 []
# squares 是一个生成器对象，值按需产生

# 转列表
list(squares)                                # 立即求值所有结果

# 迭代器协议
class MyIterator:
    def __iter__(self):
        self.current = 0
        return self                          # 实现 __iter__ 即可用 for 遍历

    def __next__(self):                      # 类似 Java 的 Iterator.next()
        self.current += 1
        return self.current
```

---

## 16. 并发编程

### 线程（threading）

```python
import threading
import time

# 创建线程（类似 Java 的 Thread）
def worker(name: str):
    print(f"{name} 开始工作")
    time.sleep(1)
    print(f"{name} 完成")

t = threading.Thread(target=worker, args=("Alice",), daemon=True)
t.start()                                    # Java: thread.start()
t.join()                                     # Java: thread.join() — 等待结束

# 互斥锁（类似 Java 的 synchronized / ReentrantLock）
lock = threading.Lock()

with lock:                                   # 自动 acquire/release
    # 临界区
    pass
```

### 子进程（subprocess）

```python
import subprocess

# 执行命令并等待完成（类似 Java 的 ProcessBuilder / Runtime.exec()）
result = subprocess.run(
    ["ls", "-la"],                          # 命令和参数
    capture_output=True,                    # 捕获 stdout/stderr（Java: redirectOutput）
    text=True,                              # 返回字符串而非 bytes
    timeout=120,                            # 超时秒数
    cwd="/path/to/dir",                     # 工作目录
    shell=False,                            # 是否通过 shell 执行
)

result.returncode                           # 退出码（Java: Process.exitValue()）
result.stdout                               # 标准输出（Java: process.getInputStream()）
result.stderr                               # 标准错误（Java: process.getErrorStream()）
```

---

## 17. 类型注解进阶

```python
from typing import Optional, Union, Callable, Any, Literal

# 基本类型（Python 3.10+）
name: str                                   # Java: String
age: int                                    # Java: int / Integer
price: float                                # Java: double / Double
active: bool                                # Java: boolean / Boolean
data: bytes                                 # Java: byte[]

# 集合类型（Python 3.9+ 直接用内置类型，不再需要 typing.List 等）
names: list[str]                            # Java: List<String>
scores: list[int]
config: dict[str, str]                      # Java: Map<String, String>
ids: set[int]                               # Java: Set<Integer>
pair: tuple[str, int]                       # Java: 无直接对应

# 可选类型
email: str | None = None                    # Java: Optional<String>
# 等价于 Optional[str]（Python 3.10+ 推荐 | None 写法）

# 联合类型
value: str | int                            # Java: 需要定义联合类型或用 Object
response: int | str | None                  # 可以是 int、str 或 None

# 函数类型
handler: Callable[[int, str], bool]         # 接收 int 和 str，返回 bool
                                            # Java: BiFunction<Integer, String, Boolean>

# 任意类型
anything: Any                               # Java: Object（关闭类型检查）

# 字面量类型
mode: Literal["read", "write"]              # 只能是这两个值
                                            # Java: 用 enum 实现
```

---

## 18. 常用标准库速查

| Python 模块 | 用途 | Java 对应 |
|---|---|---|
| `os` | 操作系统接口（环境变量、进程） | `java.lang.System` / `java.lang.Process` |
| `pathlib` | 现代文件路径操作 | `java.nio.file.Path` / `Files` |
| `subprocess` | 执行外部命令 | `java.lang.ProcessBuilder` |
| `json` | JSON 序列化/反序列化 | Jackson / Gson |
| `re` | 正则表达式 | `java.util.regex` |
| `datetime` | 日期时间 | `java.time` |
| `threading` | 线程 | `java.lang.Thread` / `java.util.concurrent` |
| `argparse` | 命令行参数解析 | args4j / JCommander |
| `logging` | 日志 | SLF4J / Log4j |
| `unittest` | 单元测试 | JUnit |
| `pytest` (第三方) | 更简洁的测试框架 | JUnit 5 + AssertJ |
| `dataclasses` | 自动生成数据类方法 | Lombok @Data / Record |
| `abc` | 抽象基类 | `abstract class` / `interface` |
| `collections` | 高级集合（deque, Counter, defaultdict） | Guava |
| `functools` | 高阶函数工具（partial, reduce, lru_cache） | Java 无直接对应 |
| `itertools` | 迭代器工具（chain, product, permutations） | Java 无直接对应 |
| `typing` | 类型注解工具 | 无（Java 类型内置在语言中） |
| `sys` | 系统参数（argv, exit, path） | `System` 类相关方法 |

---

## 19. Python vs Java 对照表

| 概念 | Python | Java |
|---|---|---|
| 程序入口 | `if __name__ == "__main__":` | `public static void main(String[] args)` |
| 类型系统 | 动态类型（运行时） | 静态类型（编译时） |
| 空值 | `None` | `null` |
| 字符串 | `"hello"` 或 `'hello'` | `"hello"`（双引号必须） |
| 布尔 | `True` / `False` | `true` / `false` |
| 数组/列表 | `[1, 2, 3]`（List） | `new int[]{1, 2, 3}` 或 `List.of(1, 2, 3)` |
| 字典/Map | `{"key": "value"}` | `Map.of("key", "value")` |
| 方法 | `def func(self, arg):` | `ReturnType method(ArgType arg)` |
| this | `self`（显式参数） | `this`（隐式可用） |
| 构造器 | `__init__(self)` | 与类同名的构造方法 |
| toString | `__str__(self)` | `toString()` |
| equals | `__eq__(self, other)` | `equals(Object other)` |
| hashCode | `__hash__(self)` | `hashCode()` |
| 继承 | `class Dog(Animal):` | `class Dog extends Animal` |
| 接口 | 鸭子类型 / ABC / Protocol | `interface` + `implements` |
| 抽象类 | `class Shape(ABC):` + `@abstractmethod` | `abstract class Shape` |
| 包/模块 | `import module` / `from pkg import X` | `package com.xxx; import ...;` |
| 访问控制 | `_name`（约定），`__name`（改写） | `private` / `protected` / `public` |
| 代码块 | 缩进 | `{ }` |
| 条件 | `if/elif/else` | `if/else if/else` |
| 三元运算 | `a if cond else b` | `cond ? a : b` |
| for | `for item in iterable:` | `for (T item : iterable)` |
| switch | `match value: case pattern:`（3.10+） | `switch(value) { case ... }` |
| 异常 | `try/except/finally` | `try/catch/finally` |
| 抛出异常 | `raise Error("msg")` | `throw new Error("msg")` |
| 资源管理 | `with expr as var:` | `try (var = expr) { ... }` |
| 泛型 | 类型注解（不强制，运行时擦除） | 泛型（编译时检查，运行时擦除） |
| final | 约定大写字母命名常量 | `final` 关键字 |
| 注解 | 装饰器 `@decorator` | `@Annotation` |
| 多返回值 | 自动打包为元组 | 需要包装类 |
| 运算符重载 | `__add__` / `__sub__` 等 | 不支持 |

---

## 参考资料

- [Python 官方文档 (中文)](https://docs.python.org/zh-cn/3/)
- [Python 官方教程](https://docs.python.org/zh-cn/3/tutorial/)
- [Real Python](https://realpython.com/) — 大量实战教程

---

> **提示**：这份文档侧重 Python 与 Java 的差异。建议配合本项目代码阅读，遇到不理解的 Python 语法随时回来查阅。

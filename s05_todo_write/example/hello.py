# 最简 Python 示例：函数定义 + 调用
# def 定义函数（类似 Java 的方法定义）
# 注意 Python 不需要声明参数类型、返回类型，也用大括号，全靠缩进
def greet(name):
    message = "Hello, " + name  # 字符串拼接用 +（和 Java 一样）
    print(message)  # print() 输出到控制台（类似 Java System.out.println()）


greet("Claude")  # 直接调用函数，不需要类包裹（Python 支持顶层函数）

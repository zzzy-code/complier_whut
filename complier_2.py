import re

# 词法分析，将代码字符串拆分成Token序列
def tokenize(code):
    token_spec = [
        ("NUMBER", r'\d+(\.\d*)?'),  # 数字（整数或小数）
        ("IDENTIFIER", r'[a-zA-Z_]\w*'),  # 标识符
        ("EQUAL", r'='),  # 赋值符号
        ("PLUS", r'\+'),  # 加法运算符
        ("MINUS", r'-'),  # 减法运算符
        ("TIMES", r'\*'),  # 乘法运算符
        ("DIVIDE", r'/'),  # 除法运算符
        ("LPAREN", r'\('),  # 左括号
        ("RPAREN", r'\)'),  # 右括号
        ("SKIP", r'[ \t]+'),  # 忽略空白符
        ("MISMATCH", r'.'),  # 非法字符
    ]
    token_re = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in token_spec)
    tokens = []
    for match in re.finditer(token_re, code):
        kind = match.lastgroup
        value = match.group()
        if kind == "SKIP":
            continue  # 跳过空白符
        elif kind == "MISMATCH":
            raise SyntaxError(f"发现非法字符: {value} 在位置 {match.start()}")
        else:
            tokens.append((kind, value, match.start()))
    return tokens

# 递归下降语法分析器
class RecursiveDescentParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.output = []  # 存储中间代码

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, token_type):
        current = self.peek()
        if current and current[0] == token_type:
            self.pos += 1
            return current
        else:
            expected = token_type
            actual = current[0] if current else "EOF"
            position = current[2] if current else "未知位置"
            raise SyntaxError(f"语法错误：预期 {expected}，但实际是 {actual}，在位置 {position}")

    def parse(self):
        try:
            self.assign_stmt()  # 从赋值语句开始解析
            if self.pos < len(self.tokens):
                extra_token = self.tokens[self.pos]
                raise SyntaxError(f"在有效语句后存在多余的Token: {extra_token[1]} 在位置 {extra_token[2]}")
            return "语法正确", self.output
        except SyntaxError as e:
            return f"语法错误：{e}", []

    # 解析赋值语句
    def assign_stmt(self):
        identifier = self.consume("IDENTIFIER")[1]  # 消耗标识符
        self.consume("EQUAL")  # 消耗等号
        value = self.expr()  # 解析右侧表达式
        self.output.append(f"{identifier} = {value}")  # 添加中间代码

    # 解析表达式
    def expr(self):
        left = self.term()
        while True:
            current = self.peek()
            if current and current[0] in ("PLUS", "MINUS"):
                op = self.consume(current[0])[1]  # 消耗加减号
                right = self.term()
                temp = f"t{len(self.output) + 1}"  # 创建临时变量
                self.output.append(f"{temp} = {left} {op} {right}")
                left = temp
            else:
                break
        return left

    # 解析项
    def term(self):
        left = self.factor()
        while True:
            current = self.peek()
            if current and current[0] in ("TIMES", "DIVIDE"):
                op = self.consume(current[0])[1]  # 消耗乘除号
                right = self.factor()
                temp = f"t{len(self.output) + 1}"  # 创建临时变量
                self.output.append(f"{temp} = {left} {op} {right}")
                left = temp
            else:
                break
        return left

    # 解析因子
    def factor(self):
        current = self.peek()
        if current[0] == "NUMBER":
            return self.consume("NUMBER")[1]  # 消耗数字
        elif current[0] == "IDENTIFIER":
            return self.consume("IDENTIFIER")[1]  # 消耗标识符
        elif current[0] == "LPAREN":
            self.consume("LPAREN")  # 消耗左括号
            value = self.expr()
            self.consume("RPAREN")  # 消耗右括号
            return value
        else:
            position = current[2] if current else "未知位置"
            raise SyntaxError(f"意外的Token: {current[1]} 在位置 {position}")

# 从控制台读取代码并分析
def analyze_console_input():
    print("请输入代码，输入空行后按回车结束输入：")
    code_lines = []
    
    while True:
        line = input()
        if line.strip() == "":  # 如果输入为空行，则结束输入
            break
        code_lines.append(line)
    
    code = "\n".join(code_lines)  # 将所有输入的行合并为一个代码字符串

    tokens = tokenize(code)  # 词法分析
    parser = RecursiveDescentParser(tokens)  # 初始化语法分析器
    result, output = parser.parse()  # 解析代码
    return result, output

# 示例用法
result, output = analyze_console_input()
print(result)  # 输出语法分析结果
if result == "语法正确":
    print("生成的中间代码如下：")
    for line in output:
        print(line)

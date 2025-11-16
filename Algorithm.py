# 引入copy标准库，后续合一的过程中为了不修改原来的子句，要将原子句深拷贝到新子句中
import copy


# 公式类
class formula:
    def __init__(self, ifnot, predicate, parameter):
        # 是否~,0代表非，1代表正
        self.ifnot = ifnot
        # 谓词（字符串）
        self.predicate = predicate
        # 参数列表（包括变量或者常量）
        self.parameter = parameter

    # 用于打印公示类的函数，返回的是公式的字符串，形如'~On(xx,john)'
    def __repr__(self):
        str_prt = ''
        if self.ifnot == 0:
            str_prt += '~'
        str_prt += self.predicate
        str_prt += '('
        for j in range(len(self.parameter)):
            str_prt += self.parameter[j]
            if j < len(self.parameter) - 1:
                str_prt += ','
        str_prt += ')'
        return str_prt


# 将子句（类型为公式类的列表）转变成元组，再转变成字符串返回
def list_to_str(list0):
    return str(tuple(list0))


# 判断子句list0是否在子句集KB中，避免重复归结（0代表KB中存在list0，1代表KB中不存在list0）
def ifin(list0, KB):
    n = len(KB)
    for i in range(n):
        if KB[i] == list0:
            return 0
    return 1


# 将子句list1和子句list2进行归结
def resolution(list1, list2, list1_index, list2_index, KB, step, result):
    m = len(list1)
    n = len(list2)
    OK = 0  # 是否归结成功
    new_list = []  # 归结后的子句
    # 遍历子句中的各个公式，找到能满足归结条件的两个原子公式
    for i in range(m):
        for j in range(n):
            if list1[i].ifnot != list2[j].ifnot and list1[i].predicate == list2[j].predicate:  # 在满足归结条件的情况下
                if list1[i].parameter == list2[j].parameter:  # 不用进行合一的情况下
                    new_list = list2[:j] + list2[j + 1:] + list1[:i] + list1[i + 1:]  # 去掉两个子句的对应原子并合并
                    if ifin(new_list, KB) == 1:
                        OK = 1
                        addresult = ''  # 字符串形式的下一个归结步骤
                        KB.append(new_list)  # 将合并的新子句加入到子句集中
                        addresult += str(step[0]) + ' '
                        step[0] += 1
                        addresult += 'R[' + str(list1_index)  # 输出合并的原子公式1的标号
                        if m > 1:
                            addresult += str(chr(i + 97))
                        addresult += ',' + str(list2_index)  # 输出合并的原子公式2的标号
                        if n > 1:
                            addresult += str(chr(j + 97))
                        addresult += '] = '
                        addresult += list_to_str(new_list)  # 输出出加入子句集的新子句
                        result.append(addresult)  # 将新的归结步骤加入到归结步骤列表中
                        if new_list == []:  # 产生空子句则返回0，代表归结完成
                            return 0
                else:  # 需要进行合一的情况下
                    z = len(list1[i].parameter)
                    fix_list = []  # 存储合一后的子句
                    for k in range(z):
                        # 由于题目没有明确告诉我变量和常量的格式区别，我根据三个测试输入规定长的是常量，短的是变量，下面分类讨论
                        if len(list1[i].parameter[k]) > len(list2[j].parameter[k]):
                            fix_list = copy.deepcopy(list2)  # 深拷贝合一前的子句
                            # 遍历字句中的所有公式的参数，将该变量替换为常量
                            for t in range(n):
                                for r in range(len(list2[t].parameter)):
                                    if list2[t].parameter[r] == list2[j].parameter[k]:
                                        fix_list[t].parameter[r] = list1[i].parameter[k]
                            new_list = fix_list[:j] + fix_list[j + 1:] + list1[:i] + list1[i + 1:]  # 去掉两个子句的对应原子并合并
                            if ifin(new_list, KB) == 1:
                                OK = 1
                                addresult = ''  # 字符串形式的下一个归结步骤
                                KB.append(new_list)  # 将合并的新子句加入到子句集中
                                addresult += str(step[0]) + ' '
                                step[0] += 1
                                addresult += 'R[' + str(list1_index)  # 输出合并的原子公式1的标号
                                if m > 1:
                                    addresult += str(chr(i + 97))
                                addresult += ',' + str(list2_index)  # 输出合并的原子公式2的标号
                                if n > 1:
                                    addresult += str(chr(j + 97))
                                addresult += ']{' + str(list2[j].parameter[k]) + '=' + str(
                                    list1[i].parameter[k]) + '} = '  # 输出具体的变量和常量
                                addresult += list_to_str(new_list)  # 输出加入子句集的新子句
                                result.append(addresult)  # 将新的归结步骤加入到归结步骤列表中
                                if new_list == []:  # 产生空子句则返回0，代表归结完成
                                    return 0
                        elif len(list2[j].parameter[k]) > len(list1[i].parameter[k]):
                            fix_list = copy.deepcopy(list1)
                            # 遍历字句中的所有公式的参数，将该变量替换为常量
                            for t in range(m):
                                for r in range(len(list1[t].parameter)):
                                    if list1[t].parameter[r] == list1[i].parameter[k]:
                                        fix_list[t].parameter[r] = list2[j].parameter[k]
                            new_list = list2[:j] + list2[j + 1:] + fix_list[:i] + fix_list[i + 1:]  # 去掉两个子句的对应原子并合并
                            if ifin(new_list, KB) == 1:
                                OK = 1
                                addresult = ''  # 字符串形式的下一个归结步骤
                                KB.append(new_list)  # 将合并的新子句加入到子句集中
                                addresult += str(step[0]) + ' '
                                step[0] += 1
                                addresult += 'R[' + str(list1_index)  # 输出合并的原子公式1的标号
                                if m > 1:
                                    addresult += str(chr(i + 97))
                                addresult += ',' + str(list2_index)  # 输出合并的原子公式2的标号
                                if n > 1:
                                    addresult += str(chr(j + 97))
                                addresult += ']{' + str(list1[i].parameter[k]) + '=' + str(
                                    list2[j].parameter[k]) + '} = '  # 输出具体的变量和常量
                                addresult += list_to_str(new_list)  # 打出加入子句集的新子句
                                result.append(addresult)  # 将新的归结步骤加入到归结步骤列表中
                                if new_list == []:  # 产生空子句则返回0，代表归结完成
                                    return 0

    return 1


# 公式字符串转变成公式类
def str_to_class(string):
    n = len(string)
    ifnot = 1
    predicate = ''
    parameter = []
    if string[0] == '~':
        ifnot = 0
    ifname = 0
    begin = 0
    for i in range(n):
        if string[i] == '(':
            ifname = 1
            begin = i + 1
            if ifnot == 1:
                predicate = string[0:i]
            else:
                predicate = string[1:i]
        if ifname == 1:
            if string[i] == ',' or string[i] == ')':
                parameter.append(string[begin:i])
                begin = i + 1
    newclass = formula(ifnot, predicate, parameter)
    return newclass


# 将公式字符串的列表转变成公式类的列表
def to_list_of_class(KB):
    for i in range(len(KB)):
        for j in range(len(KB[i])):
            KB[i][j] = str_to_class(KB[i][j])


# 子句集归结的主函数
def ResolutionFOL(KB):
    # 先将KB的类型从元组的集合转变成嵌套列表
    result = []
    KB = list(KB)
    for i in range(len(KB)):
        KB[i] = list(KB[i])
    to_list_of_class(KB)
    step = [1]  # 每一步的标号
    # 输出初始的所有公式
    for i in range(len(KB)):
        new_step = ''
        new_step += str(step[0]) + ' '
        step[0] += 1
        new_step += list_to_str(KB[i])
        result.append(new_step)
    # 对子句集的每两条子句进行遍历，尝试归结，归结成功则输出归结步骤和新加入子句集的公式（输出由resolution函数完成）
    for k in range(len(KB)):
        for i in range(len(KB)):
            for j in range(i + 1, len(KB)):
                x = resolution(KB[i], KB[j], i + 1, j + 1, KB, step, result)
                if x == 0:
                    return result  # 得到空子句，函数退出


# 示例1
KB1 = {('GradStudent(sue)',), ('~GradStudent(x)', 'Student(x)'), ('~Student(x)', 'HardWorker(x)'),
       ('~HardWorker(sue)',)}
steps1 = ResolutionFOL(KB1)
for i in range(len(steps1)):
    print(steps1[i])

# 示例2
# KB2 = {('A(tony)',), ('A(mike)',), ('A(john)',), ('L(tony,rain)',), ('L(tony,snow)',), ('~A(x)', 'S(x)', 'C(x)'),
#        ('~C(y)', '~L(y,rain)'), ('L(z,snow)', '~S(z)'), ('~L(tony,u)', '~L(mike,u)'), ('L(tony,v)', 'L(mike,v)'),
#        ('~A(w)', '~C(w)', 'S(w)')}
# steps2 = ResolutionFOL(KB2)
# for i in range(len(steps2)):
#     print(steps2[i])

# 示例3
# KB3 = {('On(tony,mike)',), ('On(mike,john)',), ('Green(tony)',), ('~Green(john)',),
#        ('~On(xx,yy)', '~Green(xx)', 'Green(yy)')}
# steps3 = ResolutionFOL(KB3)
# for i in range(len(steps3)):
#     print(steps3[i])

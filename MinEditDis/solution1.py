# 算法逻辑
def editdis(str1, str2):
    # 防止出现空串的情况
    len_str1 = len(str1) + 1
    len_str2 = len(str2) + 1
    # 用一维数组的方式建立一个二维数组,相当于横纵坐标的两个位置在比较
    matrix = [0 for n in range(len_str1 * len_str2)]
    # 前len_str1个位都按顺序赋值
    for i in range(len_str1):
        matrix[i] = i
    # 每len_str1个字符为一组，第一个赋值
    for j in range(0, len(matrix), len_str1):
        # if j % len_str1 == 0:这一步感觉可以省略
        matrix[j] = j;
    for i in range(1, len_str1):
        for j in range(1, len_str2):
            if str1[i-1] == str2[j-1]:
                cost = 0
            else:
                cost = 1
            matrix[j*len_str1+i] = min(matrix[(j-1)*len_str1]+1, matrix[j*len_str1+(i-1)]+1, matrix[(j-1)*len_str1+(i-1)]+cost)
#    print(matrix)
    return matrix[-1]

str1 = 'horse'
str2 = 'ros'
print(editdis(str1, str2))

# dp方法
def minEditDis(str1, str2):
    x = len(str1) + 1
    y = len(str2) + 1
    dis = [[0 for i in range(x)] for j in range(y)]
    for i in range(x):
        dis[0][i] = i
    for j in range(y):
        dis[j][0] = j
    for i in range(1, x):
        for j in range(1, y):
            if str1[i-1] == str2[j-1]:
                dis[i][j] = dis[i-1][j-1]
            else:
                dis[i][j] = min(dis[i-1][j], dis[i][j-1], dis[i-1][j-1]) + 1
    return dis[x-1][y-1]

str1 = 'intention'
str2 = 'execution'
print(minEditDis(str1, str2))

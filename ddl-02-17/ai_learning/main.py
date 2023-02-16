import collections
import numpy as np
import pandas as pd
from random import randrange
from random import seed
import matplotlib.pyplot as plt


# 获取数据函数类
class DB:
    # 读取数据
    def read_data(self, path: str):
        with open(path, 'r', encoding='utf-8') as fp:
            data = fp.readlines()
        for i, x in enumerate(data):
            x = x.strip()
            data[i] = x.split(',')
        data.remove([''])
        train, testdata = self.train_test_split(data, proportion=0.8, random_seed=22)

        def topd(data):
            data = pd.DataFrame(data)
            for i in data.columns[0:-1]:
                data[i] = data[i].astype('float')
            return data

        train = topd(train)
        testdata = topd(testdata)
        return train, testdata

    # 计算返回平均数和极差
    def avr_ptp(self, data_m: np.ndarray):
        avr = np.mean(data_m, axis=0)
        ptp = np.ptp(data_m, axis=0)
        return np.array([avr, ptp])

    # 特征缩放
    def better_data(self, X: np.ndarray, ap: np.ndarray):
        n = ap.shape[1]
        X = np.subtract(X, ap[0])
        X = np.divide(X, ap[1])
        return X

    # 处理各种数据
    def initial(self, train: pd.DataFrame):
        y = np.asarray(train.loc[:, train.columns[-1]])
        X = np.asarray(train.loc[:, train.columns[0:-1]])
        ap = self.avr_ptp(X)
        m = len(y)
        X = self.better_data(X, ap)
        x0 = np.ones(m).reshape(m, 1)
        X = np.hstack((x0, X))
        n = X.shape[1]
        return X, y, n, m, ap

    # 处理y
    def obtainy(self, y):
        dic = {}
        dic = dic.fromkeys(y).keys()
        y_list = []
        for i in dic:
            y1 = []
            for k in y:
                y1.append(k == i)
            y_list.append(y1)
        return y_list, len(dic)

    # 数据分割
    def train_test_split(self, data, proportion=0.7, random_seed=None):
        train_data = []
        seed(random_seed)
        train_size = proportion * len(data)
        data_copy = list(data)

        while len(train_data) < train_size:
            train_data_index = randrange(len(data_copy))
            train_data.append(data_copy.pop(train_data_index))
        return train_data, data_copy


# 梯度下降算法类
class Gradient_descent:
    def __init__(self, X, y, theta, afa=0.1):
        self.X = X
        self.y = y.reshape(len(y), 1)
        self.theta = theta
        self.m = X.shape[0]
        self.afa = afa

    def predictions(self):
        return np.reciprocal((1 + np.exp(-np.matmul(self.X, self.theta))))

    def costFunctionJ(self):
        sqrErrors = -np.matmul(self.y.T, np.log(self.predictions())) - np.matmul((1 - self.y).T,
                                                                                 np.log(1 - self.predictions()))
        return float(1 / self.m * sqrErrors)

    def derivativedelete(self):
        return (np.matmul((self.predictions() - self.y).T, self.X)).T / self.m

    def Gdt_dsc(self):
        self.theta = self.theta - self.afa * self.derivativedelete()

    # 梯度下降
    def GGGG_d(self):
        J_list = [self.costFunctionJ()]
        for i in range(1000):
            self.Gdt_dsc()
            J_list.append(self.costFunctionJ())
        return self.theta, J_list[-1]


def partopt(X, y, n, afa=0.1):
    thetalist = []
    # 防止陷入局部最优，循环取几个起始点
    for i in range(-5, 6):
        initheta = np.ones(n).reshape(n, 1) * i
        GD = Gradient_descent(X, y, initheta, afa)
        initheta, J = GD.GGGG_d()
        thetalist.append((initheta.copy(), J))
    ans = min(thetalist, key=lambda x: x[1])
    return ans[0], ans[1]


# 测试
class TEST:
    hypothesis = []

    def addhy(self, theta, id_):
        theta_r = theta.copy()
        self.hypothesis.append([theta_r, id_])

    def test_ex(self, data):
        result = []
        for hy in self.hypothesis:
            result.append((np.reciprocal(1 + np.exp(-hy[0].T.dot(data))), hy[1]))
        return max(result, key=lambda x: x[0])


def main():
    # 获取各种数据
    """
    X : 特征值
    y : 分类
    n : 特征数量
    m : 训练集容量
    ap : average 和 ptp 平均值和极差
    :return:
    """
    db = DB()
    train, testdata = db.read_data('./irisdata.dat')

    X, y, n, m, ap = db.initial(train)
    y, totcls = db.obtainy(y)
    y = np.asarray(y)

    # 进行梯度下降
    ts = TEST()

    theta1, J = partopt(X, y[0], n, 0.5)
    ts.addhy(theta1, 1)
    theta2, J = partopt(X, y[1], n, 0.8)
    ts.addhy(theta2, 2)
    theta3, J = partopt(X, y[2], n, 0.8)
    ts.addhy(theta3, 3)

    print(ts.hypothesis)

    # 测试
    ha = collections.Counter()
    ha['Iris-setosa'] = 1
    ha['Iris-versicolor'] = 2
    ha['Iris-virginica'] = 3
    rightcnt = 0

    def sol(data, rightcnt):
        datax = data[0:-1]
        datax = db.better_data(datax, ap)
        datax = np.hstack((float(1), datax))
        res = (ts.test_ex(list(datax)), data)
        print(res)
        if res[0][1] == ha[res[1][-1]]:
            rightcnt += 1
        return rightcnt

    data = np.asarray(testdata)
    for i in range(len(data)):
        rightcnt = sol(data[i], rightcnt)
    print(f'准确率: {rightcnt}/{len(testdata)}')


if __name__ == "__main__":
    main()

### 算法：梯度下降

### 成果展示：
* **回归得到三种分类参数列表**:
```
  1. [array([[-2.02333575],[-2.35988991],[ 6.93878696],[-6.104296  ],[-6.0846037 ]]), 1],  
  2. [array([[-1.02759317e+00],[ 5.75824268e-03],[-6.24996800e+00],[ 3.19542117e+00],[-2.64619723e+00]]), 2],   
  3. [array([[-4.17437233],[ 2.06372992],[-3.32835651],[ 7.50671886],[10.87416835]]), 3]  
```

* **测试**:  
```
((array([0.9643152]), 1), array([4.9, 3.0, 1.4, 0.2, 'Iris-setosa'], dtype=object))  
((array([0.98635324]), 1), array([5.0, 3.4, 1.5, 0.2, 'Iris-setosa'], dtype=object))  
((array([0.99435329]), 1), array([5.4, 3.9, 1.3, 0.4, 'Iris-setosa'], dtype=object))  
((array([0.98735345]), 1), array([5.1, 3.5, 1.4, 0.3, 'Iris-setosa'], dtype=object))  
((array([0.97506834]), 1), array([5.0, 3.4, 1.6, 0.4, 'Iris-setosa'], dtype=object))  
((array([0.9885251]), 1), array([5.5, 3.5, 1.3, 0.2, 'Iris-setosa'], dtype=object))  
((array([0.98933736]), 1), array([5.0, 3.5, 1.3, 0.3, 'Iris-setosa'], dtype=object))  
((array([0.95725104]), 1), array([4.8, 3.0, 1.4, 0.3, 'Iris-setosa'], dtype=object))  
((array([0.32054024]), 2), array([5.6, 3.0, 4.5, 1.5, 'Iris-versicolor'], dtype=object))  
((array([0.68484894]), 2), array([6.3, 2.5, 4.9, 1.5, 'Iris-versicolor'], dtype=object))  
((array([0.55310765]), 2), array([6.1, 2.8, 4.7, 1.2, 'Iris-versicolor'], dtype=object))  
((array([0.40583778]), 2), array([6.4, 2.9, 4.3, 1.3, 'Iris-versicolor'], dtype=object))  
((array([0.51247195]), 2), array([6.8, 2.8, 4.8, 1.4, 'Iris-versicolor'], dtype=object))  
((array([0.63053679]), 3), array([6.7, 3.0, 5.0, 1.7, 'Iris-versicolor'], dtype=object))  
((array([0.37983819]), 2), array([6.0, 2.9, 4.5, 1.5, 'Iris-versicolor'], dtype=object))  
((array([0.70258848]), 2), array([5.5, 2.4, 3.8, 1.1, 'Iris-versicolor'], dtype=object))  
((array([0.58447363]), 2), array([5.8, 2.6, 4.0, 1.2, 'Iris-versicolor'], dtype=object))  
((array([0.35697091]), 2), array([5.7, 3.0, 4.2, 1.2, 'Iris-versicolor'], dtype=object))  
((array([0.40576064]), 2), array([6.2, 2.9, 4.3, 1.3, 'Iris-versicolor'], dtype=object))  
((array([0.53745949]), 2), array([5.1, 2.5, 3.0, 1.1, 'Iris-versicolor'], dtype=object))  
((array([0.99310448]), 3), array([7.6, 3.0, 6.6, 2.1, 'Iris-virginica'], dtype=object))  
((array([0.88225301]), 3), array([5.7, 2.5, 5.0, 2.0, 'Iris-virginica'], dtype=object))  
((array([0.99897628]), 3), array([7.7, 2.6, 6.9, 2.3, 'Iris-virginica'], dtype=object))  
((array([0.98222852]), 3), array([6.9, 3.2, 5.7, 2.3, 'Iris-virginica'], dtype=object))  
((array([0.97576771]), 3), array([6.4, 2.8, 5.6, 2.2, 'Iris-virginica'], dtype=object))  
((array([0.73460026]), 2), array([6.1, 2.6, 5.6, 1.4, 'Iris-virginica'], dtype=object))  
((array([0.99490803]), 3), array([7.7, 3.0, 6.1, 2.3, 'Iris-virginica'], dtype=object))  
((array([0.79173836]), 3), array([6.4, 3.1, 5.5, 1.8, 'Iris-virginica'], dtype=object))  
((array([0.94971688]), 3), array([6.2, 3.4, 5.4, 2.3, 'Iris-virginica'], dtype=object))  
((array([0.65941781]), 3), array([5.9, 3.0, 5.1, 1.8, 'Iris-virginica'], dtype=object))  
```

* **准确率**: 28/30 (93.3333%)


### 所作的尝试

#### Python，明明只append了一次，为什么所有子列表都变了啊.jpg！！！！！！   

#### 梯度下降有时候可以正常拟合有时候不正常，仔细检查了一天发现是获取y时用集合顺序是随机的！！！

#### 最后判断不上，偏差太大，发现原来是因为特征缩放，输入的时候要同样处理一遍数据

在网上找了几个机器学习的例子，了解一下机器学习算法是要干什么  
建立算法类  
读入样本  
运行算法，打印代价函数  
打印学习后的参数

学习回归分类算法  
简单了解KNN算法  
尝试octave和matlab  

浅浅试了一下用梯度下降做回归  
竟然成功了！！！  

最后再来实现数据集划分
https://zhuanlan.zhihu.com/p/475930864  
（知乎大佬写的真好，csdn知乎俩太好用了）

~~找小错找麻了~~  

python的set()函数去重不保留顺序！！！
要顺序的话用字典去重
```python
dic = {}
dic = dic.fromkeys(list).keys()
```

matlab
* double(y) 将categories类型的y转换成数字  
* y1 = y == 1 y中为1的设1，不为1的设0  
* range(X,1) 求极差  

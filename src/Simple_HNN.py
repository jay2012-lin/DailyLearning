# -*-coding:UTF-8-*-
# Author:jaylin
# File:Simple_HNN.py
# Time:2017/5/23 15:37
# 简单的隐马尔可夫模型示例代码
# http://www.hankcs.com/nlp/hmm-and-segmentation-tagging-named-entity-recognition.html

states = ('Rainy','Sunny') #隐状态
observations = ('walk','shop','clean')#观测状态 实际状态，根据这些状态使用维特比算法计算最有可能的情况
start_probability ={'Rainy':0.6,'Sunny':0.4}#初始概率
transition_probability ={#隐状态转换概率
 'Rainy':{'Rainy':0.7,'Sunny':0.3},
 'Sunny':{'Rainy':0.4,'Sunny':0.6}
}
emission_probability={#发射概率
 'Rainy' : {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
 'Sunny' : {'walk': 0.6, 'shop': 0.3, 'clean': 0.1},
}

def viterbi(obs,states,start_p,trans_p,emit_p):

    """

    :param obs:观测序列
    :param states:隐状态
    :param start_p:初始概率（隐状态）
    :param trans_p:转移概率（隐状态）
    :param emit_p: 发射概率 （隐状态表现为显状态的概率）
    :return:
    """

    # 路径概率表 V[时间][隐状态] = 概率
    V = [{}]
    # 一个中间变量，代表当前状态是哪个隐状态
    path = {}
    # 初始化初始状态 (t == 0)
    for state in states:
        V[0][state] = start_p[state]*emit_p[state][obs[0]]
        path[state] = [state]

    #对t>0使用维特比算法进行递推
    for t in range(1,len(obs)):#迭代到n-1
        V.append({})
        newpath = {}

        for state in states:
            # 概率 隐状态 = 前状态是y0的概率 * y0转移到y的概率 * y表现为当前状态的概率
            #print state
            (prob,prob_state)=max([(V[t-1][state0]*trans_p[state0][state]*emit_p[state][obs[t]],state0) for state0 in states])
            #记录当前的概率
            V[t][state] = prob
            #记录路径
            newpath[state]= path[prob_state]+[state] #这儿的加号的意义好像就是append
        #更新路径
        path = newpath

    print_dptable(V)
    (prob,state) = max([(V[len(obs)-1][state],state) for state in states])
    return (prob,path[state])

#打印路径概率表
def print_dptable(V):
    print " ",
    for i in range(len(V)):print "%7d"%(i+1),
    print

    for state in V[0].keys():
        print "%.5s:"%state,
        for t in range(len(V)):
            print "%.7s"%("%f"%V[t][state]),
        print


def example():
    return viterbi(observations,states,start_probability,transition_probability,emission_probability)


print example()
import csv
import time
import copy
import numpy as np
import pandas as pd
from math import log,pow
from sklearn.preprocessing import MinMaxScaler
from rules import *
# Extract dependency pattern in each sentence
def get_denp(dependence):
    pattern_all = []
    for sentence in dependence:
        pattern = []
        for piece in sentence:
            pattern.append(piece[1])
        pattern = list(set(pattern))
        pattern_all.append(pattern)
    return pattern_all

# Combine tokenized result with dependency pattern result
def data_gather(dependence,segment):
    n = len(dependence)
    m = len(segment)
    #print(m,n)
    for i in range(n):
        dependence[i] = dependence[i] + segment[i]
    return dependence

# Calculate supp value
def calc_supp(node_1,node_2,data):
    length = len(data)
    all = []
    for ele1 in node_1:
        prob = []
        for ele2 in node_2:
            in_o_in_t = 0
            in_o_no_t = 0
            no_o_in_t = 0
            no_o_no_t = 0
            for sentence in data:
                if ele1 in sentence:
                    if ele2 in sentence:
                        in_o_in_t += 1
                    else:
                        in_o_no_t += 1
                else:
                    if ele2 in sentence:
                        no_o_in_t += 1
                    else:
                        no_o_no_t += 1
            try:
                Pij = in_o_in_t/(in_o_in_t + no_o_in_t)
            except:
                Pij = 0
            Nij = in_o_in_t
            Nj = in_o_in_t + no_o_in_t
            try:
                Pij_ = in_o_no_t/(in_o_no_t + no_o_no_t)
            except:
                Pij_ = 0
            Nij_ = in_o_no_t
            Nj_ = in_o_no_t + no_o_no_t
            Pi = (in_o_in_t + in_o_no_t)/length
            Ni = in_o_in_t + in_o_no_t
            N = length
            T1 = [Pij,Nij,Nj]
            T2 = [Pij_,Nij_,Nj_]
            T3 = [Pi,Ni,N]
            supp = 2*(calc_T(T1)+calc_T(T2)-calc_T(T3))
            #print([in_o_in_t,in_o_no_t,no_o_in_t,no_o_no_t])
            prob.append(supp)
        all.append(prob)
        minMax = MinMaxScaler()
        array_norm = minMax.fit_transform(all)
    return array_norm

# Calculate confidence
def cal_pattern_conf(opinion,target,pattern,cluster):
    output = []
    for ele in pattern:
        conf_1 = calc_supp([ele], target, cluster)
        conf_2 = calc_supp([ele], opinion, cluster)
        score = sum(conf_1)+sum(conf_2)
        output.append([ele,score])
    return output

# Calculate T
def calc_T(T):
    #print(T)
    try:
        # return log(pow(T[0],T[1])*pow(1-T[0],T[2]-T[1]),10)
        return T[1]*log(T[0],10) + (T[2]-T[1]) * log((1-T[0]),10)
    except:
        return 0

# Calculate parameter matrix
def score_matrix(W1,W2):
    S0 = np.ones((1,np.shape(W1)[0]))
    S1 = np.ones((1,np.shape(W2)[1]))
    M0 = np.dot(S0,W1)
    En0 = np.dot(M0,W2)
    M1 = np.dot(S1,np.transpose(W2))
    En1 = np.dot(M1,np.transpose(W1))
    S2 = S0 + En1
    M2 = M0 + M1
    En2 = En0 + S1
    return S2.tolist()[0],M2.tolist()[0],En2.tolist()[0]

# Initialize min max normalization
def MinMaxNorm(orig):
    Min = min(orig)
    Max = max(orig)
    for n in range(len(orig)):
        orig[n] = (orig[n] - Min) / (Max - Min)
    return orig

# Filtering process
def refinement(arr,score):
    for i in range(0,len(score)-1):

        if score[i] <= 2:
            print(arr[i])
            arr[i] = None
        else:
            continue
    arr = filter(None,arr)
    return arr

le = 11
# Initilize opinion word seeds & target word seeds
op = set(input('Input seed opinion words separated by comma:').split(','))
ta = set(input('Input seed target words separated by comma:').split(','))

for cons in [1]:#,1.5,2,2.5,3,3.5,4,4.5,5]:
    ind = 1
    flag = 1
    all_pairs = []
    for o in range(24341):
        all_pairs.append([])
    all_cluster = []
    while flag:
        if ind < 25:
            start = ind * 1000 - 999
            end = ind * 1000
        else:
            flag = 0
            continue
            #start = 24001
            #end = 24341
            #flag = 0
        print(ind, start, end, '**************')
        # Import tokenized (after segmentation) data
        with open('seg_data.csv', 'r', encoding='UTF-8') as csvfile1:
            reader = csv.reader(csvfile1)
            sentence = [ele[0] for ele in reader]
            segment = sentence[start:end + 1]
            k = 0
            for one in segment:
                segment[k] = eval(one)
                segment[k] = [x for j in segment[k] for x in j]
                k = k + 1
        # Import dependency parsing result data
        with open('dep_data.csv', 'r', encoding='UTF-8') as csvfile2:
            reader = csv.reader(csvfile2)
            data = [row for row in reader]
            data = data[start:end + 1]
            dependence = []
            for row in data:
                sub = []
                for index in range(len(row)):
                    if row[index] == '':
                        pass
                    else:
                        sub.append(eval(row[index]))
                dependence.append(sub)

        pattern_data = get_denp(dependence)
        # for ele in dependence:
        cluster = data_gather(pattern_data, segment)
        all_cluster += cluster
        opinion = op
        target = ta
        pattern = {'mmod', 'dobj'}
        pattern_1 = {'advmod'}
        pattern_2 = {'nsubj'}
        rules = ['R11(dependence[i], opinion, pattern, target, all_pairs[start+i-1])',
                 'R12(dependence[i], opinion, pattern, target, all_pairs[start+i-1])',
                 'R13(dependence[i], opinion, pattern, target, all_pairs[start+i-1])',
                 'R21(dependence[i],opinion,pattern_1,pattern_2,target, all_pairs[start+i-1])',
                 'R22(dependence[i],opinion,pattern_1,pattern_2,target,all_pairs[start+i-1])',
                 'R23(dependence[i],opinion,pattern_1,pattern_2,target,all_pairs[start+i-1])',
                 'R31(dependence[i],target,pattern,all_pairs[start+i-1])',
                 'R32(dependence[i],opinion,pattern,all_pairs[start+i-1])', 'R41(dependence[i],target)',
                 'R42(dependence[i],opinion)']
        # print(calc_supp(pattern,target,cluster))

        count = 0
        goon = True
        iteration = 0
        while goon:
            cache_o = copy.deepcopy(opinion)
            cache_t = copy.deepcopy(target)
            cache_p = copy.deepcopy(pattern)
            for i in range(len(dependence)):
                for rule in rules:
                    count = count + 1
                    eval(rule)
                    if (count > 1000) and (count % 200 == 0):
                        opinion = list(opinion)
                        target = list(target)
                        pattern = list(pattern | pattern_1 | pattern_2)
                        W1 = calc_supp(opinion, pattern, cluster)
                        W2 = calc_supp(pattern, target, cluster)
                        score_o, score_p, score_t = score_matrix(W1, W2)
                        # score_o = MinMaxNorm(score_o)
                        # score_p = MinMaxNorm(score_p)
                        # score_t = MinMaxNorm(score_t)

                        print(score_o)
                        print(opinion)
                        print('###############')

                        opinion = refinement(opinion, score_o)
                        pattern = refinement(pattern, score_p)
                        target = refinement(target, score_t)
                        opinion = set(opinion)
                        target = set(target)
                        pattern = set(pattern)
                        if opinion == cache_o and target == cache_t and pattern == cache_p:
                            goon = False
            iteration += 1
            print(iteration)

        time.sleep(5)
        ind += 1

    test = pd.DataFrame(data=all_pairs)
    #file = 'pairs' + str(le) + '.csv'
    test.to_csv('pairs.csv', index=False, encoding='utf_8_sig', sep=',')
    le += 1
    # print(cal_pattern_conf(opinion,target,pattern,cluster))
    print(opinion)
    print(pattern)
    print(target)





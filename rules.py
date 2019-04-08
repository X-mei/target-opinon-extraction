'''
根据OP算法实现的八个提取规则
'''

# POS tag
NN = ['NN', 'NNP', 'NNS', 'NP', 'NR', 'NT', 'PN']
JJ = ['JJ', 'JJS', 'JJR', 'VA', 'ADJP']

# Dep = [] Depandency relations在每个实现函数里有所定义，因为每一个函数需要的依存关系不同
CONJ = ["conj"]

# 三类规则：Type1：O->T、Type2：T->T、Type3:O/T->O
# Type1：O->T
'''规则的实现均为考虑提取出来的意见词和方面词是否已经出现过'''
'''parser[(i) * 3][0] == Dep,不知道用==会不会有问题'''

# 从opinion一步到target
def R11(parser, Opi, Dep, Tar, Pairs):
    # Dep = ["amod", "prep", "nsubj", "csubj", "xsubj", "dobj","iobj"]
    for i in range(len(parser)):
        # R11,提取T
        if parser[i][0][0] in Opi and parser[i][1] in Dep and parser[i][2][1] in NN:
            Tar.add(parser[i][2][0])  # ####################成对OT
            #print("运行了R11")
            if [parser[i][2][0],parser[i][0][0]] not in Pairs:
                Pairs.append([parser[i][2][0],parser[i][0][0]])
    return Pairs


# 从target一步到opinion
def R12(parser,Opi,Dep,Tar, Pairs):
    # Dep = ["amod", "prep", "nsubj", "csubj", "xsubj", "dobj","iobj"]
    for i in range(len(parser)):
        # R11,提取T
        '''
        if parser[i][0][0] in Tar and parser[i][1] in Dep and parser[i][2][1] in JJ:
            Opi.add(parser[i][2][0])  # ####################成对OT
            print("运行了R11")
        '''
        if parser[i][2][0] in Tar and parser[i][1] in Dep and parser[i][0][1] in JJ:
            Opi.add(parser[i][0][0])  # ####################成对OT
            #print("运行了R12")
            if [parser[i][2][0],parser[i][0][0]] not in Pairs:
                Pairs.append([parser[i][2][0],parser[i][0][0]])
    return Pairs

# 从opinion和target一步到pattern
def R13(parser,Opi,Dep,Tar,Pairs):
    for i in range(len(parser)):
        if parser[i][2][0] in Tar and parser[i][0][0] in Opi and parser[i][1] not in Dep:
            Dep.add(parser[i][1])  # ####################成对OT
            #print("运行了R13")
            if [parser[i][2][0],parser[i][0][0]] not in Pairs:
                Pairs.append([parser[i][2][0],parser[i][0][0]])
    return Pairs

# 从opinion两步到target
def R21(parser,Opi,Dep1,Dep2,Tar,Pairs):
    # Dep = ["amod", "prep", "nsubj", "csubj", "xsubj", "dobj", "iobj"]
    for i in range(len(parser)):
        if parser[i][0][0] in Opi and parser[i][1] in Dep1:
            for j in range(len(parser)):
                if (parser[i][2][0] == parser[j][2][0] and i != j and parser[j][1] in Dep2 and
                        parser[j][0][1] in NN):
                    Tar.add(parser[j][0][0])  #####################成对OT
                    #print("运行了R21")
                    if [parser[j][0][0],parser[i][0][0]] not in Pairs:
                        Pairs.append([parser[j][0][0],parser[i][0][0]])
    return Pairs

# 从target两步到opinion
def R22(parser,Opi,Dep1,Dep2,Tar,Pairs):
    # Dep = ["amod", "prep", "nsubj", "csubj", "xsubj", "dobj", "iobj"]
    for i in range(len(parser)):
        if parser[i][0][0] in Tar and parser[i][1] in Dep2:
            for j in range(len(parser)):
                if ((parser[i][2][0] == parser[j][2][0]) and i != j and parser[j][1] in Dep1 and
                        parser[j][0][1] in JJ):
                    Opi.add(parser[j][0][0])  #####################成对OT
                    #print("运行了R22")
                    if [parser[i][0][0],parser[j][0][0]] not in Pairs:
                        Pairs.append([parser[i][0][0],parser[j][0][0]])
    return Pairs


# 从opinion和target两步到pattern
def R23(parser, Opi, Dep1, Dep2, Tar, Pairs):
    # Dep = ["amod", "prep", "nsubj", "csubj", "xsubj", "dobj", "iobj"]
    for i in range(len(parser)):
        if parser[i][0][0] in Opi:
            for j in range(len(parser)):
                if ((parser[i][2][0] == parser[j][2][0]) and i != j and parser[j][2][0] in Tar):
                    Dep1.add(parser[i][1])  #####################成对OT
                    Dep2.add(parser[j][1])
                    #print("运行了R12")
                    if [parser[j][2][0],parser[i][0][0]] not in Pairs:
                        Pairs.append([parser[j][2][0],parser[i][0][0]])
    return Pairs

# 从opinion一步到opinion
def R32(parser, Opi, Dep, Pairs):
    for i in range(len(parser)):
        if parser[i][0][0] in Opi and parser[i][1] in CONJ and parser[i][2][1] in JJ:
            Opi.add(parser[i][2][0])
            for pair in Pairs:
                if parser[i][0][0] in pair[1]:
                    if [pair[0],parser[i][2][0]] not in Pairs:
                        Pairs.append([pair[0],parser[i][2][0]])
            #print("运行了R32")

        if parser[i][2][0] in Opi and parser[i][1] in CONJ and parser[i][0][1] in JJ:
            Opi.add(parser[i][0][0])
            for pair in Pairs:
                if parser[i][2][0] in pair[1]:
                    if [pair[0],parser[i][0][0]] not in Pairs:
                        Pairs.append([pair[0],parser[i][0][0]])
            #print("另一种运行了R32")

# 从target一步到target
def R31(parser, Tar, Dep, Pairs):
    for i in range(len(parser)):
        if parser[i][0][0] in Tar and parser[i][1] in CONJ and parser[i][2][1] in NN:
            Tar.add(parser[i][2][0])
            for pair in Pairs:
                if parser[i][0][0] in pair[0]:
                    if [parser[i][2][0],pair[1]] not in Pairs:
                        Pairs.append([parser[i][2][0],pair[1]])
            #print("运行了R31")

        if parser[i][2][0] in Tar and parser[i][1] in CONJ and parser[i][0][1] in NN:
            Tar.add(parser[i][0][0])
            for pair in Pairs:
                if parser[i][2][0] in pair[0]:
                    if [parser[i][0][0],pair[1]] not in Pairs:
                        Pairs.append([parser[i][0][0],pair[1]])
            #print("另一种运行了R31")

# 从target两步到target
def R41(parser,Tar):
    for i in range(len(parser)):
        if parser[i][0][0] in Tar:
            for j in range(len(parser)):
                if parser[i][2][0] == parser[j][2][0] and parser[j][0][0] in Tar and parser[i][1] == parser[j][1]:
                    Tar.add(parser[j][0][0])
                    #print("运行了R41")

# 从opinion两步到opinion
def R42(parser,Opi):
    for i in range(len(parser)):
        if parser[i][0][0] in Opi:
            for j in range(len(parser)):
                if parser[i][2][0] == parser[j][2][0] and parser[j][0][0] in Opi and parser[i][1] == parser[j][1]:
                    Opi.add(parser[j][0][0])
                    #print("运行了R42")

'''
def R42(parser,O_Expanded,Dep1,Dep2):
    result42 = []
    # Dep = ["amod", "prep", "nsubj", "csubj", "xsubj", "dobj", "conj"]
    for i in range(0, len(parser) // 3):
        if parser[i * 3 + 2][0] in O_Expanded:
            for j in range(0, len(parser) // 3):
                if (parser[i * 3][0] == Dep1 and parser[j * 3][0] == Dep2 and parser[i * 3 + 1][0] ==
                        parser[j * 3 + 1][0] and i != j and parser[j * 3 + 2][1] in JJ ):
                    result42.append(parser[j * 3 + 2][0])
                    print("运行了R42")
        if parser[i * 3 + 1][0] in O_Expanded:
            for j in range(0, len(parser) // 3):
                if (parser[i * 3][0] == Dep1 and parser[j * 3][0] == Dep2 and parser[i * 3 + 2][0] ==
                        parser[j * 3 + 2][0] and i != j and parser[j * 3 + 1][1] in JJ):
                    result42.append(parser[j * 3 + 1][0])
                    print("另一种运行了R42")
    return result42
'''

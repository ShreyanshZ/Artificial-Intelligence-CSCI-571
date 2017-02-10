import sys,copy



def addQuery(term):
    dictionary = {}
    predicateName = getPredicateName(term)
    if predicateName in dictionary:
        dictionary[predicateName].append(term)
    else:
        dictionary[predicateName] = [term]
    KnowledgeBase.append(dictionary)

def makeKB(sentence):
    for item in sentence:
        dictionary = {}
        literals = item.split('|')
        for term in literals:
            predicateName = getPredicateName(term)
            if predicateName in dictionary:
                dictionary[predicateName].append(term)
            else:
                dictionary[predicateName] = [term]
        KnowledgeBase.append(dictionary)

def getPredicateName(item):
    if item[0] == '~':
        item = item[1:]
    predicateName = item.split('(')
    return predicateName[0]

def findArguments(string):
    start = string.find("(")
    end = string.find(")")
    temp = string[start + 1:end]
    arg = temp.split(',')
    return arg

def isUnifiable(String1, String2):
    tempList = []
    argument1 = findArguments(String1)
    argument2 = findArguments(String2)
    bound = {}
    i = 0
    if len(argument1) == len(argument2):
        i = 0
        while i < len(argument1):
            if argument1[i][0].isupper() and argument2[i][0].isupper():
                if argument1[i] == argument2[i]:
                    tempList.append(argument1[i])
                else:
                    break
            elif argument1[i][0].isupper() and argument2[i] not in bound:
                tempList.append(argument1[i])
                bound[argument2[i]] = argument1[i]
            elif argument2[i] in bound:
                tempB = bound[argument2[i]]
                if tempB != argument1[i]:
                    break
                else:
                    tempList.append(argument1[i])
            else:
                if argument2[i][0].islower() and argument2[i] not in bound:
                    tempList.append(argument1[i])
                    bound[argument2[i]] = argument1[i]
                elif argument2[i] in bound:
                    tempB = bound[argument2[i]]
                    if tempB != argument1[i]:
                        break
                    else:
                        tempList.append(argument1[i])
                else:
                    tempList.append(argument1[i])
            i += 1
        if i < len(argument1):
            return None
    else:
        return None
    return tempList

def unify(checkBound, inputList):
    temp = getPredicateName(inputList)
    if inputList[0] == '~':
        temp = '~' + temp
    temp = temp + '('
    tempList = findArguments(inputList)
    for i in range(0, len(tempList)):
        if tempList[i] in checkBound:
            temp = temp + checkBound[tempList[i]] + ','
        else:
            temp = temp + tempList[i] + ','
    temp = temp[:len(temp) - 1]
    temp = temp + ')'
    return temp

def Resolution(query, knowledgeBase):
    #print('resolving', query)
    key = getPredicateName(query)
    for i in range(0, len(knowledgeBase)):
        HashSet = knowledgeBase[i]
        log = 0
        #print('search', key, 'in', knowledgeBase[i], 'i', i, 'size', len(knowledgeBase))
        if key in HashSet:
            #print('In for', key)
            gTemp = HashSet[key]
            isNegative = True
            if query[0] == '~':
                isNegative = False
            if isNegative:
                jTemp = 0
                while jTemp < len(gTemp):
                    tTemp = gTemp[jTemp]
                    if tTemp[0] == '~':
                        yTemp = isUnifiable(query, tTemp)
                        if yTemp:
                            rTemp = findArguments(tTemp)
                            checkBound = {}
                            k = 0
                            while k < len(rTemp):
                                #print('here', k, len(rTemp), rTemp[k], yTemp[k])
                                checkBound[rTemp[k]] = yTemp[k]
                                k += 1
                            log = jTemp
                            inputList = []
                            for k in HashSet:
                                if k != key:
                                    temp = HashSet[k]
                                    for ti in temp:
                                        inputList.append(unify(checkBound, ti))
                            pTemp = 0
                            while pTemp < len(gTemp):
                                if pTemp != log:
                                    inputList.append(unify(checkBound, gTemp[pTemp]))
                                pTemp += 1
                            #print('unified', inputList)
                            if len(inputList) == 0:
                                #print('RESOLVED')
                                return True
                            tempKnowledgeBase = knowledgeBase[:]
                            tempKnowledgeBase.pop(i)
                            #print(len(tempKnowledgeBase))
                            qTemp = 0
                            while qTemp < len(inputList):
                                ans = Resolution(inputList[qTemp], tempKnowledgeBase)
                                if not ans:
                                    #print('CANNOT RESOLVE')
                                    break
                                qTemp += 1
                            if qTemp == len(inputList):
                                return True
                    jTemp += 1
            else:
                jTemp = 0
                while jTemp < len(gTemp):
                    tTemp = gTemp[jTemp]
                    if tTemp[0] != '~':
                        yTemp = isUnifiable(query, tTemp)
                        if yTemp:
                            #print('YO', yTemp)
                            rTemp = findArguments(tTemp)
                            checkBound = {}
                            k = 0
                            while k < len(rTemp):
                                #print('here2', k, len(rTemp), rTemp[k], yTemp[k])
                                checkBound[rTemp[k]] = yTemp[k]
                                k += 1
                            log = jTemp
                            inputList = []
                            for k in HashSet:
                                if k != key:
                                    temp = HashSet[k]
                                    for ti in temp:
                                        inputList.append(unify(checkBound, ti))
                            pTemp = 0
                            while pTemp < len(gTemp):
                                if pTemp != log:
                                    inputList.append(unify(checkBound, gTemp[pTemp]))
                                pTemp += 1
                            #print('unified', inputList)
                            if len(inputList) == 0:
                                #print('RESOLVED')
                                return True
                            tempKnowledgeBase = knowledgeBase[:]
                            tempKnowledgeBase.pop(i)
                            #print(len(tempKnowledgeBase))
                            qTemp = 0
                            while qTemp < len(inputList):
                                ans = Resolution(inputList[qTemp], tempKnowledgeBase)
                                if not ans:
                                    #print('CANNOT RESOLVE')
                                    break
                                qTemp += 1
                            if qTemp == len(inputList):
                                return True
                    jTemp += 1
    return False

def cleanInput(line):
    line = line.replace(" ", "")
    line = line.replace("~", " ~ ")
    line = line.replace("&", " & ")
    line = line.replace("|", " | ")
    line = line.replace("=>", " => ")
    line = line.rstrip('\n')
    return line

def pretoInfix(cnf):
    tempCNF=copy.deepcopy(cnf)
    if tempCNF[0] == "&":
        for i in range(1, len(tempCNF)):
            if "~" in tempCNF[i]:
                tempCNF[i] = joinNot(tempCNF[i])
            if "|" in tempCNF[i]:
                tempCNF[i] = orPremise(tempCNF[i])
        andString = ""
        for i in range(1, len(tempCNF)):
            if i == len(tempCNF) - 1:
                andString += (tempCNF[i])
            else:
                andString += (tempCNF[i])
                andString += "&"
        tempCNF = andString
        return (andString)
    elif tempCNF[0] == "|":
        tempCNF = orPremise(tempCNF)
        return (tempCNF)
    elif tempCNF[0] == "~":
        tempCNF = joinNot(tempCNF)
        return tempCNF
    else:
        return tempCNF

def orPremise(orcnf):
    temporcnf=copy.deepcopy(orcnf)
    for i in range(1, len(temporcnf)):
        if "~" in temporcnf[i]:
            temporcnf[i] = (joinNot(temporcnf[i]))
    orString = ""
    for i in range(1, len(temporcnf)):
        if i == len(temporcnf) - 1:
            orString += (temporcnf[i])
        else:
            orString += (temporcnf[i])
            orString += "|"
    return orString

def joinNot(premiseList):
    premise = ""
    while premiseList:
        premise += premiseList.pop(0)
    return (premise)

def properFormat(output):
    tempStack = []
    while output:
        temp = output.pop()
        if temp in prec:
            if temp == "~":
                oper1 = tempStack.pop()
                insertStack = []
                insertStack.append(temp)
                insertStack.append(oper1)
                tempStack.append(insertStack)
            else:
                oper1 = tempStack.pop()
                oper2 = tempStack.pop()
                insertStack = []
                insertStack.append(temp)
                insertStack.append(oper1)
                insertStack.append(oper2)
                tempStack.append(insertStack)
        else:
            tempStack.append(temp)
    tempStack.reverse()
    if (len(tempStack)) == 1:
        return tempStack.pop()
    else:
        return tempStack

def fixBrackets(infixexpr):
    i = 0
    while i < len(infixexpr):
        if i == 0 and infixexpr[i] == "(" and (infixexpr[i + 1] in prec or infixexpr[i + 1] == " " or infixexpr[
                i + 1] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or infixexpr[i + 1] == "("):
            infixexpr = infixexpr[:i] + " { " + infixexpr[i + 1:]
            i = 0
        if i != 0 and infixexpr[i] == "(" and (infixexpr[i + 1] in prec or infixexpr[i + 1] == " " or infixexpr[
                i + 1] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or infixexpr[i + 1] == "(") and infixexpr[
                    i - 1] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmonoqrstuvwxyz":
            infixexpr = infixexpr[:i] + " { " + infixexpr[i + 1:]
            i = 0
        if infixexpr[i] == ")" and (infixexpr[i - 1] == ")" or infixexpr[i - 1] == " "):
            infixexpr = infixexpr[:i] + " } " + infixexpr[i + 1:]
            i = 0
        i += 1
    return infixexpr

def infixToPostfix(infixexpr):
    infixexpr = fixBrackets(infixexpr)
    tokenList = infixexpr.split()
    tokenList.reverse()
    for i in range(0, len(tokenList)):
        if (tokenList[i] == '}'):
            tokenList[i] = '['
        elif (tokenList[i] == '{'):
            tokenList[i] = ']'
    opStack = []
    postfixList = []
    for token in tokenList:
        if token not in prec:
            postfixList.append(token)
        elif token == '[':
            opStack.append(token)
        elif token == ']':
            topToken = opStack.pop()
            while topToken != '[':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (opStack) and (prec[opStack[len(opStack) - 1]] > prec[token]):
                postfixList.append(opStack.pop())
            opStack.append(token)
    while opStack:
        postfixList.append(opStack.pop())
    postfixList.reverse()
    return postfixList

def isDistributable(fact):
    if fact[0] == '|':
        for i in range(1, len(fact)):
            if len(fact[i]) > 1 and not isinstance(fact[i], str):
                if fact[i][0] == '&':
                    return True
    return False

def Sweep(fact):
    answer = []
    if fact[0] == '~':
        return fact
    answer.append(fact[0])
    outer_op = fact[0]
    for i in range(1, len(fact)):
        if fact[i][0] == outer_op:
            for jTemp in range(1, len(fact[i])):
                answer.append(fact[i][jTemp])
        else:
            answer.append(fact[i])
    return answer

def Clarified(operator, literals, current):
    answer = []
    answer.append(operator)
    if isinstance(literals, str):
        answer.append(literals[0])
    else:
        answer.append(Clarified(operator, literals[0:len(literals) - 1], literals[len(literals) - 1]))
    answer.append(current)
    return answer

def clarify(fact):
    if len(fact) > 3 and not isinstance(fact, str):
        fact = Clarified(fact[0], fact[1:len(fact) - 1], fact[len(fact) - 1])
    for i in range(1, len(fact)):
        if len(fact[i]) > 1 and not isinstance(fact[i], str):
            fact[i] = clarify(fact[i])
    if len(fact) > 3 and not isinstance(fact, str):
        fact = Clarified(fact[0], fact[1:len(fact) - 1], fact[len(fact) - 1])
    return fact


def isRedundant(logic1, logic2):
    if len(logic1) != len(logic2) and not isinstance(logic1, str) and not isinstance(logic2, str):
        return False
    else:
        if len(logic1) == len(logic2) == 1 and not isinstance(logic1, str) and not isinstance(logic2, str):
            if logic1 == logic2:
                return True
            else:
                return False
        else:
            temp = list(logic2)
            for element in logic1:
                try:
                    temp.remove(element)
                except ValueError:
                    return False
            return not temp


def ifPresent(answer, fact):
    for i in range(1, len(answer)):
        if isRedundant(answer[i], fact):
            return True
    return False

def spreadNot(fact):
    answer = []
    if (fact[1][0] == '|'):
        answer.append('&')
    elif (fact[1][0] == '&'):
        answer.append('|')
    elif (fact[1][0] == '~'):
        return fact[1][1]
    for i in range(1, len(fact[1])):
        if len(fact[1][i]) != 1 and not isinstance(fact[1][i], str):
            answer.append(spreadNot(['~', fact[1][i]]))
        else:
            answer.append(['~', fact[1][i]])
    return answer

def spreadOR(fact):
    answer = []
    answer.append('&')
    if fact[1][0] == '&' and fact[2][0] == '&':
        answer.append(traverseOr(['|', fact[1][1], fact[2][1]]))
        answer.append(traverseOr(['|', fact[1][1], fact[2][2]]))
        answer.append(traverseOr(['|', fact[1][2], fact[2][1]]))
        answer.append(traverseOr(['|', fact[1][2], fact[2][2]]))
    else:
        if fact[1][0] == '&':
            if len(fact[2]) > 2 and not isinstance(fact[2], str):
                if isDistributable(fact[2]):
                    fact[2] = traverseOr(fact[2])
                    answer.append(traverseOr(['|', fact[1][1], fact[2][1]]))
                    answer.append(traverseOr(['|', fact[1][1], fact[2][2]]))
                    answer.append(traverseOr(['|', fact[1][2], fact[2][1]]))
                    answer.append(traverseOr(['|', fact[1][2], fact[2][2]]))
                else:
                    answer.append(traverseOr(['|', fact[1][1], fact[2]]))
                    answer.append(traverseOr(['|', fact[1][2], fact[2]]))
            else:
                answer.append(traverseOr(['|', fact[1][1], fact[2]]))
                answer.append(traverseOr(['|', fact[1][2], fact[2]]))
        else:
            if len(fact[1]) > 2 and not isinstance(fact[1], str):
                if isDistributable(fact[1]):
                    fact[1] = traverseOr(fact[1])
                    answer.append(traverseOr(['|', fact[1][1], fact[2][1]]))
                    answer.append(traverseOr(['|', fact[1][1], fact[2][2]]))
                    answer.append(traverseOr(['|', fact[1][2], fact[2][1]]))
                    answer.append(traverseOr(['|', fact[1][2], fact[2][2]]))
                else:
                    answer.append(traverseOr(['|', fact[1], fact[2][1]]))
                    answer.append(traverseOr(['|', fact[1], fact[2][2]]))
            else:
                answer.append(traverseOr(['|', fact[1], fact[2][1]]))
                answer.append(traverseOr(['|', fact[1], fact[2][2]]))
    return clarify(answer)

def removeRedundant(fact):
    if len(fact) > 2 and not isinstance(fact, str):
        answer = []
        answer.append(fact[0])
        answer.append(fact[1])
        for i in range(2, len(fact)):
            if not ifPresent(answer, fact[i]):
                answer.append(fact[i])
        if len(answer) == 2 and not isinstance(answer, str):
            answer = answer[1]
        return answer
    else:
        return fact

def traverseSweep(fact):
    if isinstance(fact,str):
        return fact
    fact = Sweep(fact)
    for i in range(1, len(fact)):
        if len(fact[i]) > 1 and not isinstance(fact[i], str):
            fact[i] = traverseSweep(fact[i])
    fact = Sweep(fact)
    return fact

def traverseImplies(fact):
    if fact[0] == '=>' and len(fact) == 3:
        answer = []
        answer.append('|')
        answer.append(['~', fact[1]])
        answer.append(fact[2])
        fact=copy.deepcopy(answer)
    for i in range(1, len(fact)):
        if len(fact[i]) > 1 and not isinstance(fact[i], str):
            fact[i] = traverseImplies(fact[i])
    if fact[0] == '=>' and len(fact) == 3:
        answer = []
        answer.append('|')
        answer.append(['~', fact[1]])
        answer.append(fact[2])
        fact=copy.deepcopy(answer)
    return fact

def traverseNegation(fact):
    if fact[0] == '~' and len(fact) == 2 and len(fact[1]) != 1 and not isinstance(fact[1], str):
        fact = spreadNot(fact)
    for i in range(1, len(fact)):
        if len(fact[i]) > 1 and not isinstance(fact[i], str):
            fact[i] = traverseNegation(fact[i])
    if fact[0] == '~' and len(fact) == 2 and len(fact[1]) != 1 and not isinstance(fact[1], str):
        fact = spreadNot(fact)
    return fact

def traverseOr(fact):
    if isDistributable(fact):
        fact = spreadOR(fact)
    for i in range(1, len(fact)):
        if len(fact[i]) > 1 and not isinstance(fact[i], str):
            fact[i] = traverseOr(fact[i])
    if isDistributable(fact):
        fact = spreadOR(fact)
    return clarify(fact)

def traverseRedundant(fact):
    fact = removeRedundant(fact)
    for i in range(1, len(fact)):
        if len(fact[i]) > 1 and not isinstance(fact[i], str):
            fact[i] = traverseRedundant(fact[i])
    fact = removeRedundant(fact)
    return fact

# *****************************************************MAIN*********************************************************#
def main():
    inputfile = open('input.txt', 'r')
    outputfile = open('output.txt', 'w')
    lines = []
    for line in inputfile:
        line = cleanInput(line)
        lines.append(line)
    noq = int(lines[0])
    querylist = []
    for i in range(1, noq + 1):
        querylist.append(lines[i])
    #print(querylist)
    for i in range(0, len(querylist)):
        querylist[i] = querylist[i].replace(" ", "")
    #print(querylist)
    resolution = []
    for i in range(1, noq + 1):
        resolution.append(lines[i])
    nof = int(lines[noq + 1])
    #print(nof)
    #print(nof + 1 + noq + 1)
    queries = []
    for i in range(noq + 2, nof + 1 + noq + 1):
        queries.append(lines[i].rstrip('\n'))
    listTerms = []
    for query in queries:
        op = properFormat(infixToPostfix(query))
        if isinstance(op, list):
            cnf=[]
            if len(op) == 0:
                cnf=op
            if len(op) == 1 and not isinstance(op, str):
                cnf=op[0]
            else:
                cnf = traverseImplies(op)
                cnf = traverseNegation(cnf)
                cnf = clarify(cnf)
                cnf = traverseOr(cnf)
                cnf = traverseSweep(cnf)
                cnf = traverseRedundant(cnf)
                cnf = pretoInfix(cnf)
            listTerms.append(cnf)
        else:
            listTerms.append(op)
    sentence = []
    #print(listTerms)
    for tem in listTerms:
        c = tem.split("&")
        for i in c:
            sentence.append(i)
    makeKB(sentence)
    #print(len(KnowledgeBase))
    for item in querylist:
        if item[0] == '~':
            item = item[1:]
        else:
            item = '~' + item
        addQuery(item)
        sol = Resolution(item, KnowledgeBase)
        #print(item, sol)
        if sol == True:
            outputfile.write("TRUE\n")
        if sol == False:
            outputfile.write("FALSE\n")
        KnowledgeBase.pop()
    outputfile.close()

if __name__=='__main__':
    prec = {"~": 4, "&": 3, "|": 2, "=>": 1, "[": 0, "]": 0}
    KnowledgeBase = []
    main()
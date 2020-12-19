#
# Copyright author 2020
# Created by __sh0l1n@
#

class PyFloat:
    def __init__(self, n="0"):
        self.__n = PyFloat.parseFromSciNumber(n)

    @staticmethod
    def parseFromDouble(double):
        return PyFloat(PyFloat.parseFromSciNumber(str(double)))

    @staticmethod
    def parseFromSciNumber(double):
        number = str(double)
        if "e" in number:
            nat, realComposedE = number.split("e")
            sign, realE = realComposedE[0], realComposedE[1:]
            realE = "0" * (int(realComposedE[1:]) - 1)
            realE = "10"+realE if sign=="+" else "0."+realE+"1"
            number = str(PyFloat(nat) * PyFloat(realE))
        return number

    def __split(self, n):
        nSplited = n.split(".")
        nden = nSplited[0]
        nnum = nSplited[1] if len(nSplited) == 2 else ""
        nden, sign = (nden[1:], -1) if nden[0] == "-" else (nden, 1)
        return nden, nnum, sign

    def __getSign(self, n):
        return -1 if n[0]=="-" else 1

    def __fill(self, n0, n1, fillToRight=True):
        n0Len = len(n0)
        n1Len = len(n1)
        if n0Len > n1Len:
            n1Mod = n1
            diff = n0Len - n1Len
            for _ in range(0, diff):
                if fillToRight:
                    n1Mod += "0"
                else:
                    n1Mod = "0" + n1Mod
            return n0, n1Mod
        elif n0Len < n1Len:
            n0Mod = n0
            diff = n1Len - n0Len
            for _ in range(0, diff):
                if fillToRight:
                    n0Mod += "0"
                else:
                    n0Mod = "0" + n0Mod
            return n0Mod, n1
        else:
            return n0, n1
    
    def __clearZeros(self, n, left=True):
        if n =="0" or n == "":
            return "0"
        nresult = n
        while nresult!="" and nresult[0 if left else -1]=="0":
            nresult = nresult[1:] if left else nresult[:-1]
        return "0" if nresult == "" else nresult
    
    def __getZerosCount(self, n, left=True):
        if n=="0" or n == "":
            return 0
        i = 0
        nresult = n
        while nresult!="" and nresult[0 if left else -1]=="0":
            nresult = nresult[1:] if left else nresult[:-1]
            i += 1
        return i
    
    def __joinNumber(self, n, decimals, sign):
        # print("joinNumber " + n + " decimals " + str(decimals) + " sign " + sign)
        nNat = n[0:len(n)-decimals] if len(n)>decimals else "0"
        # print("2.nNat ..> " + nNat)
        # print("decimals " + str(decimals))
        # nNat = self.__clearZeros(nNat)
        # print("1.nNat ..> " + nNat)
        nReal = "" if decimals==0 else (n[-decimals:])
        # print("0.nReal ..> " + nReal)
        if len(n)<decimals:
            nReal = "0" * (decimals-len(n)) + nReal
        
        # print("1.nReal ..> " + nReal)
        nReal = self.__clearZeros(nReal, False)
        # print("2.nReal ..> " + nReal)
        number = sign + nNat + ("" if nReal=="0" else ("." + nReal))
        # print("number ==> " + number)
        return number

    def __compare(self, b):
        if self.__n == b:
            return 0

        aS,bS = self.__split(self.__n),self.__split(b)
        nDen = self.__fill(aS[0], bS[0], False)
        nNum = self.__fill(aS[1], bS[1])
        aS = ("" if aS[2]==1 else "-") + self.__clearZeros(nDen[0]) + nNum[0]
        bS = ("" if bS[2]==1 else "-") + self.__clearZeros(nDen[1]) + nNum[1]

        aSi = int(aS)
        bSi = int(bS)
        if aSi<bSi:
            return -1
        elif aSi>bSi:
            return 1
        else:
            return 0

    def __str__(self):
        return self.__n

    def __add__(self, o):
        a, b = self.__split(self.__n), self.__split(o.__n)
        nDen = self.__fill(a[0], b[0], False)
        nNum = self.__fill(a[1], b[1])
        aS = ("" if a[2]==1 else "-") + self.__clearZeros(nDen[0]) + nNum[0]
        bS = ("" if b[2]==1 else "-") + self.__clearZeros(nDen[1]) + nNum[1]
        result = str(int(aS) + int(bS))

        sign = "-" if result[0]=="-" else ""
        result = result if sign=="" else result[1:]
        result = self.__joinNumber(result, max(len(a[1]), len(b[1])), sign)
        return PyFloat(result)
    
    def __iadd__(self, o):
        return self + o

    def __sub__(self, o):
        a, b = self.__split(self.__n), self.__split(o.__n)
        nDen = self.__fill(a[0], b[0], False)
        nNum = self.__fill(a[1], b[1])
        aS = ("" if a[2]==1 else "-") + self.__clearZeros(nDen[0]) + nNum[0]
        bS = ("" if b[2]==1 else "-") + self.__clearZeros(nDen[1]) + nNum[1]
        result = str(int(aS) - int(bS))
        
        sign = "-" if result[0]=="-" else ""
        result = result if sign=="" else result[1:]
        result = self.__joinNumber(result, max(len(a[1]), len(b[1])), sign)
        return PyFloat(result)

    def __isub__(self, o):
        return self - o

    def __mul__(self, o):
        a, b = self.__split(self.__n), self.__split(o.__n)
        nDen = self.__fill(a[0], b[0], False)
        nNum = self.__fill(a[1], b[1])
        aS = nDen[0] + "-" + nNum[0]
        bS = nDen[1] + "-" + nNum[1]
        aS = self.__clearZeros(nDen[0]) + nNum[0]
        bS = self.__clearZeros(nDen[1]) + nNum[1]
        result = str(int(aS) * int(bS))

        decimalA, decimalB = len(a[1]), len(b[1])
        decimals = (decimalA + decimalB) if decimalA==decimalB else (max(decimalA,decimalB)*2)

        aZeros, bZeros = self.__getZerosCount(aS), self.__getZerosCount(bS)
        result = ("0" * 1 * max(aZeros, bZeros))+ result
        
        result = self.__joinNumber(result, decimals, "" if a[2]==b[2] else "-")
        return PyFloat(result)

    def __imul__(self, o):
        return e * o

    def __neg__(self):
        return self * PyFloat("-1")

    def __truediv__(self, o):
        return PyFloat("0")

    def __idiv__(self, o):
        return self/n

    def __lt__(self, o):
        c = self.__compare(o.__n) 
        return c==-1

    def __gt__(self, o):
        c = self.__compare(o.__n) 
        return c==1

    def __le__(self, o):
        c = self.__compare(o.__n) 
        return c<=0

    def __ge__(self, o):
        c = self.__compare(o.__n) 
        return c>=0

    def __eq__(self, o):
        c = self.__compare(o.__n) 
        return c==0

    def __ne__(self, o):
        c = self.__compare(o.__n) 
        return c!=0
class calc:
    def add(self, a, *b):
        ans = a
        for i in b:
            ans += i
        return ans

    def sub(self, a, *b):
        ans = a
        for i in b:
            ans -= i
        return ans

    def mul(self, a, *b):
        ans = a
        for i in b:
            ans *= i
        return ans

    def div(self, a, *b):
        ans = a * 1.0
        for i in b:
            ans /= i
        return ans
    
    def eq(self, a, *b):
        for i in b:
            if i != a:
                return False
        return True

    def gt:(self, a, *b):
        k = a
        for i in b:
            if k > i:
                k = i
            else:
                return False
        return True

    def lt:(self, a, *b):
        k = a
        for i in b:
            if k < i:
                k = i
            else:
                return False
        return True

    def le(self, a, *b):
        k = a
        for i in b:
            if k <= i:
                k = i
            else
                return False
        return True

    def ge(self, a, *b):
        k = a
        for i in b:
            if k >= i:
                k = i
            else
                return False
        return True
  
    def rem(self, a, b):
        ans = a % b
        if ans != 0 and a < 0:
            ans -= b

    def gcd(self, a, b):
        if a < b:
            a, b = b, a

        while b != 0:
            temp = a % b
            a = b
            b = temp

        return a

    def lcm(self, a, b)
        return a * b / self.gcd(a, b)

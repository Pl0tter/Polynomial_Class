import random


class Polynomial:
    upper_register = {1: '\u00B9', 2: '\u00B2', 3: '\u00B3', 4: '\u2074', 5: '\u2075',
                      6: '\u2076', 7: '\u2077', 8: '\u2078', 9: '\u2079', 0: '\u2070'}

    def __init__(self, poly: dict | str | int = '', upper_limit: int = 100,
                 lower_limit: int = 0):
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
        if isinstance(poly, dict):
            self.polynomial = poly
        elif isinstance(poly, str):
            self.polynomial = self.decode(poly)
        elif isinstance(poly, int):
            self.polynomial = self.create(poly)

    def create(self, max_order: int) -> dict:
        polynomial = {}
        for degree in range(max_order, -1, -1):
            coef = random.randint(self.lower_limit, self.upper_limit)
            if coef:
                polynomial[degree] = coef
        return polynomial

    def decode(self, poly: str) -> dict:
        polynomial = {}
        poly = poly.replace(' ', '').replace('+', ' ').replace('-', ' -').split()
        if poly[-1].endswith('=0'):
            poly[-1] = poly[-1][:-2]
        for item in poly:
            if '*x**' in item:
                term = item.split('*x**')
                polynomial[int(term[1])] = polynomial.get(int(term[1]), 0) + int(term[0])
            elif '*x' in item:
                term = item.replace('*x', '')
                polynomial[1] = int(term)
            else:
                polynomial[0] = int(item)
        zero_list = []
        for key, value in polynomial.items():
            if value == 0:
                zero_list.append(key)
        [polynomial.pop(key) for key in zero_list]
        return polynomial

    def __add__(self, other):
        result = {}
        overall_keys = list(set(list(self.polynomial.keys()) + list(other.polynomial.keys())))
        overall_keys.sort(reverse=True)
        for degree in overall_keys:
            result[degree] = self.polynomial.get(degree, 0) + other.polynomial.get(degree, 0)
        return Polynomial(poly=result)

    def __sub__(self, other):
        result = {}
        overall_keys = list(set(list(self.polynomial.keys()) + list(other.polynomial.keys())))
        overall_keys.sort(reverse=True)
        for degree in overall_keys:
            result[degree] = self.polynomial.get(degree, 0) - other.polynomial.get(degree, 0)
        return Polynomial(poly=result)

    def __repr__(self):
        poly = []
        keys = list(self.polynomial.keys())
        for degree in keys:
            if degree == 1 and self.polynomial.get(1):
                poly.append(f'{self.polynomial.get(1)}x')
            elif degree == 0 and self.polynomial.get(0):
                poly.append(f'{self.polynomial.get(0)}')
            else:
                upper_degree = ''.join([Polynomial.upper_register.get(int(i)) for i in str(degree)])
                coef = self.polynomial.get(degree)
                if coef > 0:
                    poly.append(f'{f"{coef}x" if coef != 1 else "x"}{upper_degree}')
                else:
                    poly.append(f'{f"{coef}x" if coef != -1 else "-x"}{upper_degree}')
        return ' + '.join(poly).replace(' + -', ' - ') + ' = 0'


poly_1 = Polynomial(poly=9)
poly_2 = Polynomial(poly='34*x**3 + 55*x**2 - 34*x**3 + 4*x**1 + 5 =   0')
print(poly_1)
print(poly_2)

print(poly_1 - poly_2)

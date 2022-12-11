
P = [{
    0: 0.5,
    5: 0.7,
    10: 0.8,
    15: 0.9,
    20: 0.95
},
{
    0: 0.7,
    5: 0.8,
    10: 0.9,
    15: 0.97,
    20: 0.99
}]

def part_a():
    for n in [3, 5, 10]:
        print("N=",n, end=': ')
        for d in [0,5,10,15,20]:
            prod = 1
            for _ in range(n):
                prod *= P[1][d]
            print(prod, end='\t')
        print()

def part_b():
    ans = {3: 15, 5: 20, 10: 20}
    Z = [1/3, 2/3]
    for n in [3, 5, 10]:
        print("N=",n, end=': ')
        prod = 1
        for _ in range(n):
            c = P[0][ans[n]] * Z[0]
            c += P[1][ans[n]] * Z[1]
            prod *= c
        print(1 - prod, prod)

def part_c():
    ans = {3: 15, 5: 20, 10: 20}
    Z = [1/3, 2/3]
    for n in [5]:
        for _ in range(n):
            c = (1 - P[0][ans[n]]) * Z[0]
            c += (1 - P[1][ans[n]]) * Z[1]
            print((1 - P[0][ans[n]])* Z[0] / c)
        

if __name__ == "__main__":
    part_c()
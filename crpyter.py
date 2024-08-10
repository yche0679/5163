import random

from sympy import mod_inverse

import random
from sympy import isprime, nextprime

def setup(n, alpha):
    # 寻找一个大素数 p 作为模数
    p = nextprime(1000)
    g = random.randint(2, p - 1)
    g1 = pow(g, alpha, p)
    g2 = random.randint(2, p - 1)

    # 创建 n x n 的矩阵 U
    U = [[random.randint(1, p - 1) for _ in range(n)] for _ in range(n)]
    k = random.randint(1, 100)  # 随机选择哈希函数的密钥

    master_key = pow(g2, alpha, p)
    params = {"g": g, "g1": g1, "g2": g2, "U": U, "k": k, "p": p}
    return params, master_key


def key_gen(params, ID, master_key):
    # 哈希 ID 到 {0,1}^w，这里简化为用整数表示
    hashed_id = sum([ord(char) for char in ID]) % params["p"]
    a = [random.randint(0, 1) for _ in range(10)]  # a 为 ID 的二进制哈希

    r = [random.randint(1, params["p"] - 1) for _ in range(len(params["U"]))]
    d_id = [pow(params["g2"], params["k"], params["p"])]
    d_id.extend([pow(params["g"], r[i], params["p"]) * pow(params["U"][i][0], r[i], params["p"]) % params["p"] for i in range(len(r))])

    return d_id

def encrypt(params, ID, M):
    t = random.randint(1, params["p"] - 1)
    C = [pow(params["g1"], t, params["p"]) * M % params["p"]]  # 注意模运算位置
    for u_i in params["U"]:
        C.append(pow(params["g"], t, params["p"]) * pow(u_i[0], t, params["p"]) % params["p"])
    return C


def decrypt(params, d_id, C):
    A = pow(C[0], d_id[0], params["p"])
    rest = C[1:]
    product = 1
    for cj, dj in zip(rest, d_id[1:]):
        product *= pow(cj, dj, params["p"])
    M = A * mod_inverse(product, params["p"]) % params["p"]  # 注意逆元的应用
    return M



# 设置环境和参数
n = 4
alpha = 5
params, master_key = setup(n, alpha)

# 用户ID和消息
ID = "user@example.com"
M = 123

# 生成密钥和加密消息
d_id = key_gen(params, ID, master_key)
C = encrypt(params, ID, M)

# 解密消息
decrypted_message = decrypt(params, d_id, C)

print(f"Original Message: {M}")
print(f"Decrypted Message: {decrypted_message}")

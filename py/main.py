import numpy as np
import math

def pairs(domains: list[str]) -> dict[str,str]:
    domain_len = len(domains)
    result = []

    for i in range(domain_len):
        for j in range(i + 1, domain_len):
            result.append((domains[i], domains[j]))
    
    return result

def top_k(domains: list[str], 
          k: int,
          window_len: int,
          threshold: float=0.70) -> list[str]:
    domain_len = len(domains)

    if (window_len > domain_len):
        print(f"ERROR: window length > domain list length ({window_len} > "
                                                         f"{domain_len})")
        exit(1)

    global_max = []

    print("Begin top-k computation:\n"
          f"  # domains = {domain_len}\n"
          f"  k = {k}\n"
          f"  window size = {window_len}\n"
          f"  threshold = {threshold}")

    for i in range(0, domain_len, window_len):
        window = domains[i:i+window_len]
        uniq_pairs = pairs(window)
        local_max = np.full(len(uniq_pairs), -1.0, dtype=np.float32)

        for j in range(len(uniq_pairs)):
            X, Y = uniq_pairs[j]
            ed = edit_distance(X, Y) 
            score = round(scoring(ed, len(X) if len(X) > len(Y) else len(Y)), 2)
            if score > threshold:
                local_max[j] = score
        idx = np.argpartition(local_max, -k)
        for id in idx[-k:]:
            # this checks if the current window returned at least k max scores
            if local_max[id] > 0:
                global_max.append(uniq_pairs[id])

    return global_max

def my_min(*args) -> int:
    min = args[0]
    for v in args:
        if v < min:
            min = v
    
    return min

def edit_distance(X: str, Y: str) -> int:
    len_X = len(X)
    len_Y = len(Y)

    if (len_X == 0):
        return len_Y
    elif (len_Y == 0):
        return len_X

    E: np.ndarray = np.zeros((len_X + 1, len_Y + 1), dtype=np.uint8)
    E[0] = np.arange(len_Y + 1)
    E[:,0] = np.arange(len_X + 1)

    for i in range(1, len_X + 1):
        for j in range(1, len_Y + 1):
            # deletion
            a = E[i - 1, j] + 1
            # insertion
            b = E[i, j - 1] + 1
            # substitution
            c = E[i - 1, j - 1] + (1 if X[i - 1] != Y[j - 1] else 0)

            E[i, j] = min(a,b,c)

    # print(reconstruct(E, X, Y))

    # return E[len_X - 1, len_Y - 1]
    return E[len_X, len_Y]

def reconstruct(E: np.ndarray, X: str, Y: str) -> list[str]:
    i = len(X)
    j = len(Y)

    L: list[str] = []

    while (i > 0 or j > 0):
        if i == 0:
            L.insert(0, f"Insert {Y[j - 1]} at beginning")
            j -= 1
        elif j == 0 or E[i, j] == 1 + E[i - 1, j]:
            L.insert(0, f"Delete {X[i - 1]}")
            i -= 1
        elif E[i, j] == 1 + E[i, j - 1]:
            L.insert(0, f"Insert {Y[j - 1]} after {X[i - 1]}") 
            j -= 1
        elif X[i - 1] == Y[j - 1]:
            i -= 1; j -= 1
        else:
            L.insert(0, f"Substitute {Y[j - 1]} for {X[i - 1]}")
            i -= 1; j -= 1

    return L

def gaussian(x: int, eds: list[int]) -> float:
    sigma = np.std(eds)
    mu = np.mean(eds)

    lhs = (1) / float(sigma * np.sqrt(2 * np.pi))
    print(lhs)
    rhs = np.exp(-0.5 * np.power(((x - mu) / sigma), 2))
    print(rhs)

    return lhs * rhs

def scoring(ed: int, max_ed: int) -> float:
    if ed == 0:
        return 1.0
    return 1 - (ed / float(max_ed))

def main() -> None:
    # with open(
    #         "/usr/local/opt/wordlists/seclists/" +
    #         "Passwords/darkweb2017-top100.txt",
    #         "r") as wordlist:

    #     domains = [d.strip() for d in wordlist.readlines()]

    #     for d1 in domains:
    #         for d2 in domains:
    #             if d1 != d2:
    #                 ed = edit_distance(d1, d2)
    #                 print(f"The edit distance of '{d1}' and '{d2}' is {ed}")
    """
        d1 = core.google.com
        d2 = c0r3.g00g13.com
    """
    d1 = "mail.google.com"
    d2 = "google.com"

    eds = np.empty(2, dtype=np.uint8)
    a = ''.join(d1.split('.')[0:-2])
    a_len = len(a)

    b = ''.join(d2.split('.')[0:-2])
    b_len = len(b)

    ed = edit_distance(a, b)
    eds[0] = ed

    c_len = len(c)

    d = ''.join(d2.split('.')[-2:-1])
    d_len = len(d)

    ed = edit_distance(c, d)
    eds[1] = ed

    domain_score, sub_score = (scoring(eds[0], np.max([a_len, b_len])),
                               scoring(eds[1], np.max([c_len, d_len])))

if __name__ == "__main__":
    with open("/usr/local/opt/wordlists/seclists/"
              "Discovery/DNS/shubs-subdomains.txt") as wordlist:
        words = [word.strip() for word in wordlist.readlines()[:1600] ]
        top_5 = top_k(words, 5, math.floor(0.25*len(words)), 0.60)
        print(top_5)


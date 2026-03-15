def execute(text1: str, text2: str) -> str:
    base = 131
    window_size = 3
    def rolling_hashes(s: str, w: int):
        if len(s) < w:
            return []
        h = 0
        p = 1
        for i in range(w):
            p *= base
        res = []
        for i, ch in enumerate(s):
            h = h * base + ord(ch)
            if i >= w:
                h -= ord(s[i - w]) * p
            if i >= w - 1:
                res.append(h)
        return res

    v1 = rolling_hashes(text1, window_size)
    v2 = rolling_hashes(text2, window_size)

    if not v1 or not v2:
        return "0.00%"

    set1 = set(v1)
    set2 = set(v2)
    common = set1 & set2
    same = len(common)

    total = len(v1) + len(v2)
    similarity = 2.0 * same / total if total > 0 else 0.0
    return f"{similarity*100:.2f}%"
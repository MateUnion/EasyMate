"""
字符串相似度计算工具
使用滚动哈希算法计算两个字符串的相似度（窗口大小为3字节）
"""

def execute(text1: str, text2: str) -> str:
    """
    计算两个字符串的相似度

    Args:
        text1: 第一个字符串
        text2: 第二个字符串

    Returns:
        相似度百分比，格式为 "XX.XX%"
    """
    # 基数和窗口大小
    base = 131
    window_size = 3

    def rolling_hashes(s: str, w: int):
        """
        计算字符串的滚动哈希值集合

        Args:
            s: 输入字符串
            w: 窗口大小

        Returns:
            哈希值列表
        """
        if len(s) < w:
            return []
        h = 0
        p = 1
        # 预计算base的w次方
        for i in range(w):
            p *= base
        res = []
        for i, ch in enumerate(s):
            # 更新哈希值
            h = h * base + ord(ch)
            if i >= w:
                # 移除窗口外的字符贡献
                h -= ord(s[i - w]) * p
            if i >= w - 1:
                # 记录窗口哈希值
                res.append(h)
        return res

    # 计算两个字符串的哈希值集合
    v1 = rolling_hashes(text1, window_size)
    v2 = rolling_hashes(text2, window_size)

    # 如果任一字符串长度小于窗口大小，返回0%
    if not v1 or not v2:
        return "0.00%"

    # 转换为集合，计算公共哈希值
    set1 = set(v1)
    set2 = set(v2)
    common = set1 & set2
    same = len(common)

    # 计算相似度：2 * 公共元素 / 总元素数
    total = len(v1) + len(v2)
    similarity = 2.0 * same / total if total > 0 else 0.0

    # 返回百分比
    return f"{similarity*100:.2f}%"

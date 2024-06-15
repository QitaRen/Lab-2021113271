# --*-- coding:utf-8 --*--
"""
项目：
作者：Wang
日期：2024年06月11日
"""

import networkx as nx
from collections import Counter


def query_bridge_words(graph, word1, word2):
    """
    在有向图 graph 中找到 word1 和 word2 之间的桥接词并返回。

    参数:
    graph (networkx.DiGraph): 有向图。
    word1 (str): 第一个词。
    word2 (str): 第二个词。

    返回:
    str: 一个指示桥接词或缺乏桥接词的信息。
    """
    word1 = word1.lower()
    word2 = word2.lower()
    if word1 not in graph and word2 not in graph:#两个词都不在图中
        return f'No "{word1}" and "{word2}" in the graph!'
    if word1 not in graph:#第一个词不在图中
        return f'No "{word1}" in the graph!'
    if word2 not in graph:#第二个词不在图中
        return f'No "{word2}" in the graph!'

    # 查找桥接词：在 word1 的后继节点中找到那些也是 word2 的前驱节点的词
    bridge_words = [node for node in graph.nodes() if word1 in
                    graph.predecessors(node) and word2 in graph.successors(node)]

    if not bridge_words:#没有桥接词
        return f'No bridge words from "{word1}" to "{word2}"!'
    if len(bridge_words) == 1:#一个桥接词
        return f'The bridge word from "{word1}" to "{word2}" is: {bridge_words[0]}.'
    bridge_words_list = ", ".join(bridge_words[:-1])
    return (f'The bridge words from "{word1}" to "{word2}" are: {bridge_words_list},'
            f' and {bridge_words[-1]}.')#多个桥接词


def create_graph(wordlist):
    """
    根据词列表创建有向图。

    参数:
    wordlist (list): 词列表。

    返回:
    networkx.DiGraph: 生成的有向图。
    """
    G = nx.DiGraph()
    dic = Counter(wordlist)
    for v in dic:
        G.add_node(v)
    edgeslist = []
    for i, v in enumerate(wordlist):
        if i >= 1:
            edge = wordlist[i - 1] + ' ' + v
            edgeslist.append(edge)
    edge_num = Counter(edgeslist)
    for k, v in edge_num.items():
        edge_div_list = k.split()
        G.add_edge(edge_div_list[0], edge_div_list[1], weight=v)
    return G


def test_create_graph():
    words = ["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]
    graph = create_graph(words)
    return graph


def test_query_bridge_words():
    graph = test_create_graph()

    # 测试用例 1: 两个词都不在图中
    assert query_bridge_words(graph, "cat", "mouse") == 'No "cat" and "mouse" in the graph!'

    # 测试用例 2: 第一个词不在图中
    assert query_bridge_words(graph, "cat", "quick") == 'No "cat" in the graph!'

    # 测试用例 3: 第二个词不在图中
    assert query_bridge_words(graph, "quick", "mouse") == 'No "mouse" in the graph!'

    # 测试用例 4: 一个桥接词
    assert query_bridge_words(graph, "the", "brown") == 'The bridge word from "the" to "brown" is: quick.'

    # 测试用例 5: 没有桥接词
    assert query_bridge_words(graph, "quick", "dog") == 'No bridge words from "quick" to "dog"!'

    # 测试用例 6: 多个桥接词
    words = ["the", "quick", "brown", "fox", "quick", "lazy", "fox","dog"]
    graph = create_graph(words)
    assert query_bridge_words(graph, "quick", "fox") == 'The bridge words from "quick" to "fox" are: brown, and lazy.'

    print("All tests passed!")


test_query_bridge_words()

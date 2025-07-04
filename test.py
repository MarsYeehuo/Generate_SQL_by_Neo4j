# coding=utf8

from embed import get_embedding
from sklearn.metrics.pairwise import cosine_similarity
from neomodel import db
import numpy as np

def test_all_similarities(query, top_k=20):
    qv = np.array(get_embedding(query)).reshape(1, -1)
    res, _ = db.cypher_query("MATCH (n:NLP) RETURN n.text, n.embedding")

    scores = []
    for text, vec in res:
        if vec:
            sim = cosine_similarity(qv, [vec])[0][0]
            scores.append((text, sim))

    scores.sort(key=lambda x: x[1], reverse=True)
    print(f"\n与查询 \"{query}\" 的相似度前 {top_k}：\n")
    for text, score in scores[:top_k]:
        print(f"  - {text:<25} 相似度：{score:.4f}")

if __name__ == '__main__':
    q = input("请输入待测试的自然语言：\n> ")
    test_all_similarities(q)

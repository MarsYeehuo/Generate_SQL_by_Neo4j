# coding=utf8

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from models import Unit
from neomodel import db
from embed import get_embedding

def find_similar_units(query, top_k=3):
    qv = np.array(get_embedding(query)).reshape(1, -1)
    results, _ = db.cypher_query("MATCH (n:NLP) RETURN id(n), n.embedding, n.text")
    vectors, ids, texts = [], [], []

    for nid, vec, text in results:
        if vec:
            vectors.append(vec)
            ids.append(nid)
            texts.append(text)

    if not vectors:
        print("没有任何有效的向量数据，是否已经执行 embed 命令？")
        return []

    sims = cosine_similarity(qv, np.array(vectors))[0]
    sorted_idx = sims.argsort()[::-1][:top_k]

    print(f"\n与问题 “{query}” 的相似度排名：")
    for i in sorted_idx:
        print(f"  - {texts[i]}  → 相似度：{sims[i]:.4f}")

    unit_ids = []
    for i in sorted_idx:
        res, _ = db.cypher_query(
            "MATCH (n:NLP)-[:DESCRIBED_IN]->(u:Unit) WHERE id(n) = $id RETURN u.uid",
            {"id": ids[i]}
        )
        if res:
            unit_ids.append(res[0][0])
    return unit_ids


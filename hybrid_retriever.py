# coding=utf8
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
from embed import get_embedding
from neomodel import db
from unit_association_trigger import expand_units_by_weight
from update_weight import update_association_weights
import numpy as np
import jieba


class HybridRetriever:
    def __init__(self):
        self.unit_records = []
        self.texts = []
        self.embeddings = []
        self.tokenized = []
        self.bm25 = None

    def load_from_graph(self):
        self.unit_records = []
        self.texts = []
        self.embeddings = []
        self.tokenized = []

        query = """
        MATCH (n:NLP)
        OPTIONAL MATCH (u:Unit)-[:DESCRIBE_IN]->(n)
        RETURN u.uid, n.text, n.embedding
        """

        res, _ = db.cypher_query(query)
        for uid, text, emb in res:
            if text and emb:
                self.unit_records.append((uid, text))
                self.texts.append(text)
                self.embeddings.append(emb)
                self.tokenized.append(list(jieba.cut(text)))
        self.bm25 = BM25Okapi(self.tokenized)

    def find_units(self, query_text: str, top_k: int = 8, alpha: float = 0.6):
        if not self.bm25:
            self.load_from_graph()

        query_text = (
            query_text.replace("最近半年", "近半年")
            .replace("过去半年", "近半年")
            .replace("近6个月", "近半年")
        )

        query_vec = np.array(get_embedding(query_text)).reshape(1, -1)
        bm25_tokens = list(jieba.cut(query_text))

        bm25_scores = self.bm25.get_scores(bm25_tokens)
        sim_scores = cosine_similarity(query_vec, np.array(self.embeddings))[0]

        combined = []
        for i, (uid, text) in enumerate(self.unit_records):
            final_score = alpha * sim_scores[i] + (1 - alpha) * (bm25_scores[i] / (np.max(bm25_scores) + 1e-6))
            combined.append((uid, text, final_score))

        combined.sort(key=lambda x: x[2], reverse=True)
        top_units = [x[0] for x in combined[:top_k]]

        # 联想拓展 + 权重更新
        expanded = expand_units_by_weight(top_units, threshold=5)
        update_association_weights(expanded)
        return expanded


if __name__ == '__main__':
    retriever = HybridRetriever()
    while True:
        q = input("请输入自然语言问题：\n> ")
        units = retriever.find_units(q)
        print("\n 唤起单元：", units)

# coding=utf8

import requests
from neomodel import db
from models import NLP
import ollama
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('shibing624/text2vec-base-chinese')

def get_embedding(text: str) -> list:
    return model.encode(text).tolist()

def update_all_nlp_embeddings():
    results, _ = db.cypher_query("MATCH (n:NLP) RETURN id(n), n.text")
    for node_id, text in results:
        vector = get_embedding(text)
        db.cypher_query("MATCH (n) WHERE id(n) = $id SET n.embedding = $vec",
                        {"id": node_id, "vec": vector})
    print("NLP 向量更新完成")

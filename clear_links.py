# coding=utf8

from neomodel import db

def clear_associations():
    db.cypher_query("MATCH (u1:Unit)-[r:ASSOCIATED_WITH]->(u2:Unit) DELETE r")
    print("已清除所有 Unit 之间的关联边")

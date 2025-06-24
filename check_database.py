# coding=utf8

from neomodel import db
res, _ = db.cypher_query("CALL db.info() YIELD name RETURN name")
print("当前连接的数据库名称是：", res[0][0])

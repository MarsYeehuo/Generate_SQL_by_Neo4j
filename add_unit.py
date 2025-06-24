# coding=utf8

from models import NLP, Explanation, Field, Unit
import uuid

def create_new_unit():
    nl = input("自然语言：").strip()
    ex = input("解释说明：").strip()
    table = input("表名：").strip()
    col = input("字段名：").strip()
    if not all([nl, ex, table, col]):
        print("输入不完整")
        return

    n, _ = NLP.get_or_create({"text": nl})
    e, _ = Explanation.get_or_create({"text": ex})
    f, _ = Field.get_or_create({"table": table, "column": col})

    u = Unit(uid="unit_" + str(uuid.uuid4())[:8]).save()
    u.described_by.connect(n)
    u.explained_by.connect(e)
    u.maps_to.connect(f)

    print(f"创建完成：{u.uid}")

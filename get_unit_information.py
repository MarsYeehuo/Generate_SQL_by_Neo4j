# coding=utf8
from neomodel import db
import sys


def get_unit_info_by_uid(uid: str):
    query = """
    MATCH (u:Unit {uid: \"""" + uid + """\"})
    OPTIONAL MATCH (u)-[:DESCRIBE_IN]->(n:NLP)
    OPTIONAL MATCH (u)-[:EXPLAINS]->(e:EXPLANATION)
    OPTIONAL MATCH (u)-[:MAPS_TO]->(f:Field)
    OPTIONAL MATCH (t:Table)-[:HAS_FIELD]->(f)
    RETURN
      u.uid AS unit_id,
      n.text AS nlp_text,
      e.text AS explanation_text,
      f.name AS field_name,
      f.type AS field_type,
      f.nullable AS field_nullable,
      t.name AS table_name
    """
    # print(query)
    results, _ = db.cypher_query(query, {"uid": uid})

    info_list = []
    for row in results:
        unit_id, nlp_text, expl_text, field_name, field_type, nullable, table_name = row
        info_list.append({
            "unit_id": unit_id,
            "nlp": nlp_text,
            "explanation": expl_text,
            "field_name": field_name,
            "field_type": field_type,
            "nullable": nullable,
            "table_name": table_name
        })

    return info_list


'''
def get_unit_info_by_field_name(field_name: str):
    query = """
    MATCH (f:Field)
    WHERE f.name = $field_name
    OPTIONAL MATCH (t:Table)-[:HAS_FIELD]->(f)
    OPTIONAL MATCH (u:Unit)-[:MAPS_TO]->(f)
    OPTIONAL MATCH (u)-[:DESCRIBE_IN]->(n:NLP)
    OPTIONAL MATCH (u)-[:EXPLAINS]->(e:EXPLANATION)
    RETURN
        u.uid AS unit_id,
        t.name AS table_name,
        n.text AS nlp_text,
        n.embedding AS nlp_embedding,
        e.text AS explanation
    LIMIT 1
    """
    results, _ = db.cypher_query(query, {"field_name": field_name})
    if not results or not results[0]:
        return None

    row = results[0]
    return {
        "unit_id": row[0],
        "table_name": row[1],
        "nlp_text": row[2],
        "embedding": row[3],
        "explanation": row[4]
    }

'''
if __name__ == "__main__":
    try:
        uid = input("请输入 Unit ID（如 unit_011）：").strip()
        info_list = get_unit_info_by_uid(uid)
        if not info_list:
            print("未找到该 Unit。")
        else:
            for i, info in enumerate(info_list, 1):
                print(f"\n--- 第 {i} 条关联信息 ---")
                print(f"单元 ID: {info['unit_id']}")
                print(f"关键词: {info.get('nlp', '无')}")
                print(f"解释: {info.get('explanation', '无')}")
                print(f"字段: {info['field_name']} (类型: {info['field_type']}, 可空: {info['nullable']})")
                print(f"所属表: {info['table_name']}")

    except KeyboardInterrupt:
        print("\n操作中断")
        sys.exit(0)

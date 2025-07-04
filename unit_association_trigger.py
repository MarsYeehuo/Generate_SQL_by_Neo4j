# coding=utf8
from typing import Tuple, List

from models import Unit, Table
from neomodel import db


def get_associated_units_with_weight(uid: str, threshold: int = 5) -> list:
    source = Unit.nodes.get(uid=uid)
    results = []

    if source.associated is not None:
        for target in source.associated.all():
            rel = source.associated.relationship(target)
            if rel and rel.weight >= threshold:
                results.append(target.uid)

    return results


def expand_units_by_weight(initial_units: list, threshold: int = 5) -> tuple[list[list], list[str]]:
    """
    输入一组unit，返回包含联想单元的扩展列表。
    同时返回对应扩展的表结构信息（表名、字段名）。
    """
    expanded_uids = set(initial_units)
    table_infos = set()

    for uid in initial_units:
        related = get_associated_units_with_weight(uid, threshold)
        expanded_uids.update(related)

    # 提取结构信息：表名 + 字段名
    for uid in expanded_uids:
        query = """
        MATCH (u:Unit {uid: $uid})-[:MAPS_TO]->(f:Field)
        OPTIONAL MATCH (t:Table)-[:HAS_FIELD]->(f)
        RETURN DISTINCT t.name AS table_name, f.name AS field_name
        """
        results, _ = db.cypher_query(query, {'uid': uid})
        for table_name, field_name in results:
            if table_name and field_name:
                table_infos.add(f"[{table_name}] {field_name}")

    return list(expanded_uids), sorted(table_infos)

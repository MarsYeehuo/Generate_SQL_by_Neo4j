# coding=utf8

from models import Unit


def get_associated_units_with_weight(uid: str, threshold: int = 5) -> list:
    source = Unit.nodes.get(uid=uid)
    results = []

    if source.associated is not None:
        for target in source.associated.all():
            rel = source.associated.relationship(target)
            if rel and rel.weight >= threshold:
                results.append(target.uid)

    return results



def expand_units_by_weight(initial_units: list, threshold: int = 5) -> list:
    """
    输入一组unit，返回包含联想单元的扩展列表。
    """
    expanded = set(initial_units)
    for uid in initial_units:
        related = get_associated_units_with_weight(uid, threshold)
        expanded.update(related)
    return list(expanded)

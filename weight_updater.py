# coding=utf8

from models import Unit

def update_weights(unit_ids):
    for i in range(len(unit_ids)):
        for j in range(i + 1, len(unit_ids)):
            u1 = Unit.nodes.get(uid=unit_ids[i])
            u2 = Unit.nodes.get(uid=unit_ids[j])
            rel = u1.associated.relationship(u2)
            if rel:
                rel.weight += 1
                rel.save()
            else:
                u1.associated.connect(u2, {'weight': 1})

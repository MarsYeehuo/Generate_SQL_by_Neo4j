def update_association_weights(retrieved_uids: list):
    from models import Unit
    retrieved_set = set(retrieved_uids)
    visited_pairs = set()

    units = Unit.nodes.all()
    for u in units:
        for other in u.associated.all():
            pair = tuple(sorted((u.uid, other.uid)))
            if pair in visited_pairs:
                continue
            visited_pairs.add(pair)

            rel = u.associated.relationship(other)

            in_both = u.uid in retrieved_set and other.uid in retrieved_set
            in_either = u.uid in retrieved_set or other.uid in retrieved_set

            if in_both:
                if not rel:
                    u.associated.connect(other, {'weight': 1})
                else:
                    rel.weight += 1
                    rel.save()
            elif in_either and rel:
                rel.weight -= 1
                if rel.weight <= 0:
                    u.associated.disconnect(other)
                else:
                    rel.save()

    # 检查未连边但都在召回内的组合 → 建新边
    for i in range(len(retrieved_uids)):
        for j in range(i + 1, len(retrieved_uids)):
            uid1 = retrieved_uids[i]
            uid2 = retrieved_uids[j]
            if uid1 == uid2:
                continue
            u1 = Unit.nodes.get(uid=uid1)
            u2 = Unit.nodes.get(uid=uid2)
            if not u1.associated.relationship(u2):
                u1.associated.connect(u2, {'weight': 1})


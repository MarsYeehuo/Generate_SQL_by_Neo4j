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

            rel1 = u.associated.relationship(other)
            rel2 = other.associated.relationship(u)

            in_both = u.uid in retrieved_set and other.uid in retrieved_set
            in_either = u.uid in retrieved_set or other.uid in retrieved_set

            if in_both:
                if not rel1:
                    u.associated.connect(other, {'weight': 1})
                else:
                    rel1.weight += 1
                    rel1.save()

                if not rel2:
                    other.associated.connect(u, {'weight': 1})
                else:
                    rel2.weight += 1
                    rel2.save()

            elif in_either:
                if rel1:
                    rel1.weight -= 1
                    if rel1.weight <= 0:
                        u.associated.disconnect(other)
                    else:
                        rel1.save()
                if rel2:
                    rel2.weight -= 1
                    if rel2.weight <= 0:
                        other.associated.disconnect(u)
                    else:
                        rel2.save()

    # 检查未连边但都在召回内的组合 → 建双向边
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
            if not u2.associated.relationship(u1):
                u2.associated.connect(u1, {'weight': 1})

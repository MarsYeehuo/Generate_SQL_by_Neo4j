from neomodel import StructuredNode, StringProperty, BooleanProperty, RelationshipTo, RelationshipFrom, StructuredRel, IntegerProperty


class AssociationRel(StructuredRel):
    weight = IntegerProperty(default=1)

class Table(StructuredNode):
    name = StringProperty(required=True)
    fields = RelationshipTo('Field', 'HAS_FIELD')


class Field(StructuredNode):
    name = StringProperty(required=True)
    type = StringProperty()
    nullable = BooleanProperty()
    table = RelationshipFrom('Table', 'HAS_FIELD')


class NLP(StructuredNode):
    text = StringProperty(required=True)
    # described_in = RelationshipTo('Unit', 'DESCRIBED_IN')


class Explanation(StructuredNode):
    text = StringProperty(required=True)
    # explains = RelationshipTo('Unit', 'EXPLAINS')


class Unit(StructuredNode):
    uid = StringProperty(unique_index=True, required=True)
    described_by = RelationshipTo('NLP', 'DESCRIBED_IN')
    explained_by = RelationshipTo('Explanation', 'EXPLAINS')
    maps_to = RelationshipTo('Field', 'MAPS_TO')
    associated = RelationshipTo('Unit', 'ASSOCIATED_WITH', model=AssociationRel)

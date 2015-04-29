# coding: utf-8
from jsl import (StringField, ArrayField, Var, DictField,
                 NotField, Document, DocumentField)
from jsl.fields.compound import BaseOfField


a = StringField()
b = StringField()
c = StringField()
d = StringField()
e = StringField()
f = StringField()
g = StringField()
h = StringField()
j = StringField()


def test_array_field():
    field = ArrayField(Var({
        'role_1': a,
        'role_2': b,
        'role_none': None,
    }), additional_items=Var({
        'role_3': c,
        'role_4': d,
        'role_1': e,
        'role_none': None,
    }))
    assert set(field.iter_fields()) == set([a, b, c, d, e])
    assert set(field.resolve_and_iter_fields('role_1')) == set([a, e])
    assert set(field.resolve_and_iter_fields('role_3')) == set([c])
    assert set(field.resolve_and_iter_fields('role_none')) == set([])

    field = ArrayField(Var({
        'role_1': (a, b),
        'role_2': c
    }), additional_items=d)
    assert set(field.iter_fields()) == set([a, b, c, d])

    field = ArrayField((Var({'role_1': a, 'role_2': b, 'role_none': None}), c))
    assert set(field.iter_fields()) == set([a, b, c])
    assert set(field.resolve_and_iter_fields('role_1')) == set([a, c])
    assert set(field.resolve_and_iter_fields('role_none')) == set([c])

    field = ArrayField(a, additional_items=b)
    assert set(field.iter_fields()) == set([a, b])
    assert set(field.resolve_and_iter_fields('some_role')) == set([a, b])

    field = ArrayField()
    assert set(field.iter_fields()) == set([])


def test_dict_field():
    field = DictField(properties=Var({
        'role_1': {
            'a': Var({
                'role_a': a,
                'role_none': None,
            }),
            'b': b,
            'role_none': None,
        },
        'role_2': {'c': c},
        'role_none': None,
    }), pattern_properties=Var({
        'role_3': {
            'x*': Var({
                'role_b': d,
                'role_none': None,
            }),
        },
        'role_4': {'y*': e},
        'role_none': None,
    }), additional_properties=Var({
        'role_5': f,
        'role_6': g,
        'role_none': None,
    }))
    assert set(field.iter_fields()) == set([a, b, c, d, e, f, g])

    field = DictField(
        properties={'a': a},
        pattern_properties={'b': b},
        additional_properties=c
    )
    assert set(field.iter_fields()) == set([a, b, c])

    field = DictField()
    assert set(field.iter_fields()) == set([])


def test_base_of_field():
    field = BaseOfField((a, b))
    assert set(field.iter_fields()) == set([a, b])

    field = BaseOfField(Var({
        'role_1': (a, b),
        'role_2': c,
        'role_3': None,  # probably should raise?
    }))
    assert set(field.iter_fields()) == set([a, b, c])


def test_not_field():
    field = NotField(a)
    assert set(field.iter_fields()) == set([a])
    assert set(field.resolve_and_iter_fields('some_role')) == set([a])

    field = NotField(Var({
        'role_1': a,
        'role_2': b,
        'role_3': None,  # probably should raise?
    }))
    assert set(field.iter_fields()) == set([a, b])
    assert set(field.resolve_and_iter_fields('role_1')) == set([a])
    assert set(field.resolve_and_iter_fields('role_3')) == set([])


def test_document_field():
    class A(Document):
        a = a
        b = b

    field = DocumentField(A)
    assert set(field.iter_fields()) == set([a, b])

    class B(Document):
        field = Var({
            'a': a,
            'b': b
        })
        b = c

    field = DocumentField(B)
    assert set(field.iter_fields()) == set([a, b, c])

    class C(Document):
        pass

    field = DocumentField(C)
    assert set(field.iter_fields()) == set([])

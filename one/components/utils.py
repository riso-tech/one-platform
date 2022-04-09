"""
Reusable function for components
"""
from one.components.constants import EXCLUDE_FIELDS


def _get_name_fields(fields, exclude=[]):
    """Get list name of normal field"""
    return [
        field.name
        for field in fields
        if field.concrete
        and not (
            field.is_relation
            or field.one_to_one
            or (field.many_to_one and field.related_model)
        )
        and field.name not in EXCLUDE_FIELDS + exclude
    ]


def _get_fields(fields, exclude=[]):
    """Get list of normal field"""
    return [
        field
        for field in fields
        if field.concrete
        and not (
            field.is_relation
            or field.one_to_one
            or (field.many_to_one and field.related_model)
        )
        and field.name not in EXCLUDE_FIELDS + exclude
    ]


def _get_lookups(field):
    """List of lookups for field"""
    return list(field.get_lookups())


def _get_o2o_fields(fields):
    """Get list of nested field in o2o fields"""
    o2o_fields = [
        field
        for field in fields
        if field.one_to_one and field.name not in EXCLUDE_FIELDS
    ]
    _fields = []
    for o2o in o2o_fields:
        related_model = o2o.related_model
        # noinspection PyProtectedMember
        meta = related_model._meta
        _fields.append(
            {
                "name": meta.model_name,
                "fields": _get_fields(meta.get_fields(include_parents=False), ["id"]),
            }
        )
    return _fields

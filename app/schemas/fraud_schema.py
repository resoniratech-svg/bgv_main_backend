from marshmallow import Schema, fields, validate, ValidationError


class StrictBoolean(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, bool):
            raise ValidationError("Must be a boolean.")
        return value


class FraudRequestSchema(Schema):
    candidate_id = fields.Integer(required=True)
    duplicate_document = StrictBoolean(required=True)
    employment_overlap = StrictBoolean(required=True)
    credit_score = fields.Integer(
        required=True,
        validate=validate.Range(min=300, max=900)
    )

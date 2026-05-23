from marshmallow import Schema, fields


class BGVRequestSchema(Schema):
    id = fields.Int(dump_only=True)
    candidate_name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    verification_type = fields.Str(required=True)
    status = fields.Str()
    trust_score = fields.Float()
    remarks = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
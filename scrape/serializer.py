from marshmallow import Schema, fields


class ScrapeRequestSchema(Schema):
    url = fields.String(required=True)
    limit = fields.Integer(required=True)


class ErrorResponseSchema(Schema):
    type = fields.String(required=True)
    value = fields.String(required=True)
    message = fields.String(required=True)


class FailureResponseSchema(Schema):
    success = fields.Boolean(required=True)
    error = fields.List(fields.Nested(ErrorResponseSchema), required=True)

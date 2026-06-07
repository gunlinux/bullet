"""marshmallow schema of ``app/data/users.json`` (DummyJSON users payload).

Field names keep the original camelCase JSON keys so the schemas map onto the
data without aliasing.
"""

from __future__ import annotations

from marshmallow import Schema, fields

from app.schema.common import Role


class Coordinates(Schema):
    lat = fields.Float(required=True)
    lng = fields.Float(required=True)


class Address(Schema):
    address = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)
    stateCode = fields.Str(required=True)
    postalCode = fields.Str(required=True)
    coordinates = fields.Nested(Coordinates, required=True)
    country = fields.Str(required=True)


class Hair(Schema):
    color = fields.Str(required=True)
    type = fields.Str(required=True)


class Bank(Schema):
    cardExpire = fields.Str(required=True)
    cardNumber = fields.Str(required=True)
    cardType = fields.Str(required=True)
    currency = fields.Str(required=True)
    iban = fields.Str(required=True)


class Company(Schema):
    department = fields.Str(required=True)
    name = fields.Str(required=True)
    title = fields.Str(required=True)
    address = fields.Nested(Address, required=True)


class Crypto(Schema):
    coin = fields.Str(required=True)
    wallet = fields.Str(required=True)
    network = fields.Str(required=True)


class User(Schema):
    id = fields.Int(required=True)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    maidenName = fields.Str(required=True)  # may be an empty string
    age = fields.Int(required=True)
    gender = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    birthDate = fields.Str(required=True)
    image = fields.Url(required=True)
    bloodGroup = fields.Str(required=True)
    height = fields.Float(required=True)
    weight = fields.Float(required=True)
    eyeColor = fields.Str(required=True)
    hair = fields.Nested(Hair, required=True)
    ip = fields.Str(required=True)
    address = fields.Nested(Address, required=True)
    macAddress = fields.Str(required=True)
    university = fields.Str(required=True)
    bank = fields.Nested(Bank, required=True)
    company = fields.Nested(Company, required=True)
    ein = fields.Str(required=True)
    ssn = fields.Str(required=True)
    userAgent = fields.Str(required=True)
    crypto = fields.Nested(Crypto, required=True)
    role = fields.Enum(Role, by_value=True, required=True)


class UsersResponse(Schema):
    users = fields.List(fields.Nested(User), required=True)
    total = fields.Int(required=True)
    skip = fields.Int(required=True)
    limit = fields.Int(required=True)

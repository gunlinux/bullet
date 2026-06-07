"""msgspec struct of ``app/data/users.json`` (DummyJSON users payload).

Field names keep the original camelCase JSON keys so the structs map onto the
data without aliasing.
"""

from __future__ import annotations

import msgspec

from app.schema.common import Role


class Coordinates(msgspec.Struct):
    lat: float
    lng: float


class Address(msgspec.Struct):
    address: str
    city: str
    state: str
    stateCode: str
    postalCode: str
    coordinates: Coordinates
    country: str


class Hair(msgspec.Struct):
    color: str
    type: str


class Bank(msgspec.Struct):
    cardExpire: str
    cardNumber: str
    cardType: str
    currency: str
    iban: str


class Company(msgspec.Struct):
    department: str
    name: str
    title: str
    address: Address


class Crypto(msgspec.Struct):
    coin: str
    wallet: str
    network: str


class User(msgspec.Struct):
    id: int
    firstName: str
    lastName: str
    maidenName: str  # may be an empty string
    age: int
    gender: str
    email: str
    phone: str
    username: str
    password: str
    birthDate: str
    image: str
    bloodGroup: str
    height: float
    weight: float
    eyeColor: str
    hair: Hair
    ip: str
    address: Address
    macAddress: str
    university: str
    bank: Bank
    company: Company
    ein: str
    ssn: str
    userAgent: str
    crypto: Crypto
    role: Role


class UsersResponse(msgspec.Struct):
    users: list[User]
    total: int
    skip: int
    limit: int

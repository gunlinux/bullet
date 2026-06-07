"""pydantic model of ``app/data/users.json`` (DummyJSON users payload).

Field names keep the original camelCase JSON keys so the models map onto the
data without aliasing.
"""

from __future__ import annotations

import pydantic

from app.schema.common import Role


class Coordinates(pydantic.BaseModel):
    lat: float
    lng: float


class Address(pydantic.BaseModel):
    address: str
    city: str
    state: str
    stateCode: str
    postalCode: str
    coordinates: Coordinates
    country: str


class Hair(pydantic.BaseModel):
    color: str
    type: str


class Bank(pydantic.BaseModel):
    cardExpire: str
    cardNumber: str
    cardType: str
    currency: str
    iban: str


class Company(pydantic.BaseModel):
    department: str
    name: str
    title: str
    address: Address


class Crypto(pydantic.BaseModel):
    coin: str
    wallet: str
    network: str


class User(pydantic.BaseModel):
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


class UsersResponse(pydantic.BaseModel):
    users: list[User]
    total: int
    skip: int
    limit: int

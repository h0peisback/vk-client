import attr
from vk_client import validators
from vk_client.entities._base import Entity, entity_manager


@attr.s
class User(Entity):

    id = attr.ib(validator=validators.positive)


@attr.s
class UserManager(entity_manager(User)):
    pass

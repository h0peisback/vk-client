import more_itertools as mit
import cached_property
from vk_client import config, errors, utils, validators
from vk_client.models import base, mixins


class Group(
    base.Model,
    mixins.HasId
):
    def __init__(self, vk, id):
        assert validators.negative(id)

        super(Group, self).__init__(vk)

        self._id = id

    @property
    def name(self):
        return self._data["name"]

    @property
    def screen_name(self):
        return self._data["screen_name"]

    def get_posts(self):
        return self._vk.Post.from_owner(self)

    @cached_property.cached_property
    def _data(self):
        response = self._vk.api.groups.getById(group_id=-self.id)
        try:
            return mit.one(response)
        except ValueError:
            raise errors.NotFound(self)


class GroupManager(base.ModelManager):

    _model = Group

    @utils.flattened()
    @utils.exhausted(step=config.SEARCH_CHUNK_SIZE)
    def from_search(self, q, offset, count):
        return [
            self(
                id=-item["id"]
            )
            for item in self._vk.api.groups.search(
                offset=offset,
                count=count,
                q=q
            )["items"]
        ]

    @utils.flattened()
    @utils.exhausted(step=config.SEARCH_CHUNK_SIZE)
    def from_user(self, user, offset, count):
        return [
            self(
                id=-item
            )
            for item in self._vk.api.groups.get(
                user_id=user.id,
                offset=offset,
                count=count
            )["items"]
        ]

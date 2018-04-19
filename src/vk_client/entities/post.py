import attr
from vk_client import config
from vk_client.enums import LikableType
from vk_client.utils import offset_range
from vk_client.entities._base import Entity, entity_manager
from vk_client.entities._mixins import make_likable_mixin, OwnedMixin


@attr.s
class Post(
    Entity,
    make_likable_mixin(LikableType.POST),
    OwnedMixin
):
    """
    TODO: Add description.
    """


@attr.s
class PostManager(entity_manager(Post)):

    def count_liked(self):
        response = self._vk.api.fave.getPosts(count=1)
        return response["count"]

    def get_liked(self, count=config.FAVE_CHUNK_SIZE_DEFAULT):
        chunks = offset_range(0, count, config.FAVE_CHUNK_SIZE_MAX)
        for offset, chunk_size in chunks:
            response = self._vk.api.fave.getPosts(
                count=chunk_size,
                offset=offset
            )
            for item in response["items"]:
                yield self(
                    id=item["id"],
                    owner_id=item["owner_id"]
                )
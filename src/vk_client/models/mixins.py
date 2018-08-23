from vk_client import errors


class HasVk(object):

    _vk = NotImplemented


class HasData(object):

    _data = NotImplemented


class HasId(object):

    _id = NotImplemented

    @property
    def id(self):
        return self._id


class Authored(HasVk, HasId):

    _author_id = NotImplemented

    # TODO: Move to User class.
    @property
    def author_is_user(self):
        return self._author_id > 0

    # TODO: Move to Group class.
    @property
    def author_is_group(self):
        return self._author_id < 0

    @property
    def author(self):
        if self.author_is_user:
            return self._vk.User(id=self._author_id)
        elif self.author_is_group:
            return self._vk.Group(id=self._author_id)
        else:
            raise errors.Unreachable


class Owned(HasVk, HasId):

    _owner_id = NotImplemented

    @property
    def full_id(self):
        return "{}_{}".format(self._owner_id, self.id)

    # TODO: Move to User class.
    @property
    def owner_is_user(self):
        return self._owner_id > 0

    # TODO: Move to Group class.
    @property
    def owner_is_group(self):
        return self._owner_id < 0

    @property
    def owner(self):
        if self.owner_is_user:
            return self._vk.User(id=self._owner_id)
        elif self.owner_is_group:
            return self._vk.Group(id=self._owner_id)
        else:
            raise errors.Unreachable


class Likable(HasData, Owned):

    _likable_type = NotImplemented

    @property
    def likes_count(self):
        return self._data["likes"]["count"]

    @property
    def can_like(self):
        return not self.is_liked

    @property
    def is_liked(self):
        return bool(self._data["likes"]["user_likes"])

    def like(self):
        if self.can_like:
            self._vk.api.likes.add(
                type=self._likable_type.value,
                owner_id=self._owner_id,
                item_id=self.id
            )
            del self._data

    def unlike(self):
        if self.is_liked:
            self._vk.api.likes.delete(
                type=self._likable_type.value,
                owner_id=self._owner_id,
                item_id=self.id
            )
            del self._data

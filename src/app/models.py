from behaviors.behaviors import Slugged, Timestamped
from django.db import models
from mptt.models import MPTTModel as _MPTTModel
from mptt.models import TreeForeignKey, TreeManager

__all__ = [
    "DefaultModel",
    "TimestampedModel",
    "SluggedModel",
    "MPTTModel",
    "TreeForeignKey",
    "models",
]


class DefaultModel(models.Model):
    """Use this model as base for all your models."""

    class Meta:
        abstract = True

    def r(self):
        """A shortcut to refresh and return itself."""
        self.refresh_from_db()
        return self

    def update_from_kwargs(self, **kwargs):
        """
        A shortcut method to update model instance from the kwargs.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def setattr_and_save(self, key, value):
        """Shortcut for testing -- set attribute of the model and save"""
        setattr(self, key, value)
        self.save()


class TimestampedModel(DefaultModel, Timestamped):
    """Default app model that has `created` and `updated` attributes."""

    class Meta:
        abstract = True


class SluggedModel(Slugged, TimestampedModel):
    """Default app model that has required `slug` field."""

    @property
    def slug_source(self):
        return self.name

    class Meta:
        abstract = True


class MPTTModel(_MPTTModel, TimestampedModel):
    objects = TreeManager()

    class Meta:
        abstract = True

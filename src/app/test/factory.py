from typing import TYPE_CHECKING

from faker import Faker
from mixer.backend.django import mixer

if TYPE_CHECKING:
    from inventory.models import InventoryItem, InventoryOwner, Product
    from marketplace.models import Listing, Marketplace, MarketplaceItem
    from regions.models import Region
    from warehouse.models import Warehouse, WarehouseItem


class CycleFactory:
    def __init__(self, factory: "Factory", count: int):
        self.factory = factory
        self.count = count

    def __getattr__(self, name):
        if hasattr(self.factory, name):
            return lambda *args, **kwargs: [
                getattr(self.factory, name)(*args, **kwargs) for _ in range(self.count)
            ]


class Factory:
    faker = Faker()

    @classmethod
    def cycle(cls, count):
        return CycleFactory(cls, count)

    @classmethod
    def item(cls, bound=True, **kwargs) -> "InventoryItem":
        owner = kwargs.pop("owner", None) or cls.owner()
        item = mixer.blend(
            "inventory.InventoryItem", owner=owner, product=None, **kwargs
        )
        if bound:
            item.binder.bind_with_new()
        return item

    @classmethod
    def product(cls, **kwargs) -> "Product":
        return mixer.blend("inventory.Product", **kwargs)

    @classmethod
    def warehouse_item(cls, **kwargs) -> "WarehouseItem":
        item = kwargs.pop("item", None)
        warehouse = kwargs.pop("warehouse", None)

        if warehouse and not item:
            item = cls.item(owner=warehouse.owner)
        elif not warehouse and item:
            warehouse = cls.warehouse(owner=item.owner)
        elif not warehouse and not item:
            item = cls.item()
            warehouse = cls.warehouse(owner=item.owner)

        return mixer.blend(
            "warehouse.WarehouseItem",
            warehouse=warehouse,
            inventory_item=item,
            **kwargs
        )

    @classmethod
    def warehouse(cls, **kwargs) -> "Warehouse":
        name = kwargs.pop("name", None) or cls.faker.word()
        region = kwargs.pop("region", None) or cls.region()
        owner = kwargs.pop("owner", None) or cls.owner()
        return mixer.blend("warehouse.Warehouse", owner=owner, name=name, region=region, **kwargs)

    @classmethod
    def owner(cls, **kwargs) -> "InventoryOwner":
        return mixer.blend("inventory.InventoryOwner", **kwargs)

    @classmethod
    def marketplace(cls, **kwargs) -> "Marketplace":
        return mixer.blend("marketplace.Marketplace", **kwargs)

    @classmethod
    def listing(cls, **kwargs) -> "Listing":
        name = kwargs.pop("name", None) or cls.faker.word()
        marketplace = kwargs.pop("marketplace", None) or cls.marketplace()
        return mixer.blend(
            "marketplace.Listing", marketplace=marketplace, name=name, **kwargs
        )

    @classmethod
    def marketplace_item(cls, **kwargs) -> "MarketplaceItem":
        listing = kwargs.pop("listing", None) or cls.listing()
        item = mixer.blend(
            "marketplace.MarketplaceItem", marketplace=listing.marketplace, **kwargs
        )
        item.listings.add(listing)

        return item

    @classmethod
    def region(cls, **kwargs) -> "Region":
        name = kwargs.pop("name", None) or cls.faker.word()
        return mixer.blend(
            "regions.Region", name=name, **kwargs
        )

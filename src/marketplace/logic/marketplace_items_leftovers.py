from django.core.cache import cache
from django.shortcuts import get_object_or_404

from marketplace.models import Listing, Marketplace, MarketplaceItem


class MarketplaceItemsLeftOvers:
    def __init__(self, listing_pk: str, marketplace: Marketplace | None) -> None:
        self.listing_pk = listing_pk
        self.marketplace = marketplace

    def fetch_queryset_for_listing_items(self):
        cache_key = f"marketplace_items_{self.listing_pk}_{self.marketplace.pk if self.marketplace else 'global'}"
        if cached := cache.get(cache_key):
            return cached

        listing = self._get_listing()
        region = listing.region
        queryset = MarketplaceItem.objects.filter(
            listings__id=listing.pk,
        ).distinct()
        queryset = (
            queryset.select_related("product")
            .prefetch_related(
                "product__inventory_items", "product__inventory_items__warehouse_items"
            )
            .annotate_product_total_stock(region=region)
            .annotate_product_min_price(region=region)
            .annotate_product_max_price(region=region)
        )
        queryset = queryset.order_by("id")

        result = queryset
        cache.set(cache_key, result, 600)
        return result

    def _get_listing(self) -> Listing:
        filters = {"id": self.listing_pk}

        if self.marketplace:
            filters["marketplace"] = self.marketplace

        return get_object_or_404(Listing, **filters)

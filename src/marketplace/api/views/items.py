from rest_framework.viewsets import ReadOnlyModelViewSet

from app.permissions import MarketplaceOnly, StuffAndSuperUserOnly
from marketplace.api.serializers import SimpleListingItemSerializer
from marketplace.logic.marketplace_items_leftovers import MarketplaceItemsLeftOvers


class ListingItemViewSet(ReadOnlyModelViewSet):
    serializer_class = SimpleListingItemSerializer
    permission_classes = [StuffAndSuperUserOnly | MarketplaceOnly]

    def get_queryset(self):
        return MarketplaceItemsLeftOvers(
            listing_pk=self.kwargs["listing_pk"],
            marketplace=self.request.marketplace
        ).fetch_queryset_for_listing_items()

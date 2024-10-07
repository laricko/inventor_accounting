from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from inventory.api.item_action_views import (
    AddToListingView,
    Item2ItemBinderView,
    Item2NewBinderView,
    ItemFromItemUnBinderView,
    RemoveFromListingView,
)
from inventory.api.views import (
    InventoryGroupedItemsView,
    InventoryItemsViewSet,
    InventoryOwnersViewSet,
    ProductsView,
)
from marketplace.api.views import ListingItemViewSet, ListingViewSet, MarketplaceViewSet

# Viewsets:

router_v1 = DefaultRouter()

# Inventory viewsets

router_v1.register("inventory/items", InventoryItemsViewSet)
router_v1.register("inventory/owners", InventoryOwnersViewSet)

# Marketplace viewsets

router_v1.register("marketplace/listings", ListingViewSet)
router_v1.register("marketplace/marketplaces", MarketplaceViewSet)

listing_router = NestedDefaultRouter(
    router_v1, "marketplace/listings", lookup="listing"
)
listing_router.register(r"items", ListingItemViewSet, "listing_item")

# Views:

api_v1 = (
    path("", include(router_v1.urls)),
    # Inventory views
    path("inventory/products/<int:pk>/", ProductsView.as_view()),
    path("inventory/items/<int:item_id>/bind_with/new/", Item2NewBinderView.as_view()),
    path(
        "inventory/items/<int:item_id>/bind_with/<int:item_to_bind_id>/",
        Item2ItemBinderView.as_view(),
    ),
    path(
        "inventory/items/<int:item_id>/unbind_from/<int:item_to_unbind_id>/",
        ItemFromItemUnBinderView.as_view(),
    ),
    path(
        "inventory/items/<int:item_id>/add_to_listing/<int:listing_id>/",
        AddToListingView.as_view(),
    ),
    path(
        "inventory/items/<int:item_id>/remove_from_listing/<int:listing_id>/",
        RemoveFromListingView.as_view(),
    ),
    path("inventory/grouped_items/", InventoryGroupedItemsView.as_view()),
    # Marketplace views
    path("", include(listing_router.urls)),
)

urlpatterns = [
    path("api/v1/", include((api_v1, "api"), namespace="v1")),
    path("admin/", admin.site.urls),
]

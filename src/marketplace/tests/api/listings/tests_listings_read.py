import pytest

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    "get",
    (
        (lambda api, listings: api.get("/api/v1/marketplace/listings/")["results"][0]),
        (lambda api, listings: api.get(f"/api/v1/marketplace/listings/{listings.id}/")),
    ),
)
def test_read_listing(api, listing, get):
    got = get(api, listing)

    assert got["id"] == listing.pk
    assert got["name"] == listing.name
    assert got["items_count"] == 0
    assert "marketplace" in got


def test_read_marketplace_listing(api, listing, marketplace):
    got = api.get(f"/api/v1/marketplace/listings/{listing.id}/")

    got = got["marketplace"]
    assert got["id"] == marketplace.pk
    assert got["name"] == marketplace.name
    assert got["slug"] == marketplace.slug


def test_read_items_count(api, factory, listing):
    factory.cycle(3).marketplace_item(listing=listing)

    got = api.get(f"/api/v1/marketplace/listings/{listing.id}/")

    assert got["items_count"] == 3


def test_read_only_current_listing_items_count(api, factory, listing):
    factory.cycle(3).marketplace_item(listing=factory.listing())  # Other listing items

    got = api.get(f"/api/v1/marketplace/listings/{listing.id}/")

    assert got["items_count"] == 0


@pytest.mark.parametrize(
    "is_stuff, is_superuser, expected_status_code",
    [[False, False, 403], [True, False, 200], [False, True, 200]],
)
def test_allowed_for_stuff_and_superuser(
    api, is_stuff, is_superuser, expected_status_code
):
    api.user.is_staff = is_stuff
    api.user.is_superuser = is_superuser
    api.user.save()

    api.get("/api/v1/marketplace/listings/", expected_status_code=expected_status_code)


def test_allowed_for_marketplace(api, marketplace):
    marketplace.setattr_and_save("user", api.user)

    api.get("/api/v1/marketplace/listings/")


def test_marketplace_can_get_only_own_listings(api, marketplace, listing, factory):
    marketplace.setattr_and_save("user", api.user)
    another_listing = factory.listing()

    got = api.get("/api/v1/marketplace/listings/")["results"]

    assert listing.pk in [obj["id"] for obj in got]
    assert another_listing.pk not in [obj["id"] for obj in got]

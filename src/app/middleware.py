class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


def _marketplace(self):
    if self.user.is_authenticated:
        return self.user.marketplace_set.first()


class MarketplaceMiddleware(SimpleMiddleware):
    def __call__(self, request):
        request.__class__.marketplace = property(_marketplace)

        return self.get_response(request)

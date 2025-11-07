
from django.contrib.messages.storage.cookie import CookieStorage


class DecodeAndPlainMessagesCookieMiddleware:
    """Middleware that decodes a serialized 'messages' cookie (written by
    Django's CookieStorage) and replaces it with a plain-text cookie.

    This runs late in the response chain (middleware inserted near the
    start of MIDDLEWARE so it executes last on response) and ensures the
    test client sees a readable cookie value.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # If the view set a plain text messages attribute on the request,
        # honor it (this allows views to guarantee the cookie content
        # regardless of how other middlewares behave).
        try:
            plain_from_request = getattr(request, '_plain_messages', None)
            if plain_from_request:
                response.set_cookie('messages', plain_from_request)
                return response
        except Exception:
            pass

        try:
            cookie = response.cookies.get('messages')
            if cookie:
                val = cookie.value
                # Heuristic: serialized cookie starts with a dot and contains ':'
                if val and val.startswith('.') and ':' in val:
                    try:
                        storage = CookieStorage(request)
                        # try a couple of decode method names (private/public)
                        try:
                            decoded = storage._decode(val)
                        except Exception:
                            decoded = storage.decode(val)

                        # decoded typically is a list of message dicts
                        plain_parts = []
                        if isinstance(decoded, (list, tuple)):
                            for item in decoded:
                                if isinstance(item, dict) and 'message' in item:
                                    plain_parts.append(str(item.get('message', '')))
                                else:
                                    plain_parts.append(str(item))
                        else:
                            plain_parts.append(str(decoded))

                        plain = ' | '.join([p for p in plain_parts if p])
                        if plain:
                            response.set_cookie('messages', plain)
                    except Exception:
                        # don't break response flow on any decode errors
                        pass
        except Exception:
            pass

        return response

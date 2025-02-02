from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Exempt CSRF validation for login and logout.
    """

    def enforce_csrf(self, request):
        return

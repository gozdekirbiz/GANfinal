from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        user = request.user
        if user.is_superuser or user.is_staff:
            return False
        else:
            return super().is_open_for_signup(request)

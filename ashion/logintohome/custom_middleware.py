from .models import Customer


class BlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            "email" in request.session
            and Customer.objects.filter(email=request.session["email"]).exists()
        ):
            user = Customer.objects.get(email=request.session["email"])
            if user.is_blocked:
                del request.session["email"]
                # messages.error(request, "Admin blocked from accessing this page.")
                # return redirect('login')

        return self.get_response(request)

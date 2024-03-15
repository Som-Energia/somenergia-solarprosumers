from django.urls import reverse


class LoginMixin:
    def login(self, user):
        login_resp = self.client.post(
            reverse("token_obtain_pair"),
            data={"username": user.username, "password": "1234"},
            format="json",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="{} {}".format(
                "Bearer", login_resp.json().get("access", "")
            )
        )

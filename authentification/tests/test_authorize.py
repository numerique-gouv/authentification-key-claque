from django.test import TestCase

from authentification.tests.factories import ClientFactory, RedirectUriFactory


class TestAuthorizationInvalidRequests(TestCase):
    def test_empty_request_is_invalid(self):
        response = self.client.get("/authorize/")
        self.assertEqual(response.status_code, 400)
        response = self.client.post("/authorize/")
        self.assertEqual(response.status_code, 400)

    def test_with_one_missing_required(self):
        invalid_data = {
            "scope": "invalid-scope",
            "response_type": "invalid-content",
            "client_id": "anything",
            "redirect_uri": "not-even-an-uri",
        }
        for required_parameter in invalid_data.keys():
            request_data = invalid_data.copy()
            request_data.pop(required_parameter)
            response = self.client.get("/authorize/", data=request_data)
            self.assertEqual(
                response.status_code,
                400,
                f"Authorize should return an invalidrequest when required parameter {required_parameter} is missing",
            )
            response = self.client.post("/authorize/", data=request_data)
            self.assertEqual(
                response.status_code,
                400,
                (
                    "Authorize should return an invalidrequest "
                    f"when required parameter {required_parameter} is missing"
                ),
            )

    def test_scope_contains_openid(self):
        request_data = {
            "scope": "",
            "response_type": "invalid-content",
            "client_id": "anything",
            "redirect_uri": "https://use-an-uri.com",
        }
        invalid_scopes = ("invalid-scope", "openidd email", "open id", "email phone")
        for invalid_scope in invalid_scopes:
            request_data["scope"] = invalid_scope
            response = self.client.post("/authorize/", data=request_data)
            self.assertEqual(
                response.status_code,
                400,
                (
                    "Authorize should return an invalidrequest "
                    f"when scope parameter is {invalid_scope}"
                ),
            )
            response = self.client.get("/authorize/", data=request_data)
            self.assertEqual(
                response.status_code,
                400,
                (
                    "Authorize should return an invalidrequest "
                    f"when scope parameter is {invalid_scope}"
                ),
            )

    def test_check_response_type_is_code(self):
        request_data = {
            "scope": "openid",
            "response_type": "invalid-content",
            "client_id": "anything",
            "redirect_uri": "https://use-an-uri.com",
        }
        response = self.client.post("/authorize/", data=request_data)
        self.assertEqual(
            response.status_code,
            400,
            (
                "Authorize should return an invalidrequest "
                "when response_type is not code"
            ),
        )
        response = self.client.get("/authorize/", data=request_data)
        self.assertEqual(
            response.status_code,
            400,
            (
                "Authorize should return an invalidrequest "
                "when response_type is not code"
            ),
        )


class TestAuthorizationChecksClientId(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first_client = ClientFactory(
            client_id="first_client_id",
            name="My first client",
            client_secret="first_client_secret",
        )
        RedirectUriFactory(
            uri="https://www.first-client.com/oidc-callback",
            name="Main callback",
            client=cls.first_client,
        )

    def test_the_factory_works(self):
        self.assertEqual(
            self.first_client.redirecturi_set.first().uri,
            "https://www.first-client.com/oidc-callback",
        )

    def test_refuse_invalid_client_id(self):
        request_data = {
            "scope": "openid something",
            "response_type": "code",
            "client_id": "anything",
            "redirect_uri": "https://use-an-uri.com",
        }
        response = self.client.post("/authorize/", data=request_data)
        self.assertEqual(
            response.status_code,
            403,
            ("Authorize should return a forbidden when client_id is wrong"),
        )

    def test_refuse_invalid_redirect_uri(self):
        request_data = {
            "scope": "openid something",
            "response_type": "code",
            "client_id": "first_client_id",
            "redirect_uri": "https://unrelated-uri.com",
        }
        response = self.client.post("/authorize/", data=request_data)
        self.assertEqual(
            response.status_code,
            403,
            ("Authorize should returnn error when provided redirect uri is unknown"),
        )

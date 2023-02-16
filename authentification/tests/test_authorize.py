from django.test import TestCase


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
                f"Authorize should return an invalidrequest when required parameter {required_parameter} is missing",
            )
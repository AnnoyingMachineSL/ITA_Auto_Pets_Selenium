class ValidateResponse:

    @staticmethod
    def validate_response(response, model, status_code=None):
        if status_code is not None:
            assert response.status_code == status_code
        return model.model_validate(response.json())

    @staticmethod
    def validate_status_code(response, expected_status_code):
        if isinstance(expected_status_code, int):
            assert response.status_code == expected_status_code
        else:
            assert response.status_code == expected_status_code[0] or response.status_code == expected_status_code[1]
        return response
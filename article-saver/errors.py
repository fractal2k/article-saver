class ClickUpException(Exception):
    """Raised when a ClickUp API call fails for whatever reason.
    """

    def __init__(self, response, message):
        status_code = response.status_code
        error_message = response.text

        self.message = (
            f"{message}\nResponse code: {status_code}\nError message: {error_message}"
        )

        super().__init__(self.message)

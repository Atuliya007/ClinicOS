from fastapi import HTTPException, status


class DoctorNotFoundException(
    HTTPException,
):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )


class DoctorConflictException(HTTPException):
    def __init__(self, detail: str = "Doctor phone number already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

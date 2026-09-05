from fastapi import HTTPException, status


class PatientNotFoundException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )


class PatientConflictException(HTTPException):
    def __init__(self, detail: str = "Patient phone number already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

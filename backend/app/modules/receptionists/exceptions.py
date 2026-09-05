from fastapi import HTTPException, status


class ReceptionistNotFoundException(HTTPException):
    def __init__(self): super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Receptionist not found")


class ReceptionistConflictException(HTTPException):
    def __init__(self, detail="Receptionist phone number or email already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

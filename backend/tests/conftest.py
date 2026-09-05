import os
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.dependencies import get_db
from app.main import app
# Register all tables before metadata creation.
from app.modules.appointments import models as appointment_models  # noqa: F401
from app.modules.billing import models as billing_models  # noqa: F401
from app.modules.departments import models as department_models  # noqa: F401
from app.modules.doctors import models as doctor_models  # noqa: F401
from app.modules.laboratory import models as laboratory_models  # noqa: F401
from app.modules.patients import models as patient_models  # noqa: F401
from app.modules.pharmacy import models as pharmacy_models  # noqa: F401
from app.modules.receptionists import models as receptionist_models  # noqa: F401


@pytest.fixture()
def client():
    engine = create_engine("sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    app.dependency_overrides[get_db] = lambda: factory()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)

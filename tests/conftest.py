import pytest
from app import app, db


@pytest.fixture
def client():
    # Config for testing
    app.config["TESTING"] = True
    # In CI, this URL comes from the 'env' in your pipeline.yml

    with app.test_client() as client:
        with app.app_context():
            # Create tables in the CI's temporary Postgres
            db.create_all()
            yield client  # This is where the test happens

            # Cleanup after the test is done
            db.session.remove()
            db.drop_all()

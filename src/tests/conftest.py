import pytest

from src import create_app, db


@pytest.fixture(scope='module')
def test_app():
    # create instance from app factory
    app = create_app()

    # add test config
    app.config.from_object('src.config.TestConfig')
    with app.app_context():
        yield app # testing happens here


@pytest.fixture(scope='module')
def test_database():
    db.create_all()
    yield db # testing happens here

    # remove db after testing is done
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='module')
def client(test_app):
    return test_app.test_client()
    

from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import event
from sqlalchemy.orm.session import Session

from database import engine, get_db
from main import app


@fixture
def db():
    # https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
    engine.echo = True
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    global nested
    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def end_savepoint(_, __):  # type: ignore
        global nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@fixture
def client(db: Session):
    app.dependency_overrides[get_db] = lambda: db
    return TestClient(app, raise_server_exceptions=False)

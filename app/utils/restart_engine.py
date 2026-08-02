from app.database.configuration import engine


def restart_en():
    engine.dispose()
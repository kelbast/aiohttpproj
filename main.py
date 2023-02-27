from aiohttp import web
import jinja2
import aiohttp_jinja2

from app.settings import config, BASE_DIR
from app.store.database.accessor import PostgresAccessor


def setup_config(application):
    application["config"] = config


def setup_routes(application):
    from app.forum.routes import setup_routes as setup_forum_routes
    setup_forum_routes(application)


def setup_external_libraries(application: web.Application) -> None:
    aiohttp_jinja2.setup(
        application,
        loader=jinja2.FileSystemLoader(f"{BASE_DIR}/templates"))


def setup_accessors(application):
    application['db'] = PostgresAccessor()
    application['db'].setup(application)


def setup_app(application):
    setup_config(application)
    setup_accessors(application)
    setup_external_libraries(application)
    setup_routes(application)


app = web.Application()

if __name__ == "__main__":
    setup_app(app)
    web.run_app(app, port=config["common"]["port"])

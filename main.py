from modal import (
    Image,
    Mount,
    NetworkFileSystem,
    Secret,
    Stub,
    asgi_app,
)

from fastapi import FastAPI

web_app = FastAPI()

app_image = Image.debian_slim()

stub = Stub("11ty-homepage", image=app_image)


@stub.function(
    mounts=[Mount.from_local_dir("_site", remote_path="/_site")],
)
@asgi_app()
def fastapi_app():
    import starlette.staticfiles

    web_app.mount(
        "/",
        starlette.staticfiles.StaticFiles(directory="/_site", html=True),
    )
    # web_app.mount(
    #     "/readme/",
    #     starlette.staticfiles.StaticFiles(directory="/_site/README/"),
    # )

    return web_app

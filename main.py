from modal import (
    Image,
    Mount,
    Volume,
    Stub,
    asgi_app,
)

from fastapi import FastAPI

web_app = FastAPI()

app_image = Image.debian_slim()

stub = Stub("11ty-homepage", image=app_image)
stub.volume = Volume.persisted("site-11ty")


@stub.function(
    volumes={"/_site": stub.volume},
    keep_warm=1,
)
@asgi_app()
def fastapi_app():
    import starlette.staticfiles

    stub.volume.reload()
    web_app.mount(
        "/",
        starlette.staticfiles.StaticFiles(directory="/_site", html=True),
    )

    return web_app

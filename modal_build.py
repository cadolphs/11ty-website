from modal import Image, Volume, Stub, Mount

image = (
    Image.debian_slim()
    .apt_install("curl")
    .run_commands(
        [
            "curl -fsSL https://deb.nodesource.com/setup_21.x | bash - && apt-get install -y nodejs"
        ]
    )
    .run_commands(["npm install -g @11ty/eleventy"])
    .run_commands(["mkdir -p /remote_dir/_site"])
)


stub = Stub("11ty-homepage-builder", image=image)
stub.volume = Volume.persisted("site-11ty")


@stub.function(
    volumes={"/remote_dir/_site": stub.volume},
    mounts=[Mount.from_local_dir("./content", remote_path="/remote_dir")],
)
def build():
    import os

    try:
        os.system("cd /remote_dir && npx @11ty/eleventy")
    except:
        return {"status": "error"}

    stub.volume.commit()

    return {"status": "success"}

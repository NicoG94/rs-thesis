import kfp
import kfp.dsl as dsl
from kfp.compiler import Compiler

#1. mount volume
#2. download data from gcs
#3 print data
@dsl.pipeline(
    name = "hello world pipeline",
    description="demo pipe"
)
def hello_word():
    vop = dsl.VolumeOp(
        name="create_pvc",
        resource_name="my-pvc",
        size="2Gi",
        modes=dsl.VOLUME_MODE_RWM
    )

    step1 = dsl.ContainerOp(
        name = "download",
        image = "google/cloud-sdk:295.0.0-slim",
        command = ["gsutil", "cp", "-r"],
        arguments = ["gs://raw_movie_data", "/mnt"],
        pvolumes={"/mnt": vop.volume}
    )

    step2 = dsl.ContainerOp(
        name="step2",
        image="library/bash:4.4.23",
        command=["sh", "-c"],
        arguments=["ls", "/mnt"],
        pvolumes={"/mnt": step1.pvolume}
    )

    step3 = dsl.ContainerOp(
        name="step3",
        image="library/bash:4.4.23",
        command=["cat", "/mnt/raw_movie_data/links.csv", "/mnt/raw_movie_data/ratings.csv"],
        pvolumes={"/mnt": step2.pvolume}
    )

Compiler().compile(hello_word, 'volume_check.zip')

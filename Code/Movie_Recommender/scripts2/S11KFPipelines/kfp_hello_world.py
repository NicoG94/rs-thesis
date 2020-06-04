import kfp
import kfp.dsl as dsl
from kfp.compiler import Compiler

@dsl.pipeline(
    name = "hello world pipeline",
    description="demo pipe"
)
def hello_word():

    op1 = dsl.ContainerOp(
        name = "download",
        image = "google/cloud-sdk:216.0.0",
        command = ["gsutil", "cp"],
        arguments = ["gs://kfp-demo/hello.txt", "."]
    )

    op2 = dsl.ContainerOp(
        name="print",
        image="libary/bash:4.4.23",
        command=["echo"],
        arguments=[op1.output]
    )

Compiler().compile(hello_word, 'kfp_hello_world.zip')

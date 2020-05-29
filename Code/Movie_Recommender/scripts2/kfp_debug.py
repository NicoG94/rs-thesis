r"""
import kfp
host="http://10.10.10.10:8080/"
client = kfp.Client(host=host)#other_client_id for IAP auf GCP
print(client.list_experiments())
experiment = client.create_experiment(name="test_exp")
print(experiment)
"""
r"""
import kfp
from kfp import compiler
import kfp.dsl as dsl
import kfp.components as comp

def func1():
    return 5

def func2():
    return 6

func1_op = comp.func_to_container_op(func1, packages_to_install=["pandas", "numpy"])
func2_op = comp.func_to_container_op(func2, base_image="python:3", packages_to_install=["pandas", "numpy"])

####### create pipeline function #######
@dsl.pipeline(
    name="test_pipeline",
    description="this is a test"
)
def pipe():
    func1_task = func1_op()
    func2_task = func2_op()

####### export pipeline function #######
pipeline_filename = pipe.__name__ + "test_pipeline.tar.gz"
compiler.Compiler().compile(pipeline_func=pipe,
                          package_path=pipeline_filename)
"""



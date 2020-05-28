# https://github.com/kubeflow/pipelines/blob/master/samples/core/xgboost_training_cm/xgboost_training_cm.py
# https://kubeflow-pipelines.readthedocs.io/en/latest/index.html

import kfp
from kfp import compiler
import kfp.dsl as dsl
import kfp.gcp as gcp
import kfp.notebook
import kfp_server_api
import kfp.components as comp
import json

HOME=r"C:\Users\nicog\OneDrive\3. Semester - Masterthesis\Code\Movie_Recommender"

from scripts2.S01Datenbeschaffung.mergeData import get_coll_filt_data
from scripts2.S03DataPreparation.pivotData import get_pivot_data
from scripts2.S04Modelling.surprise2 import train_algo

####### pipeline operations #######
get_data_op = comp.func_to_container_op(get_coll_filt_data)
pivot_data_op = comp.func_to_container_op(get_pivot_data)
train_algo_op = comp.func_to_container_op(train_algo)

####### create pipeline function #######
@dsl.pipeline(
    name="test_pipeline",
    description="this is a test"
)
def rs_kfp(
        # specify params for op_functions here
        test_param1:int = 3,
        test_param2:str = "A",
        train_algo_test_param:str = "test_param"
):

    get_data_task = get_data_op()

    pivot_data_task = pivot_data_op()

    train_algo_task = train_algo_op(train_algo_test_param = train_algo_test_param, test_output = get_data_task.output)


####### export pipeline function #######
pipeline_filename = rs_kfp.__name__ + "pipeline.tar.gz"
compiler.Compiler().compile(pipeline_func=rs_kfp,
                          package_path=pipeline_filename)


####### create / reuse experiment #######
host="http://10.10.10.10:8080/"
host="ml-pipeline.kubeflow.svc.cluster.local:8888"
client = kfp.Client(host=host)#other_client_id for IAP auf GCP

EXPERIMENT_NAME = "Next - rs_kfp"

try:
    experiment = client.create_experiment(name=EXPERIMENT_NAME)
except Exception as e:
    print(f"{host} has exception: {e}")

try:
    experiment = client.get_experiment(experiment_name=EXPERIMENT_NAME)
except:
    experiment = client.create_experiment(EXPERIMENT_NAME)


####### submit RUN #######
run_name = rs_kfp.__name__ + " run"
run_result = client.run_pipeline(experiment.id, run_name, pipeline_filename)

print(run_result)

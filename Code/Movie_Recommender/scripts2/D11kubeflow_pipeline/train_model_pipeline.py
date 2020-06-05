#importing KFP pipeline
from kfp.dsl import pipeline
import kfp.dsl as dsl
from kfp.compiler import Compiler

r"""
def get_data_op():
    return dsl.ContainerOp(
        name = 'get_data', # name of the operation
        image = 'rsthesis/get_data_image:latest', #docker location in registry
        file_outputs = {
            'blob-path': '/blob_path.txt' #name of the file with result
        },
        #container_kwargs={"image_pull_policy": "Always"}
    )

def prepare_data_op(blob_path):
    return dsl.ContainerOp(
        name = 'prepare_data', # name of operation
        image = 'rsthesis/prepare_data_image:latest', #docker location in registry
        arguments = ["--blob_path", blob_path], #get_data_op.output, # passing step_1.output as argument
        command=["python", "prepare_data.py"]
        #file_outputs = {
        #    'blob-path': '/blob_path.txt' #name of the file with result
        #},
        #container_kwargs = {"image_pull_policy": "Always"}
   )
"""
def create_pvc_op():
    return dsl.VolumeOp(
        name="create_pvc",
        resource_name="my-pvc",
        size="2Gi",
        modes=dsl.VOLUME_MODE_RWM
    )

def download_data_op(vol, pvc_path):
    return dsl.ContainerOp(
        name = "download_data",
        image = "google/cloud-sdk:295.0.0-slim",
        command = ["gsutil", "cp", "-r"],
        arguments = ["gs://raw_movie_data", pvc_path],
        pvolumes={pvc_path: vol}
    )

def merge_data_op(input_path, output_path, vol, pvc_path):
    return dsl.ContainerOp(
        name = 'merge_data', # name of the operation
        image = 'rsthesis/get_data_image:latest', #docker location in registry
        file_outputs = {
            'data_output': output_path #name of the file with result
        },
        arguments=['--input_path',  input_path, '--output_path', output_path],
        container_kwargs={"image_pull_policy": "Always"},
        command=["python", "get_data.py"],
        pvolumes={pvc_path: vol}
    )

def prepare_data_op(input_path, output_path, pvc_path, vol):
    return dsl.ContainerOp(
        name = 'prepare_data',
        image = 'rsthesis/prepare_data_image:latest',
        arguments = ['--input_path',  dsl.InputArgumentPath(input_path), '--output_path', output_path],
        command=["python", "prepare_data.py"],
        file_outputs = {
            'data_output': output_path
        },
        pvolumes={pvc_path: vol},
        container_kwargs = {"image_pull_policy": "Always"}
   )

# defining pipeline meta
@pipeline(
    name='Train recommender modell',
    description='Train recommender modell pipeline'
)
# stitch the steps
def train_recommender_model_pipeline(pvc_path = "/mnt"):
    # create persistent storage
    create_pvc_op_task = create_pvc_op()
    # download the data to persistent storage
    download_data_op_task= download_data_op(vol=create_pvc_op_task.volume, pvc_path=pvc_path)
    # merge data
    merge_data_op_task = merge_data_op(input_path="/mnt", output_path="/mnt/merged_data.csv", vol=download_data_op_task.pvolume, pvc_path=pvc_path)
    merge_data_op_task.container.set_image_pull_policy("Always")
    # prepare data for training
    prepare_data_op_task = prepare_data_op(input_path=merge_data_op_task.outputs["data_output"], output_path="/mnt/prepared_data.csv", vol=merge_data_op_task.pvolume, pvc_path=pvc_path)
    prepare_data_op_task.container.set_image_pull_policy("Always")


#importing KFP compiler
#compiling the created pipeline
pipelineConfig = dsl.PipelineConf()
pipelineConfig.set_image_pull_policy("Always")
print(pipelineConfig.image_pull_policy)
Compiler().compile(train_recommender_model_pipeline, 'train_modell_pipeline3.zip', pipeline_conf=pipelineConfig)

#pipeline_conf=kfp.dsl.PipelineConf()
#pipeline_conf.add_op_transformer(gcp.use_gcp_secret('user-gcp-sa'))
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

def get_data_op(output_path):
    return dsl.ContainerOp(
        name = 'get_data', # name of the operation
        image = 'rsthesis/get_data_image:latest', #docker location in registry
        file_outputs = {
            'data_output': output_path #name of the file with result
        },
        arguments=['--output1-path', output_path],
        container_kwargs={"image_pull_policy": "Always"}
    )

def prepare_data_op(input_path, output_path):
    return dsl.ContainerOp(
        name = 'prepare_data', # name of operation
        image = 'rsthesis/prepare_data_image:latest', #docker location in registry
        arguments = ['--input1-path', input_path, '--output1-path', output_path], #get_data_op.output, # passing step_1.output as argument
        command=["python", "prepare_data.py"],
        file_outputs = {
            'data_output': output_path #name of the file with result
        },
        #container_kwargs = {"image_pull_policy": "Always"}
   )

# defining pipeline meta
@pipeline(
    name='Train recommender modell',
    description='Train recommender modell pipeline'
)
# stitch the steps
def train_recommender_model_pipeline():
    output_path = "data.txt"
    get_data_op_task = get_data_op(output_path)
    prepare_data_op_task = prepare_data_op(get_data_op_task.output, output_path)

    prepare_data_op_task.after(get_data_op_task)

#importing KFP compiler
#compiling the created pipeline
pipelineConfig = dsl.PipelineConf()
pipelineConfig.set_image_pull_policy("Always")
print(pipelineConfig.image_pull_policy)
Compiler().compile(train_recommender_model_pipeline, 'train_modell_pipeline3.zip', pipeline_conf=pipelineConfig)


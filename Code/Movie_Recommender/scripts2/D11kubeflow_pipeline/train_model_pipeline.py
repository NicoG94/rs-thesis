#importing KFP pipeline
from kfp.dsl import pipeline
import kfp.dsl as dsl
from kfp.compiler import Compiler

def get_data_op():
    return dsl.ContainerOp(
        name = 'get_data', # name of the operation
        image = 'rsthesis/get_data_image:latest', #docker location in registry
        #arguments = [context], # passing context as argument
        file_outputs = {
            'blob-path': '/blob_path.txt' #name of the file with result
            #'data': '/data_folder/data.csv'  # name of the file with result
            #'data': '/tmp/results.txt'  # name of the file with result
    }
    )

def prepare_data_op(blob_path):
    return dsl.ContainerOp(
        name = 'prepare_data', # name of operation
        image = 'rsthesis/prepare_data_image:latest', #docker location in registry
        arguments = ["--blob_path", blob_path], #get_data_op.output, # passing step_1.output as argument
        #command=["python", "prepare_data_op.py"]
        file_outputs = {
            'blob-path': '/blob_path.txt' #name of the file with result
        }
   )

# defining pipeline meta
@pipeline(
    name='Train recommender modell',
    description='Train recommender modell pipeline'
)
# stitch the steps
def train_recommender_model_pipeline():
    get_data_op_task = get_data_op()
    prepare_data_op_task = prepare_data_op(get_data_op_task.output)

    prepare_data_op_task.after(get_data_op_task)

#importing KFP compiler
#compiling the created pipeline
Compiler().compile(train_recommender_model_pipeline, 'train_modell_pipeline2.zip')


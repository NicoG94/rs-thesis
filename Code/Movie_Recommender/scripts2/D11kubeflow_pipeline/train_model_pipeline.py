#importing KFP pipeline
from kfp.dsl import pipeline

# defining pipeline meta
@pipeline(
    name='Train recommender modell',
    description='Train recommender modell pipeline'
)
# stitch the steps
def train_recommender_model():
    # importing container operation
    import kfp.dsl as dsl

    get_data_op = dsl.ContainerOp(
        name = 'get_data', # name of the operation
        image = 'rsthesis/get_data_image:latest', #docker location in registry
        #arguments = [context], # passing context as argument
        file_outputs = {
            'context': '/blob_path.txt' #name of the file with result
        }
    )
    prepare_data_op = dsl.ContainerOp(
        name = 'prepare_data', # name of operation
        image = 'rsthesis/prepare_data_image:latest', #docker location in registry
        arguments = [get_data_op], #get_data_op.output, # passing step_1.output as argument
        file_outputs = {
            'context': '/blob_path.txt' #name of the file with result
        }
   )

#importing KFP compiler
from kfp.compiler import Compiler#compiling the created pipeline
Compiler().compile(train_recommender_model, 'train_modell_pipeline.zip')

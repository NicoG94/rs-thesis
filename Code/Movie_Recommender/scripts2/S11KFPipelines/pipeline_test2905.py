#importing KFP pipeline
from kfp.dsl import pipeline

# defining pipeline meta
@pipeline(
    name='Calculate Average',
    description='This pipeline calculates average'
)
# stitch the steps
def train_recommender_modell():
    # importing container operation
    import kfp.dsl as dsl

    step_1 = dsl.ContainerOp(
        name = 'get_data', # name of the operation
        image = 'rsthesis/get_data_image:latest', #docker location in registry
        #arguments = [context], # passing context as argument
        file_outputs = {
            'context': '/output.txt' #name of the file with result
        }
    )
    step_2 = dsl.ContainerOp(
        name = 'get_data', # name of operation
        image = 'rsthesis/get_data_image:latest', #docker location in registry
        arguments = step_1.output, # passing step_1.output as argument
        file_outputs = {
            'context': '/output.txt' #name of the file with result
        }
   )

#importing KFP compiler
from kfp.compiler import Compiler#compiling the created pipeline
Compiler().compile(train_recommender_modell, 'train_modell_pipeline.zip')


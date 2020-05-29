#importing KFP pipeline
from kfp.dsl import pipeline

# defining pipeline meta
@pipeline(
    name='Calculate Average',
    description='This pipeline calculates average'
)
# stitch the steps
def average_calculation_pipeline(context: str):
    # importing container operation
    import kfp.dsl as dsl

    step_1 = dsl.ContainerOp(
        name = 'add', # name of the operation
        image = 'docker.io/avg/add', #docker location in registry
        arguments = [context], # passing context as argument
        file_outputs = {
            'context': '/output.txt' #name of the file with result
        }
    )
    step_2 = dsl.ContainerOp(
        name = 'div', # name of operation
        image = 'docker.io/avg/add', #docker location in registry
        arguments = [step_1], # passing step_1.output as argument
        file_outputs = {
            'context': '/output.txt' #name of the file with result
        }
   )

#importing KFP compiler
from kfp.compiler import Compiler#compiling the created pipeline
Compiler().compile(average_calculation_pipeline, 'pipeline.zip')


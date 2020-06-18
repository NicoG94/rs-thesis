#importing KFP pipeline
from kfp.dsl import pipeline
import kfp.dsl as dsl
from kfp.compiler import Compiler

def create_pvc_op():
    return dsl.VolumeOp(
        name="create_pvc",
        resource_name="my-pvc",
        size="5Gi",
        modes=dsl.VOLUME_MODE_RWM
    )

def download_data_op(vol, pvc_path, gs_path):
    return dsl.ContainerOp(
        name = "download_data",
        image = "google/cloud-sdk:295.0.0-slim",
        command = ["gsutil", "cp", "-r"],
        arguments = [gs_path, pvc_path],
        pvolumes={pvc_path: vol}
    )

def upload_data_op(vol, pvc_path, pred_pvc_path, gs_path):
    return dsl.ContainerOp(
        name = "upload_preds",
        image = "google/cloud-sdk:295.0.0-slim",
        command = ["gsutil", "cp", "-r"],
        arguments = [pred_pvc_path, gs_path],
        pvolumes={pvc_path: vol}
    )

def merge_data_op(input_path_links, input_path_ratings, output_path, vol, pvc_path, TAG):
    return dsl.ContainerOp(
        name = 'merge_data', # name of the operation
        image = f'rsthesis/get_data_image:{TAG}', #docker location in registry
        file_outputs = {
            'data_output': output_path #name of the file with result
        },
        arguments=['--input_path_links',  input_path_links, '--input_path_ratings',  input_path_ratings, '--output_path', output_path],
        container_kwargs={"image_pull_policy": "Always"},
        command=["python", "get_data.py"],
        pvolumes={pvc_path: vol}
    )

def prepare_data_op(input_path, output_path, pvc_path, vol, TAG):
    return dsl.ContainerOp(
        name = 'prepare_data',
        image = f'rsthesis/prepare_data_image:{TAG}',
        arguments = ['--input_path',  dsl.InputArgumentPath(input_path), '--output_path', output_path],
        command=["python", "prepare_data.py"],
        file_outputs = {
            'data_output': output_path
        },
        pvolumes={pvc_path: vol},
        container_kwargs = {"image_pull_policy": "Always"}
   )

def train_model_op(make_cv, make_train_test_split, input_path, output_path_model, output_path_preds, pvc_path, vol, TAG):
    return dsl.ContainerOp(
        name='train_model_and_predict',
        image=f'rsthesis/train_model_image:{TAG}',
        arguments=['--input_path', input_path, '--output_path_model', output_path_model, "--output_path_preds", output_path_preds,
                   "--make_train_test_split", make_train_test_split, "--make_cv", make_cv],
        command=["python", "train_model.py"],
        file_outputs={
            'data_output': output_path_preds,
            "model_output": output_path_model
        },
        pvolumes={pvc_path: vol},
        container_kwargs={"image_pull_policy": "Always"}
    )

# defining pipeline meta
@pipeline(
    name='Train recommender modell',
    description='Train recommender modell pipeline'
)
# stitch the steps
def train_recommender_model_pipeline(TAG:str, make_cv:bool=True, make_train_test_split:bool=True):
    # set constant params
    pvc_path = "/mnt"
    # create persistent storage
    create_pvc_op_task = create_pvc_op()
    # download the data to persistent storage
    download_data_op_task= download_data_op(vol=create_pvc_op_task.volume, pvc_path=pvc_path,
                                            gs_path="gs://raw_movie_data")
    # merge data
    merge_data_op_task = merge_data_op(input_path_links="/mnt/raw_movie_data/links.csv",
                                       input_path_ratings="/mnt/raw_movie_data/ratings.csv",
                                       output_path="/mnt/merged_data.csv",
                                       vol=download_data_op_task.pvolume, pvc_path=pvc_path,TAG=TAG)

    # prepare data for predictions later
    prepare_data_op_task = prepare_data_op(input_path=merge_data_op_task.outputs["data_output"],
                                           output_path="/mnt/prepared_data.csv", vol=merge_data_op_task.pvolume,
                                           pvc_path=pvc_path,TAG=TAG)
    # upload prepared data to storage
    #upload_data_op_task=upload_data_op(vol=prepare_data_op_task.pvolume, pvc_path=pvc_path,
    #                                   pred_pvc_path="/mnt/prepared_data.csv", gs_path="gs://rs_predictions")

    # train model
    train_model_op_task = train_model_op(make_cv=make_cv, make_train_test_split=make_train_test_split,
                                         input_path="/mnt/prepared_data.csv", output_path_model="/mnt/model.joblib",
                                         output_path_preds="/mnt/predictions.csv",
                                         pvc_path=pvc_path, vol=prepare_data_op_task.pvolume,TAG=TAG)
    # upload predictions to storage
    upload_data_op_task=upload_data_op(vol=train_model_op_task.pvolume, pvc_path=pvc_path,
                                       pred_pvc_path="/mnt/predictions.csv", gs_path="gs://rs_predictions")

from scripts2.D99docker_setup.push_all_images import push_all_images
TAG="test10"
repos = {"get_data_image": r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\scripts2\D01get_data",
         "train_model_image": r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\scripts2\D03train_model",
         #"prepare_data_image": r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\scripts2\D02prepare_data",
         }
#push_all_images(origtag=TAG, repos=repos)

#compiling the created pipeline
pipelineConfig = dsl.PipelineConf()
pipelineConfig.set_image_pull_policy("Always")
print(pipelineConfig.image_pull_policy)

#pipelineConfig.add_op_transformer(gcp.use_gcp_secret('user-gcp-sa'))

Compiler().compile(train_recommender_model_pipeline, 'train_modell_pipeline3.zip', pipeline_conf=pipelineConfig)

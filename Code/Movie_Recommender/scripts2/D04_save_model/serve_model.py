from joblib import dump

model_path=r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data_folder\simpleRS.pkl"
# load model

# start server
python -m sklearnserver --model_dir C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\data_folder\simpleRS.pkl --model_name SVD


from kubernetes import client

from kfserving import KFServingClient
from kfserving import constants
from kfserving import utils
from kfserving import V1alpha2EndpointSpec
from kfserving import V1alpha2PredictorSpec
from kfserving import V1alpha2TensorflowSpec
from kfserving import V1alpha2InferenceServiceSpec
from kfserving import V1alpha2InferenceService
from kubernetes.client import V1ResourceRequirements

namespace = utils.get_default_target_namespace()

api_version = constants.KFSERVING_GROUP + '/' + constants.KFSERVING_VERSION
default_endpoint_spec = V1alpha2EndpointSpec(
    predictor=V1alpha2PredictorSpec(
        tensorflow=V1alpha2TensorflowSpec(
            storage_uri='gs://kfserving-samples/models/tensorflow/flowers',
            resources=V1ResourceRequirements(
                requests={'cpu': '100m', 'memory': '1Gi'},
                limits={'cpu': '100m', 'memory': '1Gi'}))))

isvc = V1alpha2InferenceService(api_version=api_version,
                                kind=constants.KFSERVING_KIND,
                                metadata=client.V1ObjectMeta(
                                    name='flower-sample', namespace=namespace),
                                spec=V1alpha2InferenceServiceSpec(default=default_endpoint_spec))


KFServing = KFServingClient()
KFServing.create(isvc)



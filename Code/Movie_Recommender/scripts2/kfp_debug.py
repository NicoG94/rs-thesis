import kfp
host="http://10.10.10.10:8080/"
client = kfp.Client(host=host)#other_client_id for IAP auf GCP
print(client.list_experiments())
experiment = client.create_experiment(name="test_exp")
print(experiment)

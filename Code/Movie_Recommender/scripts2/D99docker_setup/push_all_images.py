import docker

# docker image build --tag=rsthesis/prepare_data_image:test21 C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\scripts2\D02prepare_data
# docker push rsthesis/prepare_data_image:test21

def push_all_images(origtag, repos):
    client = docker.from_env()
    client.login(username="rsthesis")
    for repo in repos.keys():
        print(f"start building and pushing {repo}")
        tag=f"rsthesis/{repo}:{origtag}"
        client.images.build(path=repos[repo], tag=origtag)
        client.images.build(path=repos[repo], tag=tag)
        client.images.push(tag)
        print(f"{repo} image pushed")

if __name__ == "__main__":
    # im terminal: docker build C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\scripts2\D06_predict
    origtag = "test3"
    repos={"get_data_image":r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\scripts2\D01get_data",
           "train_model_image":r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\scripts2\D03train_model",
           "prepare_data_image": r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\scripts2\D02prepare_data",
           "predict_image": r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\scripts2\D06_predict"}
    push_all_images(origtag, repos)

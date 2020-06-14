import docker

# docker image build --tag=rsthesis/get_data_image:test1 C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\scripts2\D01get_data
# docker push rsthesis/get_data_image:test1

def push_all_images(origtag, repos):
    client = docker.from_env()
    client.login(username="rsthesis")
    print("start building and pushing images")
    for repo in repos.keys():
        tag=f"rsthesis/{repo}:{origtag}"
        client.images.build(path=repos[repo], tag=origtag)
        client.images.build(path=repos[repo], tag=tag)
        client.images.push(tag)
        print(f"{repo} image pushed")

if __name__ == "__main__":
    origtag = "test2"
    repos={"get_data_image":r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\scripts2\D01get_data",
           "train_model_image":r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\scripts2\D03train_model",
           "predict_image": r"C:\Users\nicog\Documents\rs-thesis\Code\Movie_Recommender\scripts2\D06_predict"}
    push_all_images(origtag, repos)

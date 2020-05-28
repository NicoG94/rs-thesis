import typing as t
import json

def add(a: int ,b: t.Optional[int]=None) -> int:
    if b is None:
        c = a
    else:
        c = a+b
    return c


def timesTwo(a: int) -> int:
    return a*2

timesTwo(add(1,2))

context = {"numbers": "example.com/address/of/numbers"}
context = json.dumps(context)

def addComp(ctx: str) -> str:
    """This function calculates the sum of all the elements of a
    list stored in a shared memory and uploads the result"""
    # loading context string
    context = json.loads(ctx)  # defining the install function
    import subprocess
    def install(name):
        subprocess.call(['pip', 'install', name])  # install packages (installing numpy for the sake of demo)

    install('numpy')  # getting the auth token from context
    auth_token = context["auth"]

    # downloading the data required
    numbers = download(context["numbers"], auth_token)

    # uploading the intermediate result
    upload(sum(numbers), "example.com/address/of/sum",
           auth_token)  # adding the address to intermediate result to context string
    context["sum"] = "example.com/address/of/sum"
    return context

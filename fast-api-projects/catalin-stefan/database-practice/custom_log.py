from fastapi.requests import Request

def log(tag="MyApp",message="no_message",request:Request=None):
    # create log file if it already does not exist append
    with open("log.txt",mode="a+") as log:
        log.write(f"{tag}: {message}\n")
        log.write(f"\t{request.url}\n")
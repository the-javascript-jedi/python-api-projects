def log(tag="",message=""):
    # create log file if it already does not exist
    with open("log.txt","w+") as log:
        log.write(f"{tag}: {message}\n")
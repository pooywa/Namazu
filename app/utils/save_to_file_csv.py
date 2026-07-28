import pandas

def save_csv(filename:str,data:list[dict]):

    df = pandas.DataFrame(data)

    df.to_csv(filename,index=False,encoding='UTF-8')


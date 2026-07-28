import pandas

def save_csv(filename:str,data:list[dict]):

    df = pandas.DataFrame(data)

    df.to_csv(filename,index=False,encoding='utf-8-sig')


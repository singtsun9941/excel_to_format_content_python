def clean_data(df):
    new_header = getNewHeader(df)
    new_content = getContent(df)
    new_df = new_content
    new_df.columns = new_header
    return new_df

def getNewHeader(df):
    new_header = df.iloc[3].tolist()
    new_header[0] = "staff_name"
    new_header[1] = "staff_id"
    new_header[2] = "tel"
    # print(new_header.tolist())
    return new_header

def getContent(df):
    content = df.iloc[5:]
    # print(content.values.tolist())
    return content
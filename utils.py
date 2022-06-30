import glob
import tabula
import pandas as pd
from skimpy import clean_columns
from unidecode import unidecode


class Wrangling():
    # find all pdfs downloaded from the extract script
    list_pdfs = glob.glob("pdfs/*.pdf")

    # function to find and save tables from pdfs
    # I had one issue reading file 20130819_170303.pdf, so I removed this file from the folder. 
    # In the future the function below needs to handle exeptions and skip and/or log problematic files. 
    def save_tables_from_pdfs(list_pdfs):

        # extract tables from pdf
        # ref: https://stackoverflow.com/questions/49733576/how-to-extract-more-than-one-table-present-in-a-pdf-file-with-tabula-in-python
        all_pdfs = list()
        for pdf in list_pdfs:
            
            # start
            print(pdf)

            dfs = tabula.read_pdf(pdf, pages='all')
            # tabula.convert_into("pdfs/20130716_172817.pdf", "output.csv", output_format="csv", pages='all')

            dfs = pd.concat(dfs)

            clean_df = clean_columns(dfs)

            # removing extra spaces and all to lower case
            for column in clean_df.columns:
                clean_df[column] = clean_df[column].astype(str)
                clean_df[column] = clean_df[column].str.strip()
                clean_df[column] = clean_df[column].str.lower()
            # create column that stores pdf name
            clean_df["file_name"] = pdf
            clean_df = pd.DataFrame(clean_df)

            # append to list:
            all_pdfs.append(clean_df)
            
        print(all_pdfs[1])

        # res concatates the list of pdfs:
        res = pd.concat(all_pdfs)

        # save res to csv
        pd.DataFrame(res).to_csv("all_data.csv")

    def clean_flights(data, cols):
        # select specific cols
        cols = ["autoridades_apoiadas","origem","decolagem_h_local","destino","pouso_h_local","motivo","previsao_de_passageiros","file_name"]
        data = data[cols] # select specific cols

        # remove occurences without departing time
        # Convert NaN values to empty string
        nan_value = float("NaN")
        data.replace("", nan_value, inplace=True)
        data.dropna(subset = ['decolagem_h_local', 'origem', 'destino'], inplace=True)
        # save what is inside parenthesis in separate column:
        data["observation_origem"] = data["origem"].str.extract('.*\((.*)\).*')
        data["observation_destino"] = data["destino"].str.extract('.*\((.*)\).*')

        # groom columns destino and origem
        cols_clean = ['origem', 'destino']
        for col_clean in cols_clean:
            data[col_clean] = data[col_clean].astype(str) # column should be type string
            data[col_clean] = data[col_clean].str.replace(r"\(.*\)","") # remove everything that is inside () (inclusive)
            data[col_clean] = data[col_clean].str.strip() # remove extra empty spaces
            data[col_clean] = data[col_clean].apply(unidecode) # replace letters with accents with the letter without accent.
            data = data[~data[col_clean].str.contains("/")] # if any city contains : it will be removed - avoid problematic 
                                                            # records with data instead of cities in origem or destino

        return(data)

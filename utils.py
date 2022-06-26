import glob
import tabula
import pandas as pd
from skimpy import clean_columns

class Wrangling():
    # find all pdfs downloaded from the extract script
    list_pdfs = glob.glob("pdfs/*.pdf")

    # function to find and save tables from pdfs
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

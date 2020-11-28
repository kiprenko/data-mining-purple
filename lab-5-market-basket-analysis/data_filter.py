import pandas as pd

INPUT_FILE_NAME = 'Online Retail.xlsx'
OUTPUT_FILE_NAME = 'Filtered Online Retail.xlsx'


# reduce excess columns in dataframe and remove canceled orders
def filter_dataframe(df):
    df = df.filter(items=['InvoiceNo', 'StockCode', 'Quantity', 'CustomerID'])
    return df[df['InvoiceNo'].str[0] != 'C']


def save_filtered_df(df):
    writer = pd.ExcelWriter(OUTPUT_FILE_NAME, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()


if __name__ == '__main__':
    save_filtered_df(filter_dataframe(pd.read_excel(INPUT_FILE_NAME)))

import pandas as pd

def flatten_list_of_lists(list_of_lists: list, remove_non_lists: bool=True) -> list:
    """
    Flatten a list of lists
    
    Arguments
    ----------
    remove_non_lists - bool
        Option to remove non list elements
    
    Returns
    ---------
    Flattened list
    """

    if remove_non_lists:
        list_of_lists = [lst for lst in list_of_lists if isinstance(lst, list)]

    return [val for lst in list_of_lists for val in lst]

def dict_from_list(lst: list, value: any) -> dict:
    """
    Create a dictionary with keys from a `lst` and values of `value`
    """

    return {key:value for key in lst}

def convert_dtypes(df: pd.DataFrame, str_cols: list=None, int_cols: list=None, float_cols: list=None, dt_cols: dict=None) -> pd.DataFrame:
    """
    Convert pandas DataFrame columns to specific dtypes
    
    Convert column dtypes given lists/dicts of columns
    
    Arguments
    ----------
    str_cols : list
        column names to conver to str
    int_cols : list
        column names to conver to int
    float_cols : list
        column names to conver to float
    dt_cols : dict
        datetime columns and format for datetime parsing
    
    Returns
    ---------
    df : pd.DataFrame
        DataFrame with columns converted
    """

    df_typed = df.copy()

    str_dict, int_dict, float_dict = {}, {}, {}

    if str_cols: 
        str_dict = dict_from_list(str_cols, str)
    if int_cols: 
        int_dict = dict_from_list(int_cols, int)
    if float_cols: 
        float_dict = dict_from_list(float_cols, float)

    df_typed = df_typed.astype({**str_dict, **int_dict, **float_dict})

    for col, form in dt_cols.items():
        df_typed[col] = pd.to_datetime(df_typed[col], format=form)

    return df_typed

def snake_case_cols(df: pd.DataFrame) -> pd.DataFrame:
    """
    Snake case DataFrame columns

    i.e. [Start Date, Final Value] -> [start_date, final_vale]
    """

    df_out = df.copy()
    df_out.columns = [col.lower().replace(' ','_') for col in df_out.columns]

    return df_out
    

if __name__ == "__main__":
    pass

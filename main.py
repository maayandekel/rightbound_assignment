
import pandas as pd


def unify_values(df):
    """
    this function creates columns with a unified format - all uppercase and function list sorted alphabetically
    :param df: dataframe of title, functions, and function group
    :return: input dataframe with added columns of the title and function group in upper case, and the functions
             in upper case and sorted alphabetically, once as a tuple and once as a list
    """
    uppercase_title = df['title'].str.upper()
    df.insert(len(df.columns), 'uppercase_title', uppercase_title, True)
    uppercase_functions = df['functions'].str.upper()  # uppercase for consistent formatting of values for comparison
    sorted_functions = []
    sorted_functions_list = []
    for function in uppercase_functions:
        if ',' in function:
            split_function = function.split(',')
            split_function.sort()  # sorting for consistent formatting of values for comparison
        else:
            split_function = [function]
        sorted_functions_list.append(split_function)
        tuple_function = tuple(split_function)
        sorted_functions.append(tuple_function)
    df.insert(len(df.columns), 'uppercase_functions', sorted_functions, True)
    df.insert(len(df.columns), 'uppercase_functions_list', sorted_functions_list, True)
    uppercase_group = df['function_group'].str.upper()
    df.insert(len(df.columns), 'uppercase_group', uppercase_group, True)
    return df


def null_vals(df, column):
    """
    this function finds rows with null values in the dataframe
    :param df: any dataframe
    :param column: the column to check for null values in
    :return: a dataframe with only the rows where the column is null
    """
    is_null = pd.isnull(df[column])
    result_df = df[is_null]
    return result_df


def find_duplicates(df, column_list):
    """
    this function finds all the duplicate rows (including the first appearance) that are duplicative for all the columns
    in the list
    :param df: a dataframe
    :param column_list: a list of the columns who values are checked for duplication
    :return: a series of the row that is duplicated and how many times it appears
    """
    duplicates = df.duplicated(keep=False, subset=column_list)
    duplicates_df = df[duplicates]
    duplicates_count = duplicates_df.pivot_table(index=column_list, aggfunc='size')
    return duplicates_count


def find_mismatches_between_columns(df, column1, column2):
    """
    this function finds mismatches between column1 and column2 - meaning cases where a value in column1 has more than
    one "matching" value in column2
    :param df: a dataframe
    :param column1: the column which we want to find mismatches for (each value should have only 1 matching value in
    column 2)
    :param column2: the column that is meant to match column1
    :return: a dataframe that only has rows which contain a value of column1 that has more than one "matching" value of
    column 2
    """
    duplicate_column1_column2 = df.duplicated(subset=[column1, column2])
    unique_maps = df[~duplicate_column1_column2]   #keep unique cases of col1 to col2
    duplicated_column1 = unique_maps.duplicated(keep=False, subset=column1)
    mismatches = unique_maps[duplicated_column1] #keep unique mappings with duplicated col1
    mismatch_columns = mismatches[[column1, column2]]
    return mismatch_columns


def functions_matched_to_other_group(df):
    """
    this function finds the functions that are mapped to the group 'OTHER' and how many occurences each has
    :param df: a dataframe with a functions column and a function group column
    :return: a series of the functions that are mapped to 'OTHER' and a count
    """
    result_df = df.loc[df['uppercase_group'] == 'OTHER']
    function_count = result_df.pivot_table(index='uppercase_functions', aggfunc='size')
    return function_count


def duplicates_within_functions_column(df):
    """
    this function finds rows which have duplicates of the same function within the functions column
    :param df: a dataframe with a functions column in the form of a list
    :return: 1) a series of unique functions that contain a duplicate function with a count
             2) a set of the individual functions that appear as duplicates
    """
    has_duplicate = []
    functions_seen_in_row = set()
    duplicated_function = []
    for func_ls in df['uppercase_functions_list']:
        if len(func_ls) != len(set(func_ls)): #taking only cases with function duplicates
            for x in func_ls:
                if x in functions_seen_in_row:
                    duplicated_function.append(x)
                else:
                    functions_seen_in_row.add(x)
            has_duplicate.append(True)
        else:
            has_duplicate.append(False)
    unique_duplicates = set(duplicated_function)
    duplicates_in_functions_df = df[has_duplicate]
    duplicates_in_functions = duplicates_in_functions_df.pivot_table(index='uppercase_functions', aggfunc='size')
    return duplicates_in_functions, unique_duplicates


def main():
    readme_md = "# Home assignment for rightbound interview - part 1\n\n"
    df = pd.read_csv("C:/Users/programming_user/rightbound/titles_HA.csv")
    duplicate_rows = find_duplicates(df, ['title', 'functions', 'function_group'])
    readme_md += f"Number of rows that have duplicates: {len(duplicate_rows)}\n\n"
    null_functions = null_vals(df, 'functions')
    readme_md += f"Number of rows that have a null functions column: {len(null_functions)}\n\n"
    null_group = null_vals(df, 'function_group')
    readme_md += f"Number of rows that have a null function group column: {len(null_group)}\n\n"
    unify_df = unify_values(df)
    group_counts = unify_df.pivot_table(index='uppercase_group', aggfunc='size')
    readme_md += "The number of appearances of each function group:\n\n```"
    readme_md += f"{repr(group_counts)}\n```\n\n"
    #identify mismatches in mapping
    content_duplicate_rows = find_duplicates(df, ['uppercase_title', 'uppercase_functions', 'uppercase_group'])
    mismatch_title_func = find_mismatches_between_columns(unify_df, 'uppercase_title', 'uppercase_functions')
    mismatch_functions_group = find_mismatches_between_columns(unify_df, 'uppercase_functions', 'uppercase_group')
    readme_md += "The functions mapped to more than one function group are:\n\n```"
    readme_md += f"{repr(mismatch_functions_group)}\n```\n\n"
    #identify formatting issues
    mismatch_titles = find_mismatches_between_columns(unify_df, 'uppercase_title', 'title')
    mismatch_funcs = find_mismatches_between_columns(unify_df, 'uppercase_functions', 'functions')
    readme_md += f"There are {len(mismatch_funcs) / 2} functions which appear throughout in different forms (different cases or different order).\n\n"
    mismatch_groups = find_mismatches_between_columns(unify_df, 'uppercase_group', 'function_group')
    readme_md += f"There are {len(mismatch_groups / 2)} function groups which appear throughout in different forms (different cases).\n\n"
    #other category issues
    functions_to_other = functions_matched_to_other_group(unify_df)
    readme_md += "The following are the counts of each of the functions that are mapped to the function group Other:\n\n```"
    readme_md += f"{repr(functions_to_other)}\n```\n\n"
    #other issues
    dup_in_funcs_full, dup_in_funcs_ls = duplicates_within_functions_column(unify_df)
    readme_md += "The following functions appear at times as duplicates within the same row:\n\n"
    readme_md += f"```\n{repr(dup_in_funcs_ls)}\n```"

    with open('README.md', 'w') as f:
        f.write(readme_md)


if __name__ == '__main__':
    main()
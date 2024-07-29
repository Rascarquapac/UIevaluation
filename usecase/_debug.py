import pandas as pd
################## DEBUG ############################
def debug_pool_to_csv(pool_df,debug_prefix="fuck"):
    if not pool_df.empty:
        pool_df.to_csv(f'./debug/debug_{debug_prefix}_camera_pool.csv')
def debug_csv_to_pool(debug_prefix="fuck"):
    pool_df = pd.DataFrame()
    if pool_df.empty:
        pool_df= pd.read_csv(f'./debug/debug_{debug_prefix}_camera_pool.csv')
        pool_df.set_index('Model', inplace=True)
    return pool_df

def debug_usecase_to_csv(usecase_df,debug_prefix="fuck"):
    usecase_df.to_csv(f'./debug/debug_{debug_prefix}_usecase_after_analyze.csv')
    return

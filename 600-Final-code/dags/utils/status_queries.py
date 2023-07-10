from config.env_vars import PROJECT_ID, DATASET_ID, JOB_STATUS_TABLE_ID


PROCESS_JOB_START_STATUS_QUERY = (
    f"INSERT INTO `{PROJECT_ID}.{DATASET_ID}.{JOB_STATUS_TABLE_ID}` VALUES"
    " ('{process_date}', '{context}', '{process_name}', "
    "'{run_id}', 'START');"
)


PROCESS_JOB_FAILURE_STATUS_QUERY = (
    f"INSERT INTO `{PROJECT_ID}.{DATASET_ID}.{JOB_STATUS_TABLE_ID}` VALUES"
    " ('{process_date}', '{context}','{process_name}', "
    "'{run_id}', 'FAILURE');"
)

PROCESS_JOB_SUCCESS_STATUS_QUERY = (
    f"INSERT INTO `{PROJECT_ID}.{DATASET_ID}.{JOB_STATUS_TABLE_ID}` VALUES"
    " ('{process_date}', '{context}','{process_name}', "
    "'{run_id}', 'SUCCESS');"
)

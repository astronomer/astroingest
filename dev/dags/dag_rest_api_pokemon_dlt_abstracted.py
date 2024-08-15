from datetime import timedelta
from airflow.decorators import dag

import dlt
from dlt.common import pendulum

from astroingest.dlt_pipeline_task_group import DltPipelineTaskGroup

default_task_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": "test@test.com",
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "execution_timeout": timedelta(hours=20),
}


@dag(
    schedule_interval="@daily",
    start_date=pendulum.datetime(2023, 7, 1),
    catchup=False,
    max_active_runs=1,
    default_args=default_task_args,
)
def load_data():
    """
    Same as the dag_rest_api_pokemon DAG, but written with DltPipelineTaskGroup to abstract the dlt pipeline creation.
    """
    from include.rest_api import pokemon_source

    dlt_task_group = DltPipelineTaskGroup(
        pipeline_name="rest_api_pipeline_pokemon",
        dlt_source=pokemon_source,
        dataset_name="pokemon",
        destination=dlt.destinations.postgres("postgres://postgres:postgres@postgres:5432/postgres"),
        use_data_folder=False,
        wipe_local_data=True,
    )
    
    dlt_task_group()
    

load_data()

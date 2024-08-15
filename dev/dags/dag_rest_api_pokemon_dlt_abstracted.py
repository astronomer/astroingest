from datetime import timedelta
from airflow.decorators import dag

import dlt
from dlt.common import pendulum
from airflow.operators.empty import EmptyOperator

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
def astroingest_load_data():
    """
    Same as the dag_rest_api_pokemon DAG, but written with DltPipelineTaskGroup to abstract the dlt pipeline creation.
    """
    from include.rest_api import pokemon_source

    pre_dlt = EmptyOperator(task_id="pre_dlt")

    dlt_task_group = DltPipelineTaskGroup(
        pipeline_name="astroingest_rest_api_pipeline_pokemon",
        dlt_source=pokemon_source(),
        dataset_name="pokemon",
        destination=dlt.destinations.postgres(
            "postgres://airflow:pg_password@postgres:5432/airflow"
        ),
        use_data_folder=False,
        wipe_local_data=True,
    )

    post_dlt = EmptyOperator(task_id="post_dlt")

    pre_dlt >> dlt_task_group >> post_dlt


astroingest_load_data()

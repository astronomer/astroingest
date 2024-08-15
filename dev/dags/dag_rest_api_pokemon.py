from datetime import timedelta
from airflow.decorators import dag

import dlt
from dlt.common import pendulum
from dlt.helpers.airflow_helper import PipelineTasksGroup

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
    This DAG is used to load data from the Pokemon API into a Postgres database with postgres schema `pokemon`.
    """
    # set `use_data_folder` to True to store temporary data on the `data` bucket. Use only when it does not fit on the local storage
    tasks = PipelineTasksGroup(
        "pipeline_decomposed", use_data_folder=False, wipe_local_data=True
    )

    # import your source from pipeline script
    from include.rest_api import pokemon_source as source

    # modify the pipeline parameters
    pipeline = dlt.pipeline(
        pipeline_name="rest_api_pipeline_pokemon",
        dataset_name="pokemon",
        destination=dlt.destinations.postgres(
            "postgres://postgres:postgres@postgres:5432/postgres"
        ),
        full_refresh=False,  # must be false if we decompose
    )
    # create the source, the "serialize" decompose option will converts dlt resources into Airflow tasks. use "none" to disable it
    tasks.add_run(
        pipeline,
        source(),
        decompose="parallel-isolated",
        trigger_rule="all_done",
        retries=0,
        provide_context=True,
    )


load_data()

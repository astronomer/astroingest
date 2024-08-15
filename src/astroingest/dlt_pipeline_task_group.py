"""
This module contains a function to render a dbt project as an Airflow Task Group.
"""

from __future__ import annotations

from typing import Any

from dlt.helpers.airflow_helper import PipelineTasksGroup
from dlt.common.destination import TDestinationReferenceArg
from dlt.extract.source import DltSource
import dlt

class DltPipelineTaskGroup(PipelineTasksGroup):
    def __init__(
        self,
        pipeline_name: str,
        dlt_source: DltSource,
        
        # TODO: not sure if we allow these 2 to pass in?
        use_data_folder: bool = False, 
        wipe_local_data: bool = True,
        # ----------------------------------------------
        
        dataset_name: str = None,
        destination: TDestinationReferenceArg = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(pipeline_name, use_data_folder=use_data_folder, wipe_local_data=wipe_local_data, **kwargs)

        dlt_pipeline = dlt.pipeline(
            pipeline_name=pipeline_name,
            dataset_name=dataset_name,
            destination=destination,
            full_refresh=False,  # must be false if we decompose
        )
        
        self.add_run(
            pipeline = dlt_pipeline,
            data = dlt_source,
            decompose="parallel-isolated",
            trigger_rule="all_done",
            retries=0,
            provide_context=True,
        )
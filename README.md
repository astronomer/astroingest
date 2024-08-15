# astroingest

This project uses (Rye)[https://github.com/astral-sh/rye], learn how to set this up.

# Contributing

Use Docker Compose to check that your changes work in an actual Airflow runtime environment. To spin this up, run the following in this directory:

`docker compose -f dev/docker-compose.yml up -d --build`

# Project Plan

The project will have the following structure:

1. `/dev`: (TODO) Use this to set up a local development environment and import the local astroingest code as a package. Based on https://github.com/astronomer/astronomer-cosmos/tree/main/dev

2. `src/astroingest`: The astroingest package

3. `src/astroingest/ingestion_backends`: A module of the possible ingestion backends, where the first one we're implementing is `src/astroingest/ingestion_backends/dlt`.

4. `src/astroingest/ingestion_backends/*/connection_mappings`: Interface for defining ways to map Airflow connections to connection configuration that can be understood by the ingestion backend. Starting with `dlt`. See using customer providers on `dlt` here: https://dlthub.com/docs/general-usage/credentials/setup#custom-providers.

5. `src/astroingest/ingestion_backends/*/connection_mappings`: Interface for defining ways to map Airflow connections to connection configuration that can be understood by the ingestion backend. Starting with `dlt`. See using customer providers on `dlt` here: https://dlthub.com/docs/general-usage/credentials/setup#custom-providers.

This project is inspired by the work of Cosmos, the Universal Transfer Operator, and dlt's Airflow integration. See here:

1. https://github.com/astronomer/apache-airflow-providers-transfers/tree/main/src/universal_transfer_operator/data_providers
2. https://github.com/dlt-hub/dlt/blob/devel/dlt/helpers/airflow_helper.py
3. https://github.com/astronomer/apache-airflow-providers-transfers/tree/main/src/universal_transfer_operator/data_providers

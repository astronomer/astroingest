FROM quay.io/astronomer/astro-runtime:11.7.0-base

USER root

RUN pip install -U uv

COPY ./README.md ${AIRFLOW_HOME}/astroingest/
COPY ./pyproject.toml  ${AIRFLOW_HOME}/astroingest/
COPY ./src/astroingest/  ${AIRFLOW_HOME}/src/astroingest/
COPY ./dev/requirements.txt ${AIRFLOW_HOME}/requirements.txt
COPY ./dev/packages.txt ${AIRFLOW_HOME}/packages.txt


# install the package in editable mode
RUN uv pip install --system -e "${AIRFLOW_HOME}/astroingest" && \
    uv pip install --system -r ${AIRFLOW_HOME}/requirements.txt

# make sure astro user owns the package
RUN chown -R astro:astro ${AIRFLOW_HOME}/astroingest

ENV AIRFLOW_CONN_AIRFLOW_DB=postgres://airflow:pg_password@postgres:5432/airflow
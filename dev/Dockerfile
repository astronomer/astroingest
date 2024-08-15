FROM quay.io/astronomer/astro-runtime:11.9.0-base

USER root

RUN pip install -U uv

COPY ./pyproject.toml  ${AIRFLOW_HOME}/astroingest/
COPY ./README.md  ${AIRFLOW_HOME}/astroingest/
COPY ./src/  ${AIRFLOW_HOME}/astroingest/src/

# Bring in the standard Astro project files
COPY ./dev/ ${AIRFLOW_HOME}/

# install the package in editable mode
RUN uv pip install --system -e "${AIRFLOW_HOME}/astroingest" && \
    uv pip install --system -r ${AIRFLOW_HOME}/requirements.txt

# make sure astro user owns the package
RUN chown -R astro:astro ${AIRFLOW_HOME}/astroingest

USER astro

ENV AIRFLOW_CONN_AIRFLOW_DB=postgres://airflow:pg_password@postgres:5432/airflow
ENV MYSQL_DB=mysql://airflow:mysql_password@mysql:3306/airflow
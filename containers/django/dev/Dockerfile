# ref: https://github.com/mamba-org/micromamba-docker/blob/main/Dockerfile

FROM ghcr.io/mentalhealthai-org/mhai-web-deps:dev

LABEL maintainer="Ivan Ogasawara <ivan.ogasawara@gmail.com>"
LABEL org.opencontainers.image.title="Mhai"
LABEL org.opencontainers.image.authors="Mhai Team"
LABEL org.opencontainers.image.source="https://github.com/mentalhealthai-org/mhai-web"
LABEL org.opencontainers.image.version="latest"
LABEL org.opencontainers.image.description="Mhai Web"
LABEL org.mentalhealthai_org.config.version="latest"

# it is the default, but using it here to have it explicitly
USER root

ENV USERNAME=mhai

RUN mkdir -p /opt/services/mhai-web \
  && chmod -R a+rwx /opt/services/mhai-web \
  && chown ${USERNAME}:${USERNAME} /opt/services

USER ${USERNAME}

WORKDIR /opt/services/mhai-web

ARG HTTP_PROXY
ARG HTTPS_PROXY

ENV CONDA_PREFIX /opt/conda/envs/$ENV_NAME
ENV PATH ${CONDA_PREFIX}/bin:$PATH

ARG ENV=dev
ARG STATIC_ROOT
ARG MEDIA_ROOT

ENV STATIC_ROOT ${STATIC_ROOT}
ENV MEDIA_ROOT ${MEDIA_ROOT}

COPY --chown=${USERNAME}:${USERNAME} pyproject.toml poetry.lock /opt/services/mhai-web
COPY --chown=${USERNAME}:${USERNAME} containers/django/scripts/activate.sh /opt/activate.sh
COPY --chown=${USERNAME}:${USERNAME} containers/django/scripts/install-deps.sh /opt/deps/install-deps.sh
# note: src/libs/mhailib is a dependency now for the backend django
RUN mkdir /opt/services/mhai-web/src
COPY --chown=${USERNAME}:${USERNAME} src/libs /opt/services/mhai-web/src/libs

RUN conda init bash \
  && source ~/.bashrc \
  && source /opt/activate.sh \
  && conda env list \
  && /opt/deps/install-deps.sh

COPY --chown=${USERNAME}:${USERNAME} src/backend /opt/services/mhai-web/src/backend
COPY --chown=${USERNAME}:${USERNAME} src/frontend /opt/services/mhai-web/src/frontend

WORKDIR /opt/services/mhai-web/src/backend

ENV PYTHONPATH='/opt/services/mhai-web/src/backend'

RUN sudo chown ${USERNAME}:${USERNAME} /opt/
COPY --chown=${USERNAME}:${USERNAME} ./containers/django/scripts/entrypoint.sh /opt/entrypoint.sh
RUN sed -i 's/\r$//g' /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh

COPY --chown=${USERNAME}:${USERNAME} ./containers/django/dev/start /opt/start
RUN sed -i 's/\r$//g' /opt/start
RUN chmod +x /opt/start

COPY --chown=${USERNAME}:${USERNAME} ./containers/celery/dev/worker/start /opt/start-celeryworker
COPY --chown=${USERNAME}:${USERNAME} ./containers/celery/dev/beat/start /opt/start-celerybeat
COPY --chown=${USERNAME}:${USERNAME} ./containers/celery/dev/flower/start /opt/start-flower

RUN sed -i 's/\r$//g' /opt/start-celeryworker \
  && sed -i 's/\r$//g' /opt/start-celerybeat \
  && sed -i 's/\r$//g' /opt/start-flower \
  && chmod +x /opt/start-celeryworker \
  && chmod +x /opt/start-celerybeat \
  && chmod +x /opt/start-flower

# copy application code to WORKDIR
COPY --chown=${USERNAME}:${USERNAME} . ${APP_HOME}

ENTRYPOINT ["tini", "--", "/opt/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

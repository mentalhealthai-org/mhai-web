# ref: https://github.com/mamba-org/micromamba-docker/blob/main/Dockerfile

FROM ghcr.io/mentalhealthai-org/mhai-web-deps:prod

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

COPY --chown=${USERNAME}:${USERNAME} pyproject.toml poetry.lock /opt/deps/
COPY --chown=${USERNAME}:${USERNAME} containers/django/scripts/install-deps.sh /opt/deps/install-deps.sh
COPY --chown=${USERNAME}:${USERNAME} containers/django/scripts/activate.sh /opt/activate.sh

ARG ENV=prod

RUN conda init bash \
  && source ~/.bashrc \
  && source /opt/activate.sh \
  && conda env list \
  && /opt/deps/install-deps.sh

COPY --chown=${USERNAME}:${USERNAME} src/ /opt/services/mhai-web/src

ARG STATIC_ROOT
ARG MEDIA_ROOT

ENV STATIC_ROOT ${STATIC_ROOT}
ENV MEDIA_ROOT ${MEDIA_ROOT}


WORKDIR /opt/services/mhai-web/src/backend

ENV PYTHONPATH='/opt/services/mhai-web/src/backend'

RUN sudo chown ${USERNAME}:${USERNAME} /opt/
COPY --chown=${USERNAME}:${USERNAME} ./containers/django/scripts/entrypoint.sh /opt/entrypoint.sh
RUN sed -i 's/\r$//g' /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh

COPY --chown=${USERNAME}:${USERNAME} ./containers/django/prod/start /opt/start
RUN sed -i 's/\r$//g' /opt/start
RUN chmod +x /opt/start

COPY --chown=${USERNAME}:${USERNAME} ./containers/celery/prod/worker/start /opt/start-celeryworker
COPY --chown=${USERNAME}:${USERNAME} ./containers/celery/prod/beat/start /opt/start-celerybeat
COPY --chown=${USERNAME}:${USERNAME} ./containers/celery/prod/flower/start /opt/start-flower

RUN sed -i 's/\r$//g' /opt/start-celeryworker \
  && sed -i 's/\r$//g' /opt/start-celerybeat \
  && sed -i 's/\r$//g' /opt/start-flower \
  && chmod +x /opt/start-celeryworker \
  && chmod +x /opt/start-celerybeat \
  && chmod +x /opt/start-flower

# copy application code to WORKDIR
COPY --chown=${USERNAME}:${USERNAME} . ${APP_HOME}

ENTRYPOINT ["tini", "--", "/opt/entrypoint.sh"]

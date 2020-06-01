FROM ubuntu:16.04
FROM python:3.7-slim

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev libglib2.0 libsm6 libxext6 libxrender-dev


COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /

ENTRYPOINT [ "python3" ]

EXPOSE 5000
CMD [ "app.py", "run" ]
# CMD [ "app.py" ]





































# FROM tiangolo/meinheld-gunicorn-flask:python3.7

# COPY . /app

# # # FROM ubuntu:16.04
# # # FROM python:3.7

# # # RUN pip install --upgrade pip

# # # # We copy just the requirements.txt first to leverage Docker cache
# # # COPY ./requirements.txt /app/requirements.txt

# # # WORKDIR /app

# # # RUN pip install -r requirements.txt

# # # COPY . /app

# # # CMD [ "python", "application.py" ]

# # # # Herr's suggestion
# # # # conda install -c conda-forge opencv


# # #########################################

# # #FROM frolvlad/alpine-glibc:alpine-3.11
# # # FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

# # # COPY ./app /app

# # # ARG CONDA_VERSION="4.7.12.1"
# # # ARG CONDA_MD5="81c773ff87af5cfac79ab862942ab6b3"
# # # ARG CONDA_DIR="/opt/conda"

# # # ENV PATH="$CONDA_DIR/bin:$PATH"
# # # ENV PYTHONDONTWRITEBYTECODE=1

# # # # Install conda
# # # RUN echo "**** install dev packages ****" && \
# # #     apk add --no-cache --virtual .build-dependencies bash ca-certificates wget && \
# # #     \
# # #     echo "**** get Miniconda ****" && \
# # #     mkdir -p "$CONDA_DIR" && \
# # #     wget "http://repo.continuum.io/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh" -O miniconda.sh && \
# # #     echo "$CONDA_MD5  miniconda.sh" | md5sum -c && \
# # #     \
# # #     echo "**** install Miniconda ****" && \
# # #     bash miniconda.sh -f -b -p "$CONDA_DIR" && \
# # #     echo "export PATH=$CONDA_DIR/bin:\$PATH" > /etc/profile.d/conda.sh && \
# # #     \
# # #     echo "**** setup Miniconda ****" && \
# # #     conda update --all --yes && \
# # #     conda config --set auto_update_conda False && \
# # #     \
# # #     echo "**** cleanup ****" && \
# # #     apk del --purge .build-dependencies && \
# # #     rm -f miniconda.sh && \
# # #     conda clean --all --force-pkgs-dirs --yes && \
# # #     find "$CONDA_DIR" -follow -type f \( -iname '*.a' -o -iname '*.pyc' -o -iname '*.js.map' \) -delete && \
# # #     \
# # #     echo "**** finalize ****" && \
# # #     mkdir -p "$CONDA_DIR/locks" && \
# # #     chmod 777 "$CONDA_DIR/locks"

# # FROM tiangolo/uwsgi-nginx-flask:flask

# # # copy over our requirements.txt file
# # COPY requirements.txt /tmp/

# # # upgrade pip and install required python packages
# # RUN pip install -U pip
# # RUN pip install -r /tmp/requirements.txt

# # # copy over our app code
# # COPY ./app /app

# # # set an environmental variable, MESSAGE,
# # # which the app will use and display
# # ENV MESSAGE "hello from Docker"


# # # RUN conda install -c conda-forge numpy
# # # RUN conda install -c conda-forge flask
# # # RUN conda install -c conda-forge pybase64
# # # RUN conda install -c conda-forge jsonpickle
# # # RUN conda install -c conda-forge pillow
# # # RUN conda install -c conda-forge gunicorn
# # # RUN conda install -c conda-forge opencv

# # # WORKDIR /app
# # # COPY . /app


# # ENV FLASK_APP application.py
# # ENV FLASK_RUN_HOST 0.0.0.0

# # CMD ["flask", "run"]
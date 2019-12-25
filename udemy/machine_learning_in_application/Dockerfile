FROM continuumio/miniconda3
MAINTAINER "Tasuku Hori" <tasuku-hori@exa-corp.co.jp>

# For exa environment
# if not exa lan, omit them
ENV HTTP_PROXY http://solidproxy.exa-corp.co.jp:8080
ENV HTTPS_PROXY http://solidproxy.exa-corp.co.jp:8080
RUN echo "proxy_servers:" >> ~/condarc && \
    echo "    http: http://solidproxy.exa-corp.co.jp:8080" >> ~/.condarc && \
    echo "    https: http://solidproxy.exa-corp.co.jp:8080" >> ~/.condarc

# Remove (large file sizes) MKL optimizations.
RUN conda install -y nomkl
RUN conda install -y numpy scipy scikit-learn cython

# install required packages
ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -qr /tmp/requirements.txt

# expose port
EXPOSE 3000

# copy to work dir in container
ADD . /opt/ml_in_app
WORKDIR /opt/ml_in_app

# execute application
CMD python run_application.py

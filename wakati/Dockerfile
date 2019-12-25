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
RUN conda install -y nomkl && \
    conda install -y numpy scipy scikit-learn cython
ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -qr /tmp/requirements.txt

# listen port (container)
EXPOSE 3000

# add files and set command
ADD . /opt/wakati
WORKDIR /opt/wakati

CMD python run_application.py

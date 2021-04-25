FROM ubuntu:18.04

RUN apt-get update && apt-get -y install python3.7 python3-pip git cmake wget

RUN ln -s /usr/bin/pip3 /usr/bin/pip && ln -s /usr/bin/python3 /usr/bin/python

RUN pip install Cython && pip install numpy pandas


RUN wget https://github.com/apache/arrow/archive/apache-arrow-1.0.1.tar.gz \
	&& tar xzf apache-arrow-1.0.1.tar.gz &&cd arrow-apache-arrow-1.0.1/cpp
RUN cd arrow-apache-arrow-1.0.1/cpp \
    && mkdir build \
    && cd build \
    && export ARROW_HOME=/usr/local/ \
    && cmake -DCMAKE_INSTALL_PREFIX=$ARROW_HOME -DCMAKE_INSTALL_LIBDIR=lib -DARROW_WITH_BZ2=ON \
        -DARROW_WITH_ZLIB=ON \
        -DARROW_WITH_ZSTD=ON \
        -DARROW_WITH_LZ4=ON \
        -DARROW_WITH_SNAPPY=ON \
        -DARROW_PARQUET=ON \
        -DARROW_PYTHON=ON \
        -DARROW_BUILD_TESTS=OFF \
        .. \
    &&  make -j4 \
    &&  make install \
    &&  cd ../../python \
    &&  python3 setup.py build_ext --build-type=release --with-parquet \
    &&  python3 setup.py install

RUN pip install streamlit pendulum matplotlib

RUN pip install fastapi uvicorn pymongo

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV MONGO_ADDRESS=localhost:8000
ENV MONGO_CONTAINER=mongodb

COPY ./src/ /app/

WORKDIR /app/

CMD /bin/bash -c "sh startup.sh"

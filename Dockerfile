# Stage 1: Build dependencies
FROM public.ecr.aws/lambda/python:3.10 AS builder

# Install build dependencies (C compilers + Rust)
RUN yum install -y gcc gcc-c++ make wget tar gzip

# Install newer SQLite from source
RUN wget https://www.sqlite.org/2023/sqlite-autoconf-3430000.tar.gz && \
    tar xzf sqlite-autoconf-3430000.tar.gz && \
    cd sqlite-autoconf-3430000 && \
    ./configure --prefix=/usr/local && \
    make && \
    make install && \
    cd .. && \
    rm -rf sqlite-autoconf-3430000*

# Install Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Set library path for new SQLite
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Install Python packages to /var/task
COPY requirements-lambda.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements-lambda.txt --target /var/task

# Stage 2: Runtime (clean image without build tools)
FROM public.ecr.aws/lambda/python:3.10

# Copy SQLite library from builder
COPY --from=builder /usr/local/lib/libsqlite3.* /usr/local/lib/
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
ENV LD_PRELOAD=/usr/local/lib/libsqlite3.so

# Copy the installed packages from builder
COPY --from=builder /var/task/ ${LAMBDA_TASK_ROOT}/

# Copy application code
COPY backend/ ${LAMBDA_TASK_ROOT}/backend/

# Set the CMD
CMD ["backend.lambda_function.handler"]
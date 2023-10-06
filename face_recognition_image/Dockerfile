# Define custom function directory
ARG FUNCTION_DIR="/function"

FROM python:3.11 as build-image

# dep1

# Atualize a lista de pacotes e instale o aptitude
RUN apt-get update && apt-get install -y aptitude

# Use o aptitude para atualizar os pacotes
RUN aptitude update -y && aptitude safe-upgrade -y

# Instale pacotes essenciais
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl

# Instale pacotes relacionados a gráficos e vídeo
RUN apt-get install -y --fix-missing \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev

# Instale pacotes relacionados ao Boost e GTK
RUN apt-get install -y --fix-missing \
    libboost-all-dev \
    libgtk2.0-dev

# Instale pacotes relacionados a imagem e álgebra linear
RUN apt-get install -y --fix-missing \
    libjpeg-dev \
    liblapack-dev

# Instale pacotes Python e outras utilidades
RUN apt-get install -y --fix-missing \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip

# Limpe o cache e remova arquivos temporários para reduzir o tamanho da imagem
RUN apt-get clean && rm -rf /tmp/* /var/tmp/*


# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Copy function code
RUN mkdir -p ${FUNCTION_DIR}
COPY . ${FUNCTION_DIR}

# Install the function's dependencies
RUN pip3 install \
    --target ${FUNCTION_DIR} \
        awslambdaric
		
COPY requirements.txt ${FUNCTION_DIR}
RUN pip3 install \
    --target ${FUNCTION_DIR} \
    -r ${FUNCTION_DIR}/requirements.txt


# Use a slim version of the base Python image to reduce the final image size
FROM python:3.11-slim

# Atualize a lista de pacotes e instale o aptitude
RUN apt-get update && apt-get install -y aptitude

# Use o aptitude para atualizar os pacotes
RUN aptitude update -y && aptitude safe-upgrade -y

# Instale pacotes essenciais
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl

# Instale pacotes relacionados a gráficos e vídeo
RUN apt-get install -y --fix-missing \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev

# Instale pacotes relacionados ao Boost e GTK
RUN apt-get install -y --fix-missing \
    libboost-all-dev \
    libgtk2.0-dev

# Instale pacotes relacionados a imagem e álgebra linear
RUN apt-get install -y --fix-missing \
    libjpeg-dev \
    liblapack-dev

# Instale pacotes Python e outras utilidades
RUN apt-get install -y --fix-missing \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip

# Limpe o cache e remova arquivos temporários para reduzir o tamanho da imagem
RUN apt-get clean && rm -rf /tmp/* /var/tmp/*


# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
# Pass the name of the function handler as an argument to the runtime
CMD [ "lambda_function.handler" ]
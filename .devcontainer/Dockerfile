FROM python:3.12.9-bullseye

# uv（syncはdevcontainer.jsonで行う）
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# zsh
RUN apt update && apt install -y zsh git curl && \
    sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
ENV SHELL=/bin/zsh
CMD ["zsh"]

# 最適化ソルバ
# RUN apt install -y coinor-cbc coinor-libcbc-dev
RUN wget https://packages.gurobi.com/12.0/gurobi12.0.3_armlinux64.tar.gz -O /tmp/gurobi12.0.3_armlinux64.tar.gz \
    && mkdir -p /opt \
    && tar xvfz /tmp/gurobi12.0.3_armlinux64.tar.gz -C /opt \
    && rm /tmp/gurobi12.0.3_armlinux64.tar.gz
ENV GUROBI_HOME=/opt/gurobi1000/armlinux64
ENV PATH=$PATH:$GUROBI_HOME/bin
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$GUROBI_HOME/lib
FROM saimanoj123/dbfsfuse:7 
RUN apt-get update \
  && apt-get install -y openssh-server \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Warning: the created user has root permissions inside the container
# Warning: you still need to start the ssh process with `sudo service ssh start`
RUN useradd --create-home --shell /bin/bash --groups sudo ubuntu

RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install holidays==0.9.12
RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install lightgbm==2.3.1
RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install pmdarima==1.5.3
RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install stldecompose==0.0.5
RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install statsmodels==0.10.2

RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install croston==0.1.2.2
RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install arch==4.7.0
RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install xgboost==1.1.0
RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install tsfresh==0.14.1
RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install pycausalimpact==0.0.15

RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install nbconvert==5.6.1
RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install pyculiarity==0.0.7
RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install gbart==0.2.1
RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install tensorflow==2.3.1
RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install keras==2.4.3

RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install mlflow==1.9.1
RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install pystan==2.19.1.1
RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install fbprophet==0.5.0





RUN apt-get update \
  && apt-get install --yes software-properties-common apt-transport-https \
  && gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 \
  && gpg -a --export E298A3A825C0D65DFD57CBB651716619E084DAB9 | sudo apt-key add - \
  && add-apt-repository 'deb [arch=amd64,i386] https://cran.rstudio.com/bin/linux/ubuntu xenial-cran35/' \
  && apt-get update \
  && apt-get install --yes \
    libssl-dev \
    r-base \
    r-base-dev \
  && add-apt-repository -r 'deb [arch=amd64,i386] https://cran.rstudio.com/bin/linux/ubuntu xenial-cran35/' \
  && apt-key del E298A3A825C0D65DFD57CBB651716619E084DAB9 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# hwriterPlus is used by Databricks to display output in notebook cells
# Rserve allows Spark to communicate with a local R process to run R code
RUN R -e "install.packages(c('hwriterPlus'), repos='https://mran.revolutionanalytics.com/snapshot/2017-02-26')" \
 && R -e "install.packages(c('htmltools'), repos='https://cran.microsoft.com/')" \
 && R -e "install.packages('Rserve', repos='http://rforge.net/')"  \
 && R -e "install.packages('forecast', repos='https://cran.microsoft.com/snapshot/2019-11-01')"  \
 && R -e "install.packages('bnlearn', repos='https://cran.microsoft.com/snapshot/2019-11-01')"  
 
 
 
 
RUN /bin/sh -c /databricks/conda/envs/dcs-minimal/bin/pip install rpy2==3.2.6

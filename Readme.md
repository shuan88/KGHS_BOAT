
# Anaconda

1. Create a new environment `conda create --name <environment_name>`
2. activate the environment `conda activate <environment_name>`
3. install pip in environment `conda install pip`
4. install requirements.txt `while read requirement; do conda install --yes $requirement || pip install $requirement; done < requirements.txt`
5. (Optional) 


## 也可以这样子操作
1. 导出到.yml文件 `conda env export > freeze.yml`
2. 直接创建conda环境 `conda env create -f freeze.yml`
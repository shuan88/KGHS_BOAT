
# Anaconda

1. Create a new environment `conda create --name <environment_name>`
2. Activate the environment `conda activate <environment_name>`
3. Install pip in environment `conda install pip`
4. Install requirements.txt `while read requirement; do conda install --yes $requirement || pip install $requirement; done < requirements.txt`
5. (Optional) Export requirements.txt `conda list --explicit > requirements.txt`

## You can also use the following command to install all the requirements in one go
1. Export to .yml file `conda env export > freeze.yml`
2. To reproduce `conda env create -f freeze.yml`

> https://stackoverflow.com/questions/35802939/install-only-available-packages-using-conda-install-yes-file-requirements-t
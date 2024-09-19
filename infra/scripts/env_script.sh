#!/bin/bash

## Install ESA Snap
wget https://download.esa.int/step/snap/10_0/installers/esa-snap_all_linux-10.0.0.sh
chmod +x esa-snap_all_linux-10.0.0.sh
# Quiet mode to avoid prompts that block the execution
./esa-snap_all_linux-10.0.0.sh -q


## Install conda like that: https://docs.anaconda.com/miniconda/
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh

~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh


## Clone repo
git clone https://github.com/dimkirt/FLOODPY


## Create .cdsapirc - This we need to fetch from integrations
# Prompt the user for the key
read -p "Enter the Copernicus CDS key: " user_key

# Create the file with the specified content
cat << EOF > ~/.cdsapirc
url: https://cds-beta.climate.copernicus.eu/api
key: $user_key
EOF

echo "File '.cdsapirc' has been created with the provided key."

## Setup Python env
conda env create -f FLOODPY/FLOODPY_cpu_linux_vm.yml
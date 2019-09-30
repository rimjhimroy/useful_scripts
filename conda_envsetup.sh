# -------------
# Author: Rimjhim Roy Choudhury 
# tested with:
# conda 4.7.11
# usage:
# Create the conda environment
# conda create --name envname -c channel package1 package2
# source conda_envsetup.sh envname
# -------------
conda activate $1
#echo $CONDA_PREFIX
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
mkdir -p $CONDA_PREFIX/etc/conda/deactivate.d

cat <<EOF > $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
#!/bin/bash
export OLD_LD_LIBRARY_PATH=${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=${CONDA_PREFIX}/lib:${LD_LIBRARY_PATH}
EOF

cat <<EOF > $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
#!/bin/bash
export LD_LIBRARY_PATH=${OLD_LD_LIBRARY_PATH}
unset OLD_LD_LIBRARY_PATH
EOF
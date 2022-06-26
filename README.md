## [SIGCOMM'22] Vivisecting Mobility Management in 5G Cellular Networks

In this repository, we release the dataset and scripts use in SIGCOMM'22 paper, [Vivisecting Mobility Management in 5G Cellular Networks]().

This measurement paper involves several experiments, with different methodologies, conducted for several purposes. To help navigate the results easily, we have created separate [scripts](scripts) for each of the plots presented in the paper. We have also included the [datasets](data) (raw or processed) used to generate the results.

### Instructions to run the artifact

1. The scripts require python3 to be installed on the machine. We recommend that you also set up and activate a python virtual environment. Detailed instructions to set up virtualenv can be found [here](https://help.dreamhost.com/hc/en-us/articles/115000695551-Installing-and-using-virtualenv-with-Python-3).
2. Install the required python packages
   ```bash
   pip3 install -r requirements.txt
   ```
### Generate plots
Run the scripts one by one from inside the [scripts](scripts) folder. The generated results will be put in [plots](plots) folder.

### Generate ``prognos`` results
To generate results presented in Table 3 of the paper, navigate to the [src](src) folder and ``prognos`` or other comparative algorithms to get results. 

The results output by the scripts contain statistics for both 4G-LTE and 5G-NR radio interfaces.

> Note that we provide interactive notebooks for ``GBC`` and ``Stacked-LSTM`` which can be run directly on Google Colab.

If there are any questions, feel free to contact us ([hassa654@umn.edu](hassa654@umn.edu)).

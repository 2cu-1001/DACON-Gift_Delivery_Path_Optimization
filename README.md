# DACON-Gift_Delivery_Route_Optimization #
Delivery Path Optimization using Simulated Annealing


## Competition Page ##

https://dacon.io/competitions/official/236437/overview/description


# Installation #

    git clone https://github.com/2cu-1001/DACON-Gift_Delivery_Route_Optimization.git
    conda env create --file environment.yml



# Run #

    python main.py --T <initial Temperature> --T_final <final Temperature> --const <constant for log scaling> --max_iter <max iterations>
submission file will be generated => data/submission.csv

# Example output of SA #
### loss hist ###
![cost_hist](https://github.com/user-attachments/assets/c426fa4d-b874-4876-a4c0-f094c0d3afb3)


### path visuallization ###
![path_visualization](https://github.com/user-attachments/assets/9987e125-1d71-477e-ada9-81624f24f291)

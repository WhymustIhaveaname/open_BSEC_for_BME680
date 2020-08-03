### 20200503

Found the relationship between bvoc to co2 concentration, which is an exp function with a maximum cutting.

Found the relationship between siaq to co2 concentration, which is a piecewise linear function.

### 20200504

From the plot co2_res_05044, the function between resistance and temperature and co2 concentration is confirmed. The task remaining is to determinate the A parameter in the formula, denoted usually by bsec_a later.

### 20200507

Summerized bsec_b, bsec_c and two lrs from history data. Fix bsec_b to 3372\pm40, bsec_c to 4634\pm200, lr1 to 0.00184, lr2 to 0.00012.

### 20200517

Collected more data. Tried finite states machine but failed.

### 20200803

Pick up this work again. Clean up files and codes.

I am going to try this using a neural network. To this end, I will first test NN's ability of fitting exp and log, which may appear in bsec's real formula. As showed by the files in nn_exp, NN can fits exponential function very well with about 10 parameters and 2 to 3 layers.

Before beginning fitting data with NN, the errors of classical two learning rate are measured as following. Iaqdata 05082, 0520, 0522 are chosen as suitable train or test files, because of their size and data range.

item|size|number of datas|two lr err|two lr abs err|
:-:|:-:|:-:|:-:|:-:
05082|1.1M|104404|
0520 |2.4M|149084|
0522 |1.8M|61374 |
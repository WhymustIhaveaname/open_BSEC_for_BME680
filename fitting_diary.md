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

file|size|number of datas|two lr err|two lr abs err|shld err|shld abs err|
:--:|:--:|:-------------:|:--------:|:------------:|:------:|:----------:
05082|1.1M|104404|0.002708|0.03967|0.02712|0.1041
0520 |2.4M|149084|0.006010|0.06524|0.03664|0.1533
0522 |1.8M|61374 |0.007131|0.06880|0.04630|0.1777

### 20200804

I will first try RNN. If there is enough time, I will also try NEAT(NeuroEvolution of Augmenting Topologies).

A no hidden layer, fully connected, two h, no activation RNN is implemented([(3,2),(3,1)],12paras). Trained with 0520 after 100 iters, the err is optimized to 0.01478. But tested with 0522, the err is 1.1018. Also, the RNN using nn.Module is extremely slow, almost 1min each iter. I should optimize it first. Use `rnn.i2h.weight.data=` to manually set the values.  

Optimize the programme using nn.RNN. It becomes faster also still with some problems, which is that I have to split the 140000 sequence into 14 10000-sequence to make it faster. Anyway, it starts to train. Construct a naive, one linear layer, two hidden parameter RNN, train it with 0520 and test with 0522. It reached 0.009591(train) and 0.010034(test) after 100 iters. Although this is still worse than my genius two lr, it is better than straightly using shld.

Increase hidden parameter number to 8, 0.010857 and 0.009507 is achieved after 100 iters, which means that the weakness is the topology of output layer, not number of hidden paras. Reset num_h to 2, add another square linear layer and a relu layer. It reaches 0.009610 0.010049 after 50 iters. Increase num_h to 4, keep topology unchanged. The result get worse to 0.015646 0.013364. Increase num_h to 8, get 0.011392 0.009912. Change learnrate, no improve.


#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from ana_bsec import log,get_log_lines,get_bsec_a_from_log,gen_fake_a_twolr
import torch,copy,math,numpy
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

def calc_twolr_err(filename):
    bsec_a_shld,bsec_a_acct=get_bsec_a_from_log(filename)
    bsec_a_twolr=gen_fake_a_twolr(bsec_a_shld)
    #loss=F.mse_loss(torch.tensor(bsec_a_twolr),torch.tensor(bsec_a_acct))
    loss=torch.sum(torch.abs(torch.tensor(bsec_a_twolr)-torch.tensor(bsec_a_acct)))
    log(loss.item()/len(bsec_a_shld))

if __name__=="__main__":
    calc_twolr_err('iaqdata.05082')
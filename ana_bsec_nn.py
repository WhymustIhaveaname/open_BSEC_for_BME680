#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from ana_bsec import log,get_log_lines,get_bsec_a_from_log,gen_fake_a_twolr
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

def calc_twolr_err(filename):
    bsec_a_shld,bsec_a_acct=get_bsec_a_from_log(filename)
    bsec_a_twolr=gen_fake_a_twolr(bsec_a_shld)
    bsec_a_shld=torch.tensor(bsec_a_shld)
    bsec_a_acct=torch.tensor(bsec_a_acct)
    bsec_a_twolr=torch.tensor(bsec_a_twolr)
    loss1=F.mse_loss(bsec_a_twolr,bsec_a_acct)
    loss2=torch.sum(torch.abs(bsec_a_twolr-bsec_a_acct))/len(bsec_a_shld)
    loss3=F.mse_loss(bsec_a_shld,bsec_a_acct)
    loss4=torch.sum(torch.abs(bsec_a_shld-bsec_a_acct))/len(bsec_a_shld)
    log("%f|%f|%f|%f"%(loss1,loss2,loss3,loss4))

class BSEC_RNN_OLD(nn.Module):
    def __init__(self,input_size=1,hidden_size=2,output_size=1):
        super(BSEC_RNN_OLD,self).__init__()
        self.hidden_size=hidden_size
        self.i2h=nn.Linear(input_size+hidden_size,hidden_size)
        self.i2o=nn.Linear(input_size+hidden_size,output_size)
    
    def forward(self,input,hidden):
        combined=torch.cat((input,hidden))
        hidden=self.i2h(combined)
        output=self.i2o(combined)
        return output,hidden

    def init_hidden(self):
        return torch.zeros(self.hidden_size)

    def __str__(self):
        num_paras=sum([p.numel() for p in self.parameters()])
        stru=[]
        for name,child in self.named_children():
            stru.append(tuple(child.state_dict()['weight'].t().size()))
        return "%s %s %s"%(self.__class__.__name__,stru,num_paras)

class BSEC_RNN(nn.Module):
    def __init__(self,input_size=1,hidden_size=2,output_size=1):
        super(BSEC_RNN,self).__init__()
        self.hidden_size=hidden_size
        self.rnn=nn.RNN(input_size,hidden_size,batch_first=True)
        self.fc=nn.Linear(hidden_size+input_size,output_size)
    
    def forward(self,x):
        h0=torch.zeros(1,x.size(0),self.hidden_size)
        hen,h_n=self.rnn(x,h0)
        x=self.fc(torch.cat((x,hen),dim=2))
        return x

def try_rnn():
    rnn=BSEC_RNN()
    anatomise_nn(rnn)
    i=torch.tensor([[[1.0],[2.0],[3.0]]])
    rnn(i)

def anatomise_nn(net,structure_flag=True):
    if structure_flag:
        log(net)
    s_lt=[""]
    for name,child in net.named_children():
        s_dict=child.state_dict()
        s_temp=[]
        for k in s_dict:
            s_temp.append("%s: %s"%(k,s_dict[k].numpy()))
        s_lt.append("%s (%s)"%(", ".join(s_temp),name))
        #s_lt.append("%s + %s (%s)"%(s_dict['weight'].numpy(),s_dict['bias'].numpy(),name))
    log("\n".join(s_lt))

def load_data(filename,seq_len=10000):
    bsec_a_shld,bsec_a_acct=get_bsec_a_from_log(filename)
    shld_lt=[];acct_lt=[]
    i=0
    while (i+1)*seq_len<len(bsec_a_shld):
        shld_lt.append(torch.tensor([[i] for i in bsec_a_shld[i*seq_len:(i+1)*seq_len]]))
        acct_lt.append(torch.tensor([[i] for i in bsec_a_acct[i*seq_len:(i+1)*seq_len]]))
        i+=1
    bsec_a_shld=torch.stack(shld_lt)
    bsec_a_acct=torch.stack(acct_lt)
    log("load %s data from %s"%(bsec_a_shld.size(),filename))
    return bsec_a_shld,bsec_a_acct

def train():
    rnn=BSEC_RNN()
    anatomise_nn(rnn)
    train_shld,train_acct=load_data('iaqdata.0520')
    test_shld,test_acct=load_data('iaqdata.0522')
    criterion=nn.MSELoss()
    optimizer=optim.SGD(rnn.parameters(),lr=0.01,momentum=0)
    optimizer.zero_grad()
    log("begin trainging: %f, %f"%(test_err(rnn,train_shld,train_acct),test_err(rnn,test_shld,test_acct)))
    for epoch in range(101):
        output=rnn(train_shld)
        loss=criterion(output,train_acct)
        #log('begin backward')
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        if epoch%5==0:
            log("%3d: %f %f"%(epoch,loss.item(),test_err(rnn,test_shld,test_acct)))
    anatomise_nn(rnn,structure_flag=False)

def test_err(net,test_shld,test_acct):
    with torch.no_grad():
        output=net(test_shld)
        loss=F.mse_loss(output,test_acct)
    #log(output)
    #log(test_acct)
    #log("%f(%s)"%(loss.item(),test_shld.size()))
    return loss.item()

if __name__=="__main__":
    #calc_twolr_err('iaqdata.0522')
    train()
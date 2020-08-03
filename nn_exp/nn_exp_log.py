#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from ana_bsec import log
import torch,copy,math,numpy
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class NN_EXP(nn.Module):
    def __init__(self):
        super(NN_EXP,self).__init__()
        self.fc1=nn.Linear(1,4)
        self.fc2=nn.Linear(4,1)

    def forward(self, x):
        x=F.relu(self.fc1(x))
        x=self.fc2(x)
        return x

    def num_paras(self):
        return sum([p.numel() for p in self.parameters()])
    
    def num_layers(self):
        ax=0
        for name,child in self.named_children():
            ax+=1
        return ax

    def __str__(self):
        stru=[]
        for name,child in self.named_children():
            stru.append(tuple(child.state_dict()['weight'].t().size()))
        return "%s %s %s"%(self.__class__.__name__,stru,self.num_paras())

def loss_func(netout,target):
    loss=F.mse_loss(netout,target)
    return loss

def train(NetClass):
    traindata=[[torch.tensor([i,],dtype=torch.float32),torch.tensor([numpy.exp(i),],dtype=torch.float32)] 
              for i in numpy.linspace(0,numpy.log(1000),1001)]
    batch_size=1001
    trainloader=torch.utils.data.DataLoader(traindata,shuffle=True,batch_size=batch_size,drop_last=True)
    train_iter_num=int(len(traindata)/batch_size)
    testdata=[[torch.tensor([i,],dtype=torch.float32),torch.tensor([numpy.exp(i),],dtype=torch.float32)] 
              for i in numpy.linspace(numpy.log(0.8),numpy.log(1200),101)]
    testloder=torch.utils.data.DataLoader(testdata,batch_size=len(testdata))

    net=NetClass()
    #net=net.double()
    log(net)
    test_i=testloder.__iter__().__next__()
    netout=net(test_i[0])
    test_loss=loss_func(netout,test_i[1])
    log("random init: %f"%(test_loss))
    log("epoch num: train_loss test_loss")
    optimizer=optim.SGD(net.parameters(),lr=0.0001,momentum=0)
    optimizer.zero_grad()
    scheduler=torch.optim.lr_scheduler.MultiStepLR(optimizer,[5000,10000,15000],gamma=0.2)
    for epoch in range(30000):
        running_loss=0
        for i in trainloader:
            netout=net(i[0])
            loss=loss_func(netout,i[1])
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            running_loss+=loss.item()
        scheduler.step()
        if epoch%1000==0:
            with torch.no_grad():
                netout=net(test_i[0])
                test_loss=loss_func(netout,test_i[1])
            log("%3d: %f %f"%(epoch,running_loss/train_iter_num,test_loss))
    #return
    save_name='%s_%s_%s.ckpt'%(net.__class__.__name__,net.num_layers(),net.num_paras())
    torch.save(net,save_name)
    log("saved net to %s"%(save_name))

def draw_fit(netfile):
    net=torch.load(netfile+'.ckpt')
    testdata=[[torch.tensor([i,],dtype=torch.float32),torch.tensor([numpy.exp(i),],dtype=torch.float32)] 
              for i in numpy.linspace(numpy.log(0.8),numpy.log(1200),101)]
    testloder=torch.utils.data.DataLoader(testdata,batch_size=len(testdata))
    i=testloder.__iter__().__next__()
    netout=net(i[0])
    test_loss=loss_func(netout,i[1]).item()
    xs=i[0].view(1,-1).tolist()[0]
    ys_corr=i[1].view(1,-1).tolist()[0]
    ys_fit=netout.view(1,-1).tolist()[0]
    
    import matplotlib.pyplot as plt
    fig=plt.figure()
    ax1=fig.subplots(1)
    mks=3
    ax1.plot(xs,ys_corr,'o',markersize=mks,label="exp(x)")
    ax1.plot(xs,ys_fit,'x',markersize=mks,label=netfile)
    ax1.legend(loc=2)
    plt.title("%s: %.1f"%(str(net),test_loss))
    plt.savefig("%s.png"%(netfile))
    plt.show()

if __name__=="__main__":
    #train(NN_EXP)
    draw_fit("NN_EXP_3_33")
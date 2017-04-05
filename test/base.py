import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F

import os
import uuid
import torch2c


def base_test():

    fc1 = nn.Linear(10,20)
    fc1.weight.data.normal_(0.0,1.0)
    fc1.bias.data.normal_(0.0,1.0)

    fc2 = nn.Linear(20,2)
    fc2.weight.data.normal_(0.0,1.0)
    fc2.bias.data.normal_(0.0,1.0)

    model_0 = lambda x: F.log_softmax(fc2(F.relu(fc1(x))))

    fc3 = nn.Linear(10,2)
    fc3.weight.data.normal_(0.0,1.0)
    fc3.bias.data.normal_(0.0,1.0)

    fc4 = nn.Linear(10,2)
    fc4.weight.data.normal_(0.0,1.0)
    fc4.bias.data.normal_(0.0,1.0)

    softmax = nn.Softmax()

    model_1 = lambda x: F.softmax(F.elu(fc3(x)))
    model_2 = lambda x: F.softmax(F.tanh(fc3(x)))
    model_3 = lambda x: F.softmax(F.sigmoid(fc3(x)))
    model_4 = lambda x: softmax(F.leaky_relu(fc4(x)))
    model_5 = lambda x: softmax(F.logsigmoid(fc4(x)))

    model_6 = lambda x: fc3(F.max_pool2d(x.unsqueeze(dim=0),2).squeeze())
    model_7 = lambda x: fc3(F.max_pool2d(x.unsqueeze(dim=0),2).squeeze(dim=0))
    model_8 = lambda x: fc3(F.max_pool3d(x.unsqueeze(0),2).squeeze())

    data = Variable(torch.rand(10,10))
    data2 = Variable(torch.rand(20,20))
    data3 = Variable(torch.rand(2,20,20))

    out = model_0(data) + \
          model_1(data) * model_2(data) / model_3(data) / 2.0 + \
          2.0 * model_4(data) + model_5(data) + 1 - 2.0 + \
          model_6(data2) + model_7(data2) + model_8(data3)

    out_path = 'out'
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    uid = str(uuid.uuid4())

    torch2c.compile(out,'base',os.path.join(out_path,uid),compile_test=True)
 

if __name__=='__main__':

    base_test()

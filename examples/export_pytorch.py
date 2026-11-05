"""Export a small CNN as dense GEMMs. CPU, batch size one."""
import csv
from pathlib import Path
import torch
from torch import nn

class MyCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features=nn.Sequential(
            nn.Conv2d(3,32,3,padding=1),nn.ReLU(),nn.MaxPool2d(2),
            nn.Conv2d(32,64,3,stride=2,padding=1),nn.ReLU())
        self.fc=nn.Linear(64*8*8,10)
    def forward(self,x):
        return self.fc(torch.flatten(self.features(x),1))

def export(model,shape,out):
    rows=[]; handles=[]
    def hook(name):
        def record(m,inputs,output):
            x=inputs[0]
            if isinstance(m,nn.Conv2d):
                if (m.groups!=1 or m.dilation!=(1,1) or
                    m.stride[0]!=m.stride[1] or isinstance(m.padding,str) or
                    m.padding_mode!='zeros'):
                    raise ValueError('Unsupported groups, dilation, stride or padding: '+name)
                if x.shape[0]!=1: raise ValueError('Use batch size one')
                rows.append([name,output.shape[2]*output.shape[3],
                             m.out_channels,m.kernel_size[0]*m.kernel_size[1]*m.in_channels])
            else:
                if x.ndim!=2 or x.shape[0]!=1:
                    raise ValueError('Linear export requires one flattened sample: '+name)
                rows.append([name,1,m.out_features,m.in_features])
        return record
    for name,m in model.named_modules():
        if isinstance(m,(nn.Conv2d,nn.Linear)):
            handles.append(m.register_forward_hook(hook(name)))
    model.eval()
    try:
        with torch.no_grad(): model(torch.zeros(1,*shape))
    finally:
        for h in handles: h.remove()
    with Path(out).open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerow(['Layer','M','N','K',''])
        writer.writerows([*r,''] for r in rows)
    print(f'Wrote {len(rows)} layers to {out}')

if __name__=='__main__':
    export(MyCNN(),(3,32,32),Path(__file__).with_name('my_model.csv'))

#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import os, re, sys
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

class DealDataset(Dataset):
    def __init__(self, np_data):
        self.__np_data = np_data
        self.X = torch.from_numpy(self.__np_data[:, 1:])
        self.y = torch.from_numpy(self.__np_data[:, 0]).view(-1, 1)
        self.len = self.__np_data.shape[0]

    def __getitem__(self, index):
        return self.X[index], self.y[index]

    def __len__(self):
        return self.len

class CNN_Feature2d(nn.Module):
    def __init__(self, device, out_channels, conv_kernel_size=5, pool_kernel_size=2, dense_size=64, dropout=0.5):
        super(CNN_Feature2d, self).__init__()
        self.device = device
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=out_channels, kernel_size=conv_kernel_size, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=pool_kernel_size)
        )
        self.dropout1 = nn.Dropout(dropout)
        self.conv2= nn.Sequential(
            nn.Conv2d(in_channels=out_channels, out_channels=out_channels, kernel_size=conv_kernel_size, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=pool_kernel_size)
        )
        self.dropout2 = nn.Dropout(dropout)
        self.conv3= nn.Sequential(
            nn.Conv2d(in_channels=out_channels, out_channels=out_channels, kernel_size=conv_kernel_size, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=pool_kernel_size)
        )
        self.dropout3 = nn.Dropout(dropout)
        self.conv4= nn.Sequential(
            nn.Conv2d(in_channels=out_channels, out_channels=2*out_channels, kernel_size=conv_kernel_size, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=pool_kernel_size)
        )
        self.dropout4 = nn.Dropout(dropout)
        self.fc1 = nn.Linear(9*out_channels, dense_size)
        self.fc2 = nn.Linear(dense_size, 1)
    
    def forward(self, X, is_train=False):
        out = X.view(-1, 3, 29, 29)        
        out = self.conv1(out)
        # print('Conv1: ', out.size())
        if is_train:
            out = self.dropout1(out)
        out = self.conv2(out)
        # print('Conv2: ', out.size())
        if is_train:
            out = self.dropout2(out)
        out = self.conv3(out)
        # print('Conv3: ', out.size())
        if is_train:
            out = self.dropout3(out)
        # out = self.conv4(out)
        # print('Conv4: ', out.size())
        # sys.exit(0)
        # if is_train:
        #     out = self.dropout4(out)
        # print(out.size())
        # sys.exit()
        out = out.view(out.size(0), -1)
        # print(out.size())
        # sys.exit()
        out = F.relu(self.fc1(out))        
        out = torch.sigmoid(self.fc2(out))
        return out
    
    def predict(self, loader):
        score = []
        for batch_X, batch_y in loader:            
            Xb = batch_X.to(self.device)
            yb = batch_y.to(self.device)
            y_ = self.forward(Xb)
            score.append(y_.cpu().data)
        return torch.cat(score).numpy()[:, 0]

def pep1(file):
    try:
        AA = '-ARNDCQEGHILKMFPSTWYV'
        if os.path.exists(file) == False:
            return False, None
        
        with open(file) as f:
            record = f.read()
        
        records = record.split('>')[1:]
        myFasta = []
        for fasta in records:
            array = fasta.split('\n')
            name, sequence = array[0].split()[0], ''.join(array[1:]).upper()
            myFasta.append([name, sequence])
        
        seqs = []
        for fa in myFasta:
            name, sequence = fa[0], re.sub('[^ACDEFGHIKLMNPQRSTVWY]', '-', fa[1])
            for i in range(len(sequence)):
                if sequence[i] == 'K':
                    myStr = ''
                    for j in range(i-14, i+15):
                        if j in range(len(sequence)):
                            myStr += sequence[j]
                        else:
                            myStr += '-'
                    seqs.append([name+"_"+str(j+1), myStr, 0, 'testing'])
        return True, seqs
    except Exception as e:
        return False, None

def encoding(samples):
    try:
        with open('../../AAindex_normalized.txt') as f:
            records = f.readlines()[1:]

        AA_aaindex = 'ARNDCQEGHILKMFPSTWYV'
        AAindex = []
        AAindexName = []
        for i in records:
            AAindex.append(i.rstrip().split()[1:] if i.rstrip() != '' else None)
            AAindexName.append(i.rstrip().split()[0] if i.rstrip() != '' else None)

        props = 'FINA910104:LEVM760101:JACR890101:ZIMJ680104:RADA880108:JANJ780101:CHOC760102:NADH010102:KYTJ820101:NAKH900110:GUYH850101:EISD860102:HUTJ700103:OLSK800101:JURD980101:FAUJ830101:OOBM770101:GARJ730101:ROSM880102:RICJ880113:KIDA850101:KLEP840101:FASG760103:WILM950103:WOLS870103:COWR900101:KRIW790101:AURR980116:NAKH920108'.split(':')
        if props:
            tmpIndexNames = []
            tmpIndex = []
            for p in props:
                if AAindexName.index(p) != -1:
                    tmpIndexNames.append(p)
                    tmpIndex.append(AAindex[AAindexName.index(p)])
            if len(tmpIndexNames) != 0:
                AAindexName = tmpIndexNames
                AAindex = tmpIndex
        
        index = {}
        for i in range(len(AA_aaindex)):
            index[AA_aaindex[i]] = i

        blosum62 = {
            'A': [4,  -1, -2, -2, 0,  -1, -1, 0, -2,  -1, -1, -1, -1, -2, -1, 1,  0,  -3, -2, 0],  # A
            'R': [-1, 5,  0,  -2, -3, 1,  0,  -2, 0,  -3, -2, 2,  -1, -3, -2, -1, -1, -3, -2, -3], # R
            'N': [-2, 0,  6,  1,  -3, 0,  0,  0,  1,  -3, -3, 0,  -2, -3, -2, 1,  0,  -4, -2, -3], # N
            'D': [-2, -2, 1,  6,  -3, 0,  2,  -1, -1, -3, -4, -1, -3, -3, -1, 0,  -1, -4, -3, -3], # D
            'C': [0,  -3, -3, -3, 9,  -3, -4, -3, -3, -1, -1, -3, -1, -2, -3, -1, -1, -2, -2, -1], # C
            'Q': [-1, 1,  0,  0,  -3, 5,  2,  -2, 0,  -3, -2, 1,  0,  -3, -1, 0,  -1, -2, -1, -2], # Q
            'E': [-1, 0,  0,  2,  -4, 2,  5,  -2, 0,  -3, -3, 1,  -2, -3, -1, 0,  -1, -3, -2, -2], # E
            'G': [0,  -2, 0,  -1, -3, -2, -2, 6,  -2, -4, -4, -2, -3, -3, -2, 0,  -2, -2, -3, -3], # G
            'H': [-2, 0,  1,  -1, -3, 0,  0,  -2, 8,  -3, -3, -1, -2, -1, -2, -1, -2, -2, 2,  -3], # H
            'I': [-1, -3, -3, -3, -1, -3, -3, -4, -3, 4,  2,  -3, 1,  0,  -3, -2, -1, -3, -1, 3],  # I
            'L': [-1, -2, -3, -4, -1, -2, -3, -4, -3, 2,  4,  -2, 2,  0,  -3, -2, -1, -2, -1, 1],  # L
            'K': [-1, 2,  0,  -1, -3, 1,  1,  -2, -1, -3, -2, 5,  -1, -3, -1, 0,  -1, -3, -2, -2], # K
            'M': [-1, -1, -2, -3, -1, 0,  -2, -3, -2, 1,  2,  -1, 5,  0,  -2, -1, -1, -1, -1, 1],  # M
            'F': [-2, -3, -3, -3, -2, -3, -3, -3, -1, 0,  0,  -3, 0,  6,  -4, -2, -2, 1,  3,  -1], # F
            'P': [-1, -2, -2, -1, -3, -1, -1, -2, -2, -3, -3, -1, -2, -4, 7,  -1, -1, -4, -3, -2], # P
            'S': [1,  -1, 1,  0,  -1, 0,  0,  0,  -1, -2, -2, 0,  -1, -2, -1, 4,  1,  -3, -2, -2], # S
            'T': [0,  -1, 0,  -1, -1, -1, -1, -2, -2, -1, -1, -1, -1, -2, -1, 1,  5,  -2, -2, 0],  # T
            'W': [-3, -3, -4, -4, -2, -2, -3, -2, -2, -3, -2, -3, -1, 1,  -4, -3, -2, 11, 2,  -3], # W
            'Y': [-2, -2, -2, -3, -2, -1, -2, -3, 2,  -1, -1, -2, -1, 3,  -3, -2, -2, 2,  7,  -1], # Y
            'V': [0,  -3, -3, -3, -1, -2, -2, -3, -3, 3,  1,  -2, 1,  -1, -2, -2, 0,  -3, -1, 4],  # V
            '-': [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # -
        }

        for key in blosum62:
            for j, value in enumerate(blosum62[key]):
                blosum62[key][j] = round((value+4)/15, 3)

        encoding_aaindex = []
        for i in samples:
            name, sequence, label = i[0], i[1], i[2]
            code = [name, label]
            for aa in sequence:            
                if aa == '-':
                    for j in AAindex:
                        code.append(0)
                    continue
                for j in AAindex:                
                    code.append(j[index[aa]])
            encoding_aaindex.append(code)
        
        AA = 'ARNDCQEGHILKMFPSTWYV'
        encoding_binary = []
        for i in samples:
            name, sequence, label = i[0], i[1], i[2]
            code = [name, label]
            for aa in sequence:
                if aa == '-':
                    code = code + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    code += [0.05] * 9
                    continue
                for aa1 in AA:
                    tag = 1 if aa == aa1 else 0
                    code.append(tag)
                code += [0.05] * 9
            encoding_binary.append(code)
        
        encoding_blosum = []
        for i in samples:
            name, sequence, label = i[0], i[1], i[2]
            code = [name, label]
            for aa in sequence:
                code = code + blosum62[aa]
                code += [0.267] * 9
            encoding_blosum.append(code)

        encoding_aaindex = np.array(encoding_aaindex)
        encoding_binary = np.array(encoding_binary)
        encoding_blosum = np.array(encoding_blosum)
        
        encodings = np.hstack((encoding_aaindex[:, 1:], encoding_binary[:, 2:], encoding_blosum[:, 2:]))
        return True, encodings.astype(np.float32)
    except Exception as e:
        return False, None

def generateHtml(pd_result, file):
    header = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>LEMP prediction result</title>
<link rel="stylesheet" type="text/css" href="../../style.css" media="screen" />
</head>
<body>
<div id="header">
    <div id="logo">
        <h1><a href="#">&nbsp;</a></h1>
        <p>A predictor of protein crotonylation sites<a href="#"></a></p>
    </div>
    <!-- end #logo -->
    <div id="menu">
        <ul>
            <li class="first"><a href="../../index.php?page=introduction">Introduction</a></li>
            <li><a href="../../index.php?page=prediction">Prediction</a></li>
            <li><a href="../../index.php?page=help">Help</a></li>
            <li><a href="../../index.php?page=download">Download</a></li>
            <li><a href="../../index.php?page=contact">Contact Us</a></li>
        </ul>
    </div>
    <!-- end #menu -->
</div>
<div id="page1">
<a href="./nhKCR_Pred.txt">The text format:</a><br />
============================================================================================
<table width="700" border="1" cellspacing="0" cellpadding="0" bordercolor="#000000" class="tableBasic1">
    <tr>
        <th width="30%">Sample</th>       
        <th width="60%">Peptide</th>
        <th width="10%">Score</th>
        <th>Prediction</th>
    </tr>
    '''
    tail = '''
</table>
<br /><br />
============================================================================================
<h3>Legend:</h3>
<table width="450" border="1" cellspacing="0" cellpadding="0">
    <tr>
        <td width="83" height="25" align="center" valign="middle" bgcolor="#3399FF"><strong>Label</strong></td>
        <td width="148" align="center" valign="middle" bgcolor="#3399FF"><strong>Score Range</strong></td>
        <td width="107" align="center" valign="middle" bgcolor="#3399FF"><strong>Sensitivity </strong>
        <td width="100" align="center" valign="middle" bgcolor="#3399FF"><strong>Specificity</strong></td>
    </tr>
    <tr>
        <td align="center" valign="middle" bgcolor="#CC66FF"><strong>Medium</strong></td>
        <td align="center" valign="middle">[0.265 - 0.447) </td>
        <td align="center" valign="middle">77.75%</td>
        <td align="center" valign="middle">80.0%</td>
    </tr>
    <tr>
        <td align="center" valign="middle" bgcolor="#FF0000"><strong>High</strong></td>
        <td align="center" valign="middle">[0.447 - 1] </td>
        <td align="center" valign="middle">56.63%</td>
        <td align="center" valign="middle">90.0%</td>
    </tr>
</table><br />

</div>
<!-- end #page -->
<div id="footer">
    <p>&copy; 2018. All Rights Reserved. Design by Yzchen.<br />
    </p>
</div>
<!-- end #footer -->
</body>
</html>
    '''
    f = open(file, 'w')
    ftext = open('nhKCR_Pred.txt', 'w')
    f.write(header+'\n')
    ftext.write('Samples\tPeptide\tScore\tPrediction\n')
    for i in range(len(pd_result)):
        f.write('<tr>\n')
        f.write('<td>%s</td><td class="word">%s</td><td>%.4f</td>' %(pd_result.iloc[i, 0], pd_result.iloc[i, 1], float(pd_result.iloc[i, 2])))
        ftext.write('%s\t%s\t%.4f\t' %(pd_result.iloc[i, 0], pd_result.iloc[i, 1], float(pd_result.iloc[i, 2])))
        score = float(pd_result.iloc[i, 2])
        if score >= 0.447:
            f.write('<td class="highest">Yes</td>')
            ftext.write('Yes (high confidence)\n')
        elif score >= 0.265:
            f.write('<td class="high">Yes</td>')
            ftext.write('Yes (medium confidence)\n')
        else:
            f.write('<td>No</td>')
            ftext.write('No\n')
        f.write('</tr>\n')
    f.write(tail+'\n')
    ftext.close()
    f.close()


if __name__ == '__main__':    
    workDir = 'public/' + sys.argv[1]
    os.chdir(workDir)
    device = 'cpu'

    error_msg = []
    ok, samples = pep1('sequence.txt')
    pd_result = None
    if ok:
        ok_encoding, data_test = encoding(samples)
        if ok_encoding:            
            try:
                ind_set = DealDataset(data_test.astype(np.float32))

                ind = np.zeros((len(ind_set), 2))
                ind[:, 0] = data_test[:, 0].astype(np.float32)
                ind_loader = DataLoader(ind_set, batch_size=64, shuffle=False)

                model = CNN_Feature2d(device, 128, 5, 2, 64, 0.5)
                for i in range(5):
                    model.load_state_dict(torch.load('../../models/Merged_%s.pkl' %(i+1), map_location=device))
                    ind[:, 1] += model.predict(ind_loader)
                ind[:, 1] /= 5
                
                tmp_sample = np.array(samples)            
                pd_result = pd.DataFrame(np.hstack((tmp_sample[:, 0:2], ind[:, 1].reshape((-1, 1)))), columns=['Samples', 'Peptide', 'Score'])
            except Exception as e:
                pd_result = None
        else:
            error_msg.append('Feature encode error.')
    else:
        error_msg.append('Prepare sample failed.')

    generateHtml(pd_result, 'result.php')
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder,MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split, ParameterGrid
from sklearn.metrics import accuracy_score, confusion_matrix, mean_squared_error, log_loss
import operator
import json
from IPython import display
import os
import warnings

np.random.seed(0)
warnings.filterwarnings("ignore")
THRESHOLD = 4
import matplotlib
get_ipython().run_line_magic('matplotlib', 'inline')


# Task: To predict whether the user likes the mobile phone or not. <br>
# Assumption: If the average rating of mobile >= threshold, then the user likes it, otherwise not.

# <b>Missing values:</b><br>
# 'Also Known As'(459),'Applications'(421),'Audio Features'(437),'**Bezel-less display**'(266),'Browser'(449),'Build Material'(338),'Co-Processor'(451),'Display Colour'(457),'Mobile High-Definition Link(MHL)'(472),'Music'(447)
# 'Email','**Fingerprint Sensor Position**'(174),'Games'(446),'HDMI'(454),'Heart Rate Monitor'(467),'IRIS Scanner'(467),
# '**Optical Image Stabilisation**'(219),'Other Facilities'(444),'Phone Book'(444),'Physical Aperture'(87),'**Quick Charging**'(122),'Ring Tone'(444),'Ruggedness'(430),SAR Value(315),'SIM 3'(472),'SMS'(470)', 'Screen Protection'(229),'**Screen to Body Ratio** (claimed by the brand)'(428),'Sensor'(242),'Software Based Aperture'(473),
# '**Special Features**'(459),'Standby time'(334),'Stylus'(473),'TalkTime'(259), '**USB Type-C**'(374),'Video Player'(456),
# 'Video Recording Features'(458),'**Waterproof**'(398),'**Wireless Charging**','**USB OTG Support**'(159), 'Video ,'Recording'(113),'Java'(471),'Browser'(448)
# 
# <b>Very low variance:</b><br>
# 'Architecture'(most entries are 64-bit),'Audio Jack','GPS','Loudspeaker','Network','Network Support','Other Sensors'(28),'SIM Size', 'VoLTE'
# 
# 
# <b>Multivalued:</b><br>
# 'Colours','Custom UI','Model'(1),'Other Sensors','Launch Date'
# 
# <b>Not important:</b><br>
# 'Bluetooth', 'Settings'(75),'Wi-Fi','Wi-Fi Features'
# 
# <b>Doubtful:</b><br>
# 'Aspect Ratio','Autofocus','Brand','Camera Features','Fingerprint Sensor'(very few entries are missing),
# 'Fingerprint Sensor Position', 'Graphics'(multivalued),'Image resolution'(multivalued),'SIM Size','Sim Slot(s)', 'User Available Storage', 'SIM 1', 'SIM 2','Shooting Modes', 'Touch Screen'(24), 'USB Connectivity'
#     
# <b>To check:</b><br>
# 'Display Type','Expandable Memory','FM Radio'
# 
# <b>High Correlation with other features</b><br>
# 'SIM Slot(s)' high correlation with SIM1
# 'Weight' has high high correlation with capacity , screen-to-body ratio
# 'Height' - screen size is also there
#     
# <b>Given a mobile, we can't directly get these features</b><br>
# 'Rating Count', 'Review Count'
# 
# <b>Keeping:</b><br>
# 'Capacity','Flash'(17),'Height'(22),'Internal Memory'(20, require cleaning),'Operating System'(25, require cleaning), 'Pixel Density'(1, clean it),'Processor'(22, clean it), 'RAM'(17, clean), 'Rating','Resolution'(cleaning), 'Screen Resolution','Screen Size', 'Thickness'(22), 'Type','User Replaceable','Weight'(cleaning),'Sim Size'(), 'Other Sensors'(28), 'Screen to Body Ratio (calculated)','Width',
# 

# In[2]:


# read data from file
train = pd.read_csv("../input/train.csv") 
test = pd.read_csv("../input/test.csv")

# check the number of features and data points in train
print("Number of data points in train: %d" % train.shape[0])
print("Number of features in train: %d" % train.shape[1])

# check the number of features and data points in test
print("Number of data points in test: %d" % test.shape[0])
print("Number of features in test: %d" % test.shape[1])


# In[3]:


def data_clean(data):
    
    # Let's first remove all missing value features
    columns_to_remove = ['Also Known As','Applications','Audio Features','Bezel-less display'
                         'Browser','Build Material','Co-Processor','Browser'
                         'Display Colour','Mobile High-Definition Link(MHL)',
                         'Music', 'Email','Fingerprint Sensor Position',
                         'Games','HDMI','Heart Rate Monitor','IRIS Scanner', 
                         'Optical Image Stabilisation','Other Facilities',
                         'Phone Book','Physical Aperture','Quick Charging',
                         'Ring Tone','Ruggedness','SAR Value','SIM 3','SMS',
                         'Screen Protection','Screen to Body Ratio (claimed by the brand)',
                         'Sensor','Software Based Aperture', 'Special Features',
                         'Standby time','Stylus','TalkTime', 'USB Type-C',
                         'Video Player', 'Video Recording Features','Waterproof',
                         'Wireless Charging','USB OTG Support', 'Video Recording','Java']

    columns_to_retain = list(set(data.columns)-set(columns_to_remove))
    data = data[columns_to_retain]

    #Features having very low variance 
    columns_to_remove = ['Architecture','Audio Jack','GPS','Loudspeaker','Network','Network Support','VoLTE']
    columns_to_retain = list(set(data.columns)-set(columns_to_remove))
    data = data[columns_to_retain]

    # Multivalued:
    columns_to_remove = ['Architecture','Launch Date','Audio Jack','GPS','Loudspeaker','Network','Network Support','VoLTE', 'Custom UI']
    columns_to_retain = list(set(data.columns)-set(columns_to_remove))
    data = data[columns_to_retain]

    # Not much important
    columns_to_remove = ['Bluetooth', 'Settings','Wi-Fi','Wi-Fi Features']
    columns_to_retain = list(set(data.columns)-set(columns_to_remove))
    data = data[columns_to_retain]
    
    return data


# # Removing features

# In[4]:


train = data_clean(train)
test = data_clean(test)


# removing all those data points in which more than 15 features are missing 

# In[5]:


train = train[(train.isnull().sum(axis=1) <= 15)]
# You shouldn't remove data points from test set
#test = test[(test.isnull().sum(axis=1) <= 15)]


# In[6]:


# check the number of features and data points in train
print("Number of data points in train: %d" % train.shape[0])
print("Number of features in train: %d" % train.shape[1])

# check the number of features and data points in test
print("Number of data points in test: %d" % test.shape[0])
print("Number of features in test: %d" % test.shape[1])


# # Filling Missing values

# In[7]:


def for_integer(test):
    try:
        test = test.strip()
        return int(test.split(' ')[0])
    except IOError:
           pass
    except ValueError:
        pass
    except:
        pass

def for_string(test):
    try:
        test = test.strip()
        return (test.split(' ')[0])
    except IOError:
        pass
    except ValueError:
        pass
    except:
        pass

def for_float(test):
    try:
        test = test.strip()
        return float(test.split(' ')[0])
    except IOError:
        pass
    except ValueError:
        pass
    except:
        pass
def find_freq(test):
    try:
        test = test.strip()
        test = test.split(' ')
        if test[2][0] == '(':
            return float(test[2][1:])
        return float(test[2])
    except IOError:
        pass
    except ValueError:
        pass
    except:
        pass

    
def for_Internal_Memory(test):
    try:
        test = test.strip()
        test = test.split(' ')
        if test[1] == 'GB':
            return int(test[0])
        if test[1] == 'MB':
#             print("here")
            return (int(test[0]) * 0.001)
    except IOError:
           pass
    except ValueError:
        pass
    except:
        pass
    
def find_freq(test):
    try:
        test = test.strip()
        test = test.split(' ')
        if test[2][0] == '(':
            return float(test[2][1:])
        return float(test[2])
    except IOError:
        pass
    except ValueError:
        pass
    except:
        pass


# In[8]:


def data_clean_2(x):
    data = x.copy()
    
    data['Capacity'] = data['Capacity'].apply(for_integer)

    data['Height'] = data['Height'].apply(for_float)
    data['Height'] = data['Height'].fillna(data['Height'].mean())

    data['Internal Memory'] = data['Internal Memory'].apply(for_Internal_Memory)

    data['Pixel Density'] = data['Pixel Density'].apply(for_integer)

    data['Internal Memory'] = data['Internal Memory'].fillna(data['Internal Memory'].median())
    data['Internal Memory'] = data['Internal Memory'].astype(int)

    data['RAM'] = data['RAM'].apply(for_integer)
    data['RAM'] = data['RAM'].fillna(data['RAM'].median())
    data['RAM'] = data['RAM'].astype(int)

    data['Resolution'] = data['Resolution'].apply(for_integer)
    data['Resolution'] = data['Resolution'].fillna(data['Resolution'].median())
    data['Resolution'] = data['Resolution'].astype(int)

    data['Screen Size'] = data['Screen Size'].apply(for_float)

    data['Thickness'] = data['Thickness'].apply(for_float)
    data['Thickness'] = data['Thickness'].fillna(data['Thickness'].mean())
    data['Thickness'] = data['Thickness'].round(2)

    data['Type'] = data['Type'].fillna('Li-Polymer')

    data['Screen to Body Ratio (calculated)'] = data['Screen to Body Ratio (calculated)'].apply(for_float)
    data['Screen to Body Ratio (calculated)'] = data['Screen to Body Ratio (calculated)'].fillna(data['Screen to Body Ratio (calculated)'].mean())
    data['Screen to Body Ratio (calculated)'] = data['Screen to Body Ratio (calculated)'].round(2)

    data['Width'] = data['Width'].apply(for_float)
    data['Width'] = data['Width'].fillna(data['Width'].mean())
    data['Width'] = data['Width'].round(2)

    data['Flash'][data['Flash'].isna() == True] = "Other"

    data['User Replaceable'][data['User Replaceable'].isna() == True] = "Other"

    data['Num_cores'] = data['Processor'].apply(for_string)
    data['Num_cores'][data['Num_cores'].isna() == True] = "Other"


    data['Processor_frequency'] = data['Processor'].apply(find_freq)
    #because there is one entry with 208MHz values, to convert it to GHz
    data['Processor_frequency'][data['Processor_frequency'] > 200] = 0.208
    data['Processor_frequency'] = data['Processor_frequency'].fillna(data['Processor_frequency'].mean())
    data['Processor_frequency'] = data['Processor_frequency'].round(2)

    data['Camera Features'][data['Camera Features'].isna() == True] = "Other"

    #simplifyig Operating System to os_name for simplicity
    data['os_name'] = data['Operating System'].apply(for_string)
    data['os_name'][data['os_name'].isna() == True] = "Other"

    data['Sim1'] = data['SIM 1'].apply(for_string)

    data['SIM Size'][data['SIM Size'].isna() == True] = "Other"

    data['Image Resolution'][data['Image Resolution'].isna() == True] = "Other"

    data['Fingerprint Sensor'][data['Fingerprint Sensor'].isna() == True] = "Other"

    data['Expandable Memory'][data['Expandable Memory'].isna() == True] = "No"

    data['Weight'] = data['Weight'].apply(for_integer)
    data['Weight'] = data['Weight'].fillna(data['Weight'].mean())
    data['Weight'] = data['Weight'].astype(int)

    data['SIM 2'] = data['SIM 2'].apply(for_string)
    data['SIM 2'][data['SIM 2'].isna() == True] = "Other"
    
    return data


# In[9]:


train = data_clean_2(train)
test = data_clean_2(test)

# check the number of features and data points in train
print("Number of data points in train: %d" % train.shape[0])
print("Number of features in train: %d" % train.shape[1])

# check the number of features and data points in test
print("Number of data points in test: %d" % test.shape[0])
print("Number of features in test: %d" % test.shape[1])


# Not very important feature

# In[10]:


def data_clean_3(x):
    
    data = x.copy()

    columns_to_remove = ['User Available Storage','SIM Size','Chipset','Processor','Autofocus','Aspect Ratio','Touch Screen',
                        'Bezel-less display','Operating System','SIM 1','USB Connectivity','Other Sensors','Graphics','FM Radio',
                        'NFC','Shooting Modes','Browser','Display Colour' ]

    columns_to_retain = list(set(data.columns)-set(columns_to_remove))
    data = data[columns_to_retain]


    columns_to_remove = [ 'Screen Resolution','User Replaceable','Camera Features',
                        'Thickness', 'Display Type']

    columns_to_retain = list(set(data.columns)-set(columns_to_remove))
    data = data[columns_to_retain]


    columns_to_remove = ['Fingerprint Sensor', 'Flash', 'Rating Count', 'Review Count','Image Resolution','Type','Expandable Memory',                        'Colours','Width','Model']
    columns_to_retain = list(set(data.columns)-set(columns_to_remove))
    data = data[columns_to_retain]

    return data


# In[11]:


train = data_clean_3(train)
test = data_clean_3(test)

# check the number of features and data points in train
print("Number of data points in train: %d" % train.shape[0])
print("Number of features in train: %d" % train.shape[1])

# check the number of features and data points in test
print("Number of data points in test: %d" % test.shape[0])
print("Number of features in test: %d" % test.shape[1])


# In[12]:


# one hot encoding

train_ids = train['PhoneId']
test_ids = test['PhoneId']

cols = list(test.columns)
cols.remove('PhoneId')
cols.insert(0, 'PhoneId')

combined = pd.concat([train.drop('Rating', axis=1)[cols], test[cols]])
print(combined.shape)
print(combined.columns)
#combined = combined.drop(['Brand'],axis=1)
combined = pd.get_dummies(combined)
print(combined.shape)
print(combined.columns)

train_new = combined[combined['PhoneId'].isin(train_ids)]
test_new = combined[combined['PhoneId'].isin(test_ids)]


# In[13]:


train_new = train_new.merge(train[['PhoneId', 'Rating']], on='PhoneId')


# In[14]:


# check the number of features and data points in train
print("Number of data points in train: %d" % train_new.shape[0])
print("Number of features in train: %d" % train_new.shape[1])

# check the number of features and data points in test
print("Number of data points in test: %d" % test_new.shape[0])
print("Number of features in test: %d" % test_new.shape[1])


# In[15]:


train_new.head()


# In[16]:


test_new.head()


# In[17]:


class Perceptron:
    def __init__ (self):
        self.w = None
        self.b = None
        self.device = None
        self.random_inits = {'normal':np.random.normal,'uniform':np.random.uniform}
        
    def model(self, x):
        dot_product = np.dot(self.w, x)
        return 1 if (dot_product >= self.b) else 0
    
    def predict(self, X):
        Y = []
        for x in X:
            result = self.model(x)
            Y.append(result)
        return np.array(Y)
    
    def fit(self, X, Y, epochs = 1, lr = 1,seeds=(1,1),init='normal',random_inits=True):
        if X.shape[0] != Y.shape[0]:
            print('X and Y have different shapes!',X.shape[0],'!=',Y.shape[0])
            return
        if random_inits:
            np.random.seed(seeds[0])
            self.w = self.random_inits[init](size=X.shape[1])
            np.random.seed(seeds[1])
            self.b = self.random_inits[init]()
        else:
            self.w = np.ones(X.shape[1])
            self.b = 0
        
        accuracy = {}
        max_accuracy = 0
        wt_matrix = []
        
        for i in range(epochs):
            for j in range(X.shape[0]):
                x,y = X[j],Y[j]
                y_pred = self.model(x)
                if y == 1 and y_pred == 0:
                    self.w = self.w + lr * x
                    self.b = self.b - lr * 1
                elif y == 0 and y_pred == 1:
                    self.w = self.w - lr * x
                    self.b = self.b + lr * 1
                    
            accuracy[i] = accuracy_score(self.predict(X), Y)
            
            if (accuracy[i] > max_accuracy):
                max_accuracy = accuracy[i]
                chkptw = self.w
                chkptb = self.b
        
        self.w = chkptw
        self.b = chkptb
        
        print(max_accuracy)
    
        plt.plot(accuracy.values())
        plt.ylim([0, 1])
        plt.show()
    
        return max_accuracy


# In[18]:


class Perceptron_loss:
    def __init__ (self):
        self.w = None
        self.b = None
        self.device = None
        self.random_inits = {'normal':np.random.normal,'uniform':np.random.uniform}
        self.loss_function = [mean_squared_error,log_loss][0]
    def model(self, x):
        dot_product = np.dot(self.w, x)
        return 1 if (dot_product >= self.b) else 0
    
    def predict(self, X):
        Y = []
        for x in X:
            result = self.model(x)
            Y.append(result)
        return np.array(Y)
    
    def fit(self, X, Y, epochs = 1, lr = 1,seeds=(1,1),init='normal',random_inits=True):
        if X.shape[0] != Y.shape[0]:
            print('X and Y have different shapes!',X.shape[0],'!=',Y.shape[0])
            return
        if random_inits:
            np.random.seed(seeds[0])
            self.w = self.random_inits[init](size=X.shape[1])
            np.random.seed(seeds[1])
            self.b = self.random_inits[init]()
        else:
            self.w = np.ones(X.shape[1])
            self.b = 0
        
        accuracy = {}
        max_accuracy = 0
        wt_matrix = []
        loss = 1
        for i in range(epochs):
            for j in range(X.shape[0]):
                x,y = X[j],Y[j]
                y_pred = self.model(x)
                if y == 1 and y_pred == 0:
                    self.w = self.w + lr *loss* x
                    self.b = self.b - lr * 1
                elif y == 0 and y_pred == 1:
                    self.w = self.w - lr *loss* x
                    self.b = self.b + lr * 1
            pred = self.predict(X)
            accuracy[i] = accuracy_score(pred, Y)
            loss = self.loss_function(pred,Y)
            loss = -loss if  loss < 0 else loss
            
            if (accuracy[i] > max_accuracy):
                max_accuracy = accuracy[i]
                chkptw = self.w
                chkptb = self.b
        
        self.w = chkptw
        self.b = chkptb
        
        print(max_accuracy)
    
        plt.plot(accuracy.values())
        plt.ylim([0, 1])
        plt.show()
    
        return max_accuracy


# In[19]:


import torch
class Perceptron_cuda:
    def __init__ (self):
        self.w = None
        self.b = None
        self.device = None
        self.mt = 0
        self.random_inits = {'normal':np.random.normal,'uniform':np.random.uniform}
        
    def model(self, x):
        return torch.mm(x,self.w) >= self.b
    
    def predict(self, X):
        return self.model(X).cpu().numpy()
    
    def fit(self, X, Y, epochs = 1, lr = 1,seeds=(1,1),init='normal',random_inits=True):
        if X.shape[0] != Y.shape[0]:
            print('X and Y have different shapes!',X.shape[0],'!=',Y.shape[0])
            return
        if random_inits:
            np.random.seed(seeds[0])
            self.w = self.random_inits[init](size=X.shape[1])
            np.random.seed(seeds[1])
            self.b = self.random_inits[init]()
        else:
            self.w = np.ones(X.shape[1])
            self.b = 0
        
        accuracy = {}
        max_accuracy = 0
        wt_matrix = []
        lrc = lr
        zero,one = 0,1
        m1 = -1
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            self.w = torch.tensor(self.w,device=self.device).view(-1,1)
            self.b = torch.tensor(self.b,device=self.device,dtype=torch.double)
            X = torch.tensor(X,device=self.device)
            Y = torch.tensor(Y,device=self.device)
            lrc = torch.tensor(lrc,device=self.device,dtype=torch.double)
            zero = torch.tensor(0,device=self.device,dtype=torch.uint8)
            one = torch.tensor(1,device=self.device,dtype=torch.uint8)
            m1 = torch.tensor(-1,device=self.device,dtype=torch.uint8)
        for i in range(epochs):
            for j in range(X.shape[0]):
                x= X[j].view(-1,1)
                y = Y[j]
                y_pred = self.model(x.view(1,-1))
                if torch.sub(y,y_pred) == one:
                    self.w = torch.add(self.w, torch.mul(lrc, x))
                    self.b = torch.sub(self.b ,lrc)
                elif torch.sub(y,y_pred) == m1:
                    self.w = torch.sub(self.w, torch.mul(lrc, x))
                    self.b = torch.add(self.b ,lrc)
            
            accuracy[i] = accuracy_score(self.predict(X), Y.cpu().numpy())
            if (accuracy[i] > max_accuracy):
                max_accuracy = accuracy[i]
                chkptw = self.w
                chkptb = self.b
        
        self.w = chkptw
        self.b = chkptb
        
        print(max_accuracy)
    
        plt.plot(accuracy.values())
        plt.ylim([0, 1])
        plt.show()
    
        return max_accuracy


# In[20]:


perceptron = [Perceptron,Perceptron_cuda,Perceptron_loss][-1]()


# In[21]:


def data_scale(data,scaler_class,cols_to_scale,drop_cols,scale_all=False,idcol='PhoneId',data_train_scaler=None):
    scaler = scaler_class() if not data_train_scaler else data_train_scaler
    if scale_all:
        scaled = data.drop(drop_cols,axis=1)
        cols = scaled.columns
        if not data_train_scaler:
            scaler.fit(scaled)
        scaled[cols] = scaler.transform(scaled)
        data = scaled
    else:
        scaled,notscaled = data[cols_to_scale],data.drop(cols_to_scale,axis=1)
        if not data_train_scaler:
            scaler.fit(scaled)
        scaled[cols_to_scale] = scaler.transform(scaled)
        scaled[idcol] = data[idcol]
        data = scaled.merge(notscaled,on=idcol)
        data = data.drop(drop_cols,axis=1)
    return data,scaler


# In[22]:


scalers = [MinMaxScaler,StandardScaler]
test_ids = test_new[['PhoneId']]
scaler_class = scalers[1]
cols_to_scale = ['RAM','Internal Memory','Screen to Body Ratio (calculated)', 'Weight','Processor_frequency','Height', 'Capacity', 'Pixel Density', 'Screen Size', 'Resolution']
train_drop = ['PhoneId','Rating']
test_drop = ['PhoneId']
scale_all = False

x_train,train_scaler = data_scale(train_new,scaler_class,cols_to_scale,train_drop,scale_all)
x_test,test_scaler = data_scale(test_new,scaler_class,cols_to_scale,test_drop,scale_all,data_train_scaler=train_scaler)

y_train = np.array([ 1 if v>=THRESHOLD else 0 for v in train_new[['Rating']].values])
cols = x_train.columns
seeds = (1,1)


# In[23]:


def train(ep_lr):
    ep,lr = ep_lr
    print(ep,lr)
    return [ep,lr,pc.fit(x_train.values, y_train, ep,lr,seeds=seeds)]

def filtered(lst,func,index):
    maxval = func(lst[:,index])
    return np.array(list(filter(lambda v:v[index]==maxval,lst)))


# In[24]:


# parameters = list(ParameterGrid({'epochs':[1000,2000,5000,10000],'lr':[0.0001,0.001,0.01,0.1,1,0.2,0.02,0.3.0.03]}))
# parameters = list(ParameterGrid({'epochs':[100,1000,10000],'lr':[0.001,0.001,0.01,0.1,0.2,0.02,0.3,0.03]}))
# res = [train(tuple(k.values())) for k in parameters]


# In[25]:


# epi,lri,mai = 0,1,2 #indices
# best_params = np.array(res)
# best_params = filtered(best_params,max,mai)
# best_params = filtered(best_params,min,epi)
# #best_params = filtered(best_params,min,lri)
# best_params = best_params[0]
# print('Best hyperparameters found so far',best_params)


# In[26]:


#epochs,lr = int(best_params[epi]),best_params[lri]
epochs,lr,seeds = 1000,0.01,(0,0)
#epochs,lr,seeds = 100000,0.0001,(0,0)
print(epochs,lr)
max_accuracy = perceptron.fit(x_train.values, y_train, epochs, lr,seeds=seeds)


# In[27]:


# import time
# t1 = time.time()
# max_accuracy = pc.fit(x_train, y_train, 1000, 0.01,seeds=(2,4))
# print(time.time()-t1)


# In[28]:


plt.plot(perceptron.w)
plt.show()
weights = {}
for i in range(len(perceptron.w)):
    weights[cols[i]]=perceptron.w[i]
#sorted_by_value = {}
for c in list(sorted(weights, key=weights.get, reverse=True)):
    #sorted_by_value[c] = weights[c]
    print(c,weights[c])


# In[29]:


results = perceptron.predict(x_test.values)


# In[30]:


submission = pd.DataFrame({'PhoneId':test_ids['PhoneId'], 'Class':results})
submission = submission[['PhoneId', 'Class']]
submission.head()


# In[31]:


submission.to_csv("submission.csv", index=False)


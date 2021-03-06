# -*- coding: utf-8 -*-
"""
Created on Tue Jul 05 15:22:55 2016

@author: U505118
"""
import pandas as pd
from pandas import DataFrame
class randomforest:
    def rf(self,df):
        #Libraries used
        '''from sklearn import metrics
        from sklearn.ensemble import RandomForestClassifier
        import pandas as pd
        from pandas import DataFrame
        from nltk import word_tokenize
        from sklearn import preprocessing
        from sklearn.metrics import roc_auc_score
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.metrics import roc_curve, auc
        import matplotlib.pyplot as plt
        import numpy as np
        import random
        import cPickle'''
        #READING 10-K FILES
        tr=1857
        
        df = pd.read_csv('C:/Users/U505118/Desktop/FinalReview/Final.csv')
        self.df1 = pd.concat([df['Indicator'], df['Phrase']], axis=1)
        df_train = df[:tr]        
        self.df_test = df[tr:]
        
        #CLASSIFYING INTO TRAIN AND TEST DATA
        words = df_train['Phrase'].tolist()
        wt = self.df_test['Phrase'].tolist()
        
        sw_file = open('C:/Users/U505118/Desktop/FinalReview/RandomForest/stopwords.txt') 
        stopwords = sw_file.readlines()
        for i in range(0,len(stopwords)):
            stopwords[i] = stopwords[i].strip()
        sw_file.close()
        
        #CONVERTING SENTENCES TO VECTORS SO THAT THEY CAN BE INPUT IN RF AND YES,NO TO NUMBERS       
        vect = CountVectorizer(stop_words = stopwords, token_pattern = '[a-z]+', min_df=5,max_features = 400)
        idf = vect.fit_transform(words).toarray()
        number = preprocessing.LabelEncoder()
        df['Indicator'] = number.fit_transform(df.Indicator)
        
        #IMPLEMENTING RANDOM FOREST
        rf = RandomForestClassifier(n_estimators=1000,min_samples_leaf=5)
        rf.fit(idf, df['Indicator'][:tr])
        
                
        wo_test = self.df_test['Phrase'].tolist()
       
       #CONVERTING SENTENCES TO VECTORS SO THAT THEY CAN BE INPUT IN RF AND YES,NO TO NUMBERS       
        test = vect.fit_transform(wo_test).toarray()
        number = preprocessing.LabelEncoder()
        df['Indicator'] = number.fit_transform(df.Indicator)
        t = []
        self.a = 0
        self. b = 0
        self.c=0
        self.d=0
        self.co=0
        
        #PREDICTING DATA USING RF MODEL
        t = rf.predict_proba(test)
        u = []  
        u = t.tolist()    
        
        t = []
        for i in range(0,len(u)):
            if u[i][1]>0.61:
                t.append(1)
            else:
                t.append(2)
                
        #COMBINING PREDICTED VALUE AND ACTUAL VALUE       
        k = []
        for i in range(0,len(u)):
            k.append(u[i][2])
        self.df1 = pd.DataFrame({'true':df['Indicator'][tr:],'model':t,'prob':k})
        
        #CONFUSION MATRIX
        df2 = pd.DataFrame(index = {'Model +ve','Model -ve'},columns = {'Target +ve','Target -ve'})
        for i in range(tr,2674):
            if self.df1['true'][i] == self.df1['model'][i]:
                self.co = self.co+1 
            if self.df1['model'][i] == 2 and self.df1['true'][i] == 2:
                self.a = self.a+1
            elif self.df1['model'][i] == 2 and self.df1['true'][i] == 1:
                self.b = self.b+1
            elif self.df1['model'][i] == 1 and self.df1['true'][i] == 2:
                self.c = self.c+1
            else:
                self.d = self.d+1
        
        df2['Target +ve']['Model +ve'] = self.a
        df2['Target +ve']['Model -ve'] = self.c
        df2['Target -ve']['Model +ve'] = self.b
        df2['Target -ve']['Model -ve'] = self.d 
        self.model = self.df1['model']-1
        self.prob = self.df1['prob']
        self.model = self.model.reset_index()
        self.prob = self.prob.reset_index()
        return list(self.model.model),list(self.prob.prob)
    def met(self):
            #CALCULATING SENSITIVITY,PRECISION,SPECIFICITY,ACCURACY,FALSE POSITIVE RATE
            self.pp = float(self.a)/(self.a + self.b)
            self.np = float(self.d)/(self.c + self.d)
            self.sen = float(self.a)/(self.a + self.c)
            self.spe = float(self.d)/(self.b + self.d)
            self.acc = (self.a+self.d)/float(self.a+self.b+self.c+self.d)
            print "Sensitivity and Accuracy =" 
            return self.sen,self.acc
            
    def ROC(self):  
             #PLOTTING ROC CURVE
            self.df1 = self.df1[self.df1.true!=0]
            self.df1 = self.df1.reindex()
            self.fpr, self.tpr,self.thresholds = metrics.roc_curve(self.df1['true']-1,self.df1['prob'])
            roc_auc = auc(self.fpr, self.tpr)
            print roc_auc
            fig1 = plt.figure()
            ax1 = fig1.add_subplot(111)
            ax1.plot(self.fpr, self.tpr, 'b')
            plt.legend(shadow=True, fancybox=True,loc=1) 
            plt.ylabel('True Positive Rate')
            plt.xlabel('False Positive Rate')
            plt.title("ROC curve")
            plt.show()
                     
            #PLOTTING SENSITIVITY VS. SPECIFICITY CURVE
            fig2 = plt.figure()
            ax2 = fig2.add_subplot(111)
            ax2.plot(self.thresholds, self.tpr, 'b',label='Sensitivity')
            ax2.plot(self.thresholds,1-self.fpr,'r',label='1-Specificity')
            plt.legend(shadow=True, fancybox=True,loc=1) 
            plt.ylabel('Sensitivity and Specificity')
            plt.xlabel('Probability')
            plt.title("Sensitivity vs. Specificity curve")
            plt.show()
            
    def gain(self):
            #PLOTTING GAINS CHART
            TP = self.a
            FN = self.c
            self.df_test = self.df_test.reset_index()
            gain_model = [0]
            model_cumul = 0.0
            dec = len(self.df_test)/10
            dec1 = len(self.df_test)/10
            self.df_test = self.df_test.sample(n = len(self.df_test))
            self.df1.sort(columns = 'prob', inplace = True, ascending = False)
            self.df1 = self.df1.reset_index(drop = True)
            df_GL = pd.DataFrame([],columns  = ['Decile', 'Random', 'Model'])
            
            for i in range(10):
                df_GL.loc[i, 'Decile'] = str(i + 1)
                model = 0.0
                if (i==9):
                    dec1=len(self.df_test)%10
                for k in range(i*dec, (i*dec) + dec1):
                        if self.df1['true'][k] == 2:
                            model = model + 1
                model_cumul = model_cumul + model
                df_GL.loc[i, 'Model'] = str(model_cumul)
                gain_model.append(((model_cumul)/(TP + FN))*100.00)
            
            
            x=[0,10,20,30,40,50,70,90,100]            
            percent_pop = range(0, 110, 10)
            plt.plot(percent_pop, gain_model, 'b', label = "Model")
            plt.plot(x,x,'r',label="Random")
            plt.legend(shadow=True, fancybox=True,loc=1) 
            plt.ylabel('Cummulative Gain')
            plt.xlabel('Population Percentage')
            plt.title("Gain Chart")
            plt.show()  


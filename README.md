# Qure_covid_detection

For this Dataset we needed to find out probability of consolidation i.e. Class_label =1
We were provided 16000 samples for which true labels were provided, remaining 4000 samples were test dataset for which true labels were not provided.
In my base model i trained on 16000 data using Keras framework which achieved a maximum Accuracy of - 73.37 on train & 73.03 on validation data.

To improve performance i used transfer learning techinque & utilized pre-trained model of VGG 16.
It provided train accuracy of - > 89.7 & max validation accuracy of -> 76.4 %.

To demonstrate confidence score i used confusion matrix on validation data.
I have provided prediction class label for test image wise. Output is contained in excel sheet with same name.
I have provided confidence score i.e. probability of consolidation for train, validation & test image wise. Output is contained in excel sheet with same name.

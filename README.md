# target-opinon-extraction
This repository contains a target-opinion extraction algorithm implemented using python. The project can be ran at once but several data have to be prepared ahead of it:
* Segmented data as well as dependency parsing data
* Target and opinion seed words (will be required during running)
* All relevant library (rules is a python code we created, not a library)
Aside from this, several constant should be noticed while running this code on your own:
* This portion of the code should be altered according to the amount of data.
```
    for o in range(24341):
```
```
        else:
            flag = 0
            start = 24001
            end = 24341
```
* The filtering constant as one critical parameter, are define here:
```
for cons in [1]:#,1.5,2,2.5,3,3.5,4,4.5,5]:
```

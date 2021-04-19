# Implementation of Data Science Algorithms (Sketch and SVD)

1. **Error Graph of Count Min, Count Sketch and Misra-Gries**

    >!['Error Graph'](q4.png)

    > Here, I'm using 5 hash functiions so, m=k/5 for Count min and Count Sketch

    > From the graph we can see that for k=2000 (approx) CM and CS has very low error. 
    
    >So for m=400 and d=5 CM and CS sketch has error less than 1%. 
    
    > For Misra-Gries for k=100 the error is less than 1%. 

    > Since we are testing with ID's with top 1000 frequencies the Misra Gries seems to work better compared to other sketchs. But if we had tested with all the ID's in random, then CM and CS sketch has an edge over Misra-Gries.
    

2. **Result of Movie Rating prediction using K-Rank approximation** 

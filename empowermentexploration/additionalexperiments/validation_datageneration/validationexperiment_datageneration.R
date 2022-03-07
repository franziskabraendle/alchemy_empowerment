
library(ggplot2)
library(tidyr)
library(rjson)

rm(list=ls())

#necessary for filtering out 1000 random element combinations
gametree<-read.csv("..\\..\\..\\empowermentexploration\\data\\gametree\\20211011-1118\\tinyalchemyGametreeTable-data-crawl300.csv")
truegametree <- read.csv("..\\..\\..\\empowermentexploration\\resources\\littlealchemy\\data\\tinyalchemyCombinationTable.csv")
total_gametree <- merge(gametree, truegametree, by = c("first","second"))
print(head(total_gametree))
hist(gametree$predSuccess)

for (i in (1:10)){
  temp_df_true <- subset(total_gametree, predSuccess < (i/10) & predSuccess > ((i-1)/10) & success == 1) #get subsets of different predicted probabilities
  temp_df_false <- subset(total_gametree, predSuccess < (i/10) & predSuccess > ((i-1)/10) & success == 0)
 # print(nrow(temp_df_true))
  print(sum(temp_df_true$result == temp_df_true$predResult))
  
  #sample 50 predicted as true and 50 predicted as false of each group if 50 predicted as true exist
  if(nrow(temp_df_true) >= 50){ 
    sampled_subset_true <- temp_df_true[sample(nrow(temp_df_true), 50), ] 
    sampled_subset_false <- temp_df_false[sample(nrow(temp_df_false), 50), ]

    #if not, take more of the predicted false ones
  }else{ 
    true_rows <- nrow(temp_df_true)
    sampled_subset_true <- temp_df_true
    sampled_subset_false <- temp_df_false[sample(nrow(temp_df_false), 100-true_rows), ]
  }

  sampled_subset <- rbind(sampled_subset_true, sampled_subset_false)
  if(i == 1){
    sampled_df <- sampled_subset
  }else{
    sampled_df <- rbind(sampled_df, sampled_subset)
  }
}
 
hist(sampled_df$success)
# write.csv(sampled_df, "predSuccess_balanced.csv", row.names = FALSE)


#filtering out which 4 elements are used
combination_selection<-read.csv("predSuccess_balanced.csv")
print(head(combination_selection))
#exploring the data
gathered_probs <- gather(combination_selection, element, value, X0:X539)
hist(gathered_probs$value, ylim=c(0,100))
hist(gathered_probs$value, ylim=c(0,1000))

combination_selection$predBinSuccess <- ifelse(combination_selection$predSuccess >0.5, 1 ,0)

df_finalvalues <- data.frame(matrix(ncol=14, nrow=0))
names <- c("first","second","predSuccess","predBinSuccess","E1","E2","E3","E4","Prob_E1","Prob_E2","Prob_E3","Prob_E4", "success", "result")
colnames(df_finalvalues) <- names

for(j in 1:1000){ #1000

  currentrow<-gather(combination_selection[j,],element, value, X0:X539)
  currentrow<-currentrow[order(-currentrow$value),]
  
  #get result element and three additional ones which are distributed over the predicted probabilities
  currentfourvalues<-head(currentrow,1)
  firstslice <- currentrow[2:30,]
  secondslice <- currentrow[31:150,]
  thirdslice <- currentrow[151:540,]
  row2 <- firstslice[sample(nrow(firstslice),1),]
  row3 <- secondslice[sample(nrow(secondslice),1),]
  row4 <- thirdslice[sample(nrow(thirdslice),1),]
  currentfourvalues <- rbind(currentfourvalues, row2, row3, row4)



  currentfourvalues$element <- as.numeric(sub('.', '', currentfourvalues$element))

  df_tempvalues <- data.frame(matrix(ncol=14, nrow=1))
  names <- c("first","second","predSuccess","predBinSuccess","E1","E2","E3","E4","Prob_E1","Prob_E2","Prob_E3","Prob_E4", "success", "result")
  colnames(df_tempvalues) <- names
  
  df_tempvalues$first <- currentfourvalues$first[1]
  df_tempvalues$second <- currentfourvalues$second[1]
  df_tempvalues$predSuccess <- currentfourvalues$predSuccess[1]
  df_tempvalues$predBinSuccess <- currentfourvalues$predBinSuccess[1]
  df_tempvalues$success <- currentfourvalues$success[1]
  df_tempvalues$result <- currentfourvalues$result[1]

  df_tempvalues$E1 <- currentfourvalues$element[1]
  df_tempvalues$E2 <- currentfourvalues$element[2]
  df_tempvalues$E3 <- currentfourvalues$element[3]
  df_tempvalues$E4 <- currentfourvalues$element[4]
  df_tempvalues$Prob_E1 <- currentfourvalues$value[1]
  df_tempvalues$Prob_E2 <- currentfourvalues$value[2]
  df_tempvalues$Prob_E3 <- currentfourvalues$value[3]
  df_tempvalues$Prob_E4 <- currentfourvalues$value[4]

  df_finalvalues <- rbind(df_finalvalues, df_tempvalues)

}

#explore again

gathered_selection_1 <- gather(df_finalvalues, element, value, E1:E4)
print(hist(gathered_selection_1$value, breaks = 1000))
print(hist(df_finalvalues$E1, breaks = 1000))
print(hist(df_finalvalues$E2, breaks = 1000))
print(hist(df_finalvalues$E3, breaks = 1000))
print(hist(df_finalvalues$E4, breaks = 1000))

gathered_selection_2 <- gather(df_finalvalues, element, value, Prob_E1:Prob_E4)
hist(log10(gathered_selection_2$value))
hist(df_finalvalues$Prob_E1)
hist(df_finalvalues$Prob_E2)
hist(df_finalvalues$Prob_E3)
hist(df_finalvalues$Prob_E4)

which(df_finalvalues$first == df_finalvalues$E1)

for (k in (1:10)){
  tempsubset <- subset(df_finalvalues, predSuccess < (k/10) & predSuccess > ((k-1)/10) & E1==result)
  print(nrow(tempsubset))
}

# get strings

translation <- fromJSON(file = "..\\..\\..\\empowermentexploration\\resources\\littlealchemy\\data\\tinyalchemyElements.json")

df_finalvalues$first_string = translation[(df_finalvalues$first)+1]
df_finalvalues$second_string = translation[(df_finalvalues$second+1)]
df_finalvalues$E1_string = translation[(df_finalvalues$E1+1)]
df_finalvalues$E2_string = translation[(df_finalvalues$E2+1)]
df_finalvalues$E3_string = translation[(df_finalvalues$E3+1)]
df_finalvalues$E4_string = translation[(df_finalvalues$E4+1)]

#combined_df <- merge(df_finalvalues, truegametree, by = c("first","second")) #gametree only includes one way of combinations (first smaller), but df_finalvalues is already sorted that way, so it works.

translation_altered <- c("None", translation)
df_finalvalues$result_string = translation_altered[(df_finalvalues$result+2)]

#print(min(df_finalvalues$first))

write.csv(df_finalvalues, "prediction_selection.csv", row.names = FALSE)

#as json for experiment (also emp file)
jsonfile = toJSON(df_finalvalues)
write(jsonfile, "prediction_selection.json")
elementempowerment<-read.csv("..\\..\\..\\empowermentexploration\\data\\gametree\\element_empowerment\\tinyalchemy_element_empowerment_dataframe.csv")
write.csv(elementempowerment, "element_empowerment.csv", row.names = FALSE)

jsonfile2 = toJSON(elementempowerment)
write(jsonfile2, "element_empowerment.json")

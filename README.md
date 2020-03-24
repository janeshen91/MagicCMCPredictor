# MagicCMCPredictor
---
title: "Magic Cards Predictor"
author: "Jane Shen, Lake Watkins"
date: "March 24, 2020"
output: html_document
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```

## Magic the Gathering

Magic is a strategic card game. Each card costs a certain amount of mana to cost, and you can do stuff with the card to try to decrease your opponent's life to 0 (or achieve other winning coniditions). Jane has been more or less forced to play, and to her surprise even likes it a little. Here is a data analysis that she and Lake has agreed to do together as a way to level up data analysis skills, pass time during this Covid-19 crisis and perhaps even bond in a nerdy way. Also Lake thinks he'll be able to make use of it in his own card game, make lots of money and then Jane and Lake can retire to a cabin in the woods.

Overall question: 
1. how to price cards in terms of mana cost?  

2. Can we predict which cards are the most successful in different formats?  

3. What is the distribution of cards like in terms of successful (used a lot in a winning deck in a certain format like standard) vs not successful?  

4. Which evergreen keywords are like the most important in terms of success?  

5. How should we count things like cards that cost 4 greens to cast? Should we count it as having extra cost because you're forcing the player to stick to one color? If so, how much extra should it count for?


###Step 1 is to do some exploratory data analysis. 
We took the json file from scryfall, read it using the rjson library, and then Jane wrote a janky loop to convert it from a list to a data frame. It's not amazingly fast but it works. I'll skip running that part of the code and just load in the saved data.frame. Also side note, I tried to be like more up with the times and use tidyverse but I couldn't convert it to a tibble easily, so...old fashioned data.frame it is. Maybe I'll go back and do it the tidyverse way later...

```{r}
# library("rjson")
# 
# # Give the input file name to the function.
# default <- fromJSON(file = "C:/Users/Jane/source/repos/MagicCMCPredictor/data/scryfall-default-cards.json")
# 
# #names of columns we want
# namesOfFilteredInitial<-c("mana_cost","cmc","name","released_at","type_line","oracle_text","colors",
#             "color_identity","reserved","rarity","set_name","set_type","set","reprint","story_spotlight",
#             "power","toughness")
# 
# filtered2Face<-NULL
# filtered2DF<-NULL
# j<-1
# 
# for(i in 1:46923){
#   filtered2<-default[[i]][filtered]
#   namesOfFiltered2<-names(filtered2)
#   if (sum(namesOfFiltered2 %in% namesOfFilteredInitial)==17){
#     filtered2DF<-rbind(filtered2DF,data.frame(t(filtered2)))
#   }
# }

#save(filtered2DF,file="filtered2DFwithPowerToughness.RData")


```

## Exploratory Data analysis on creatures only

Creatures have power and toughness. I wanted to first just look at how converted mana cost (cmc) compared to the power and toughness of creatures

```{r , warning = FALSE}
library(ggplot2)

load("filtered2DFwithPowerToughness.RData")

#basically filtered2DF is the dataframe with the columns we filtered out. I then filtered out only the rows with numerical power and toughness

filtered2DF$powerNum<-as.numeric(filtered2DF$power)
filtered2DF$toughnessNum<-as.numeric(filtered2DF$toughness)

filtered2DFpowerNA<-filtered2DF[!is.na(filtered2DF$power),]
filtered2DFpowerNA2<-filtered2DFpowerNA[!is.na(filtered2DFpowerNA$powerNum),]
filtered2DFpowerNA3<-filtered2DFpowerNA2[!is.na(filtered2DFpowerNA2$toughnessNum),]
dim(filtered2DFpowerNA3)
#ie 21179 cards with power, toughness and cmc

ggplot(filtered2DFpowerNA3,aes(x=as.numeric(cmc),y=powerNum))+geom_point()
ggplot(filtered2DFpowerNA3,aes(x=as.numeric(cmc),y=as.numeric(toughness)))+geom_point()

filtered2DFpowerNA3$powerAndTough<-filtered2DFpowerNA3$powerNum+filtered2DFpowerNA3$toughnessNum

ggplot(filtered2DFpowerNA3,aes(x=as.numeric(cmc),y=powerAndTough))+geom_point()

```
##Some initial observations
Why are there cards that cost 0 but has power and toughness close to 25?

There is one obvious outlier on the other end: for a cmc of 15, you can get a creature with power and tougness of 99? Makes these other 2 cards that costs 15 but only gives you power and toughness around 12.5 seem too weak. 
```{r}
index25<-filtered2DFpowerNA2$powerNum>25
filtered2DFpowerNA2[index25,]       

    

`````

So the cost 15, power and tougness 99 creature is called Big Furry Monster, apparently this is like a joke card.  
The mana cost 0 but power and toughness >10 cards are the X's. so I guess another thing we can ignore

###Linear regression
```{r}
#taking out Big Furry Monster and the cmc==0
index0<-filtered2DFpowerNA3$cmc==0
index25<-filtered2DFpowerNA3$powerNum>25
indexToken<-filtered2DFpowerNA3$set_type=="token"
sum(indexToken)
filtered0<-filtered2DFpowerNA3[!indexToken,]  
indexFunny<-filtered0$set_type=="funny"
sum(indexFunny)
filtered0Un<-filtered0[!indexFunny,]  

index40<-filtered0Un$powerAndTough==40
filtered0Un2<-filtered0Un[!index40,]
lm(filtered0Un2$powerAndTough ~ as.numeric(filtered0Un2$cmc))

ggplot(filtered0Un2,aes(x=as.numeric(cmc),y=powerAndTough))+geom_point()+ geom_smooth(method='lm')

````

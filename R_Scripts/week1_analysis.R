.libPaths(c(
  "C:/Users/Sahil/AppData/Local/R/win-library/4.6",
  .libPaths()
))

library(dplyr)
library(ggplot2)
library(tidyr)
library(readr)

cat("\n===== TITANIC DATA ANALYSIS =====\n")

titanic <- read_csv(
  "Dataset/titanic_train.csv",
  show_col_types = FALSE
)

cat("\n===== DATASET DIMENSIONS =====\n")
print(dim(titanic))

cat("\n===== FIRST SIX RECORDS =====\n")
print(head(titanic))

cat("\n===== DATA STRUCTURE =====\n")
str(titanic)

cat("\n===== SUMMARY STATISTICS =====\n")
print(summary(titanic))

cat("\n===== MISSING VALUES =====\n")
print(colSums(is.na(titanic)))

cat("\n===== COLUMN NAMES =====\n")
print(names(titanic))

cat("\n===== DATASET IMPORT SUCCESSFUL =====\n")
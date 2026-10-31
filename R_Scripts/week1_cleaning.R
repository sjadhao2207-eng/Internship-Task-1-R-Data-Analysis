# ==========================================
# R DATA ANALYST INTERNSHIP
# WEEK 1 - DATA CLEANING
# Dataset: Titanic
# ==========================================

.libPaths(c(
  "C:/Users/Sahil/AppData/Local/R/win-library/4.6",
  .libPaths()
))

library(dplyr)
library(ggplot2)
library(tidyr)
library(readr)

# Project directories
dir.create("Outputs/Graphs", recursive=TRUE, showWarnings=FALSE)
dir.create("Outputs/Results", recursive=TRUE, showWarnings=FALSE)

# Import original dataset
titanic <- read_csv(
  "Dataset/titanic_train.csv",
  show_col_types=FALSE
)

cat("\n===== 1. DUPLICATE CHECK =====\n")

duplicate_rows <- sum(duplicated(titanic))
duplicate_ids <- sum(duplicated(titanic$PassengerId))

cat("Duplicate rows:", duplicate_rows, "\n")
cat("Duplicate Passenger IDs:", duplicate_ids, "\n")

# Create a working copy
clean_data <- titanic

cat("\n===== 2. MISSING VALUE TREATMENT =====\n")

# Age: median based on Pclass and Sex
age_medians <- clean_data %>%
  group_by(Pclass, Sex) %>%
  summarise(
    group_median_age = median(Age, na.rm=TRUE),
    .groups="drop"
  )

clean_data <- clean_data %>%
  left_join(age_medians, by=c("Pclass", "Sex")) %>%
  mutate(
    Age = ifelse(
      is.na(Age),
      group_median_age,
      Age
    )
  ) %>%
  select(-group_median_age)

# Fallback for any remaining missing Age
clean_data$Age[is.na(clean_data$Age)] <-
  median(titanic$Age, na.rm=TRUE)

# Embarked: fill using mode
get_mode <- function(x) {
  values <- na.omit(x)
  names(which.max(table(values)))
}

embarked_mode <- get_mode(clean_data$Embarked)

clean_data$Embarked[
  is.na(clean_data$Embarked)
] <- embarked_mode

# Cabin: remove due to high missing percentage
clean_data <- clean_data %>%
  select(-Cabin)

cat("Age missing values:", sum(is.na(clean_data$Age)), "\n")
cat("Embarked missing values:", sum(is.na(clean_data$Embarked)), "\n")
cat("Cabin column removed due to high missingness.\n")

cat("\n===== 3. OUTLIER DETECTION =====\n")

# IQR method for Fare
Q1 <- quantile(clean_data$Fare, 0.25, na.rm=TRUE)
Q3 <- quantile(clean_data$Fare, 0.75, na.rm=TRUE)

IQR_value <- IQR(clean_data$Fare, na.rm=TRUE)

lower_limit <- Q1 - 1.5 * IQR_value
upper_limit <- Q3 + 1.5 * IQR_value

fare_outliers <- clean_data %>%
  filter(Fare < lower_limit | Fare > upper_limit)

cat("Lower limit:", lower_limit, "\n")
cat("Upper limit:", upper_limit, "\n")
cat("Fare outliers detected:", nrow(fare_outliers), "\n")

# Save outlier records separately
write_csv(
  fare_outliers,
  "Outputs/Results/fare_outliers.csv"
)

# Flag outliers without deleting them
clean_data <- clean_data %>%
  mutate(
    Fare_Outlier = Fare < lower_limit |
                   Fare > upper_limit
  )

# Fare boxplot
p1 <- ggplot(clean_data, aes(y=Fare)) +
  geom_boxplot(fill="steelblue") +
  labs(
    title="Fare Outlier Detection",
    y="Passenger Fare"
  ) +
  theme_minimal()

ggsave(
  "Outputs/Graphs/fare_boxplot.png",
  p1,
  width=8,
  height=5
)

cat("\n===== 4. NORMALIZATION =====\n")

# Min-Max normalization
min_max <- function(x) {
  if (diff(range(x, na.rm=TRUE)) == 0) {
    return(rep(0, length(x)))
  }

  (x - min(x, na.rm=TRUE)) /
    (max(x, na.rm=TRUE) - min(x, na.rm=TRUE))
}

clean_data <- clean_data %>%
  mutate(
    Age_Normalized = min_max(Age),
    Fare_Normalized = min_max(Fare)
  )

cat("Age normalization completed.\n")
cat("Fare normalization completed.\n")

cat("\n===== 5. CATEGORICAL ENCODING =====\n")

clean_data <- clean_data %>%
  mutate(
    Sex = factor(Sex),
    Pclass = factor(Pclass),
    Embarked = factor(Embarked)
  )

# One-hot encoding
encoded_matrix <- model.matrix(
  ~ Sex + Pclass + Embarked - 1,
  data=clean_data
)

encoded_data <- data.frame(
  PassengerId=clean_data$PassengerId,
  encoded_matrix
)

write_csv(
  encoded_data,
  "Outputs/Results/titanic_encoded.csv"
)

cat("Categorical encoding completed.\n")

cat("\n===== 6. FINAL DATA VALIDATION =====\n")

cat("Final dimensions:\n")
print(dim(clean_data))

cat("\nRemaining missing values:\n")
print(colSums(is.na(clean_data)))

cat("\nFinal summary:\n")
print(summary(clean_data))

# Save cleaned dataset
write_csv(
  clean_data,
  "Outputs/Results/titanic_cleaned.csv"
)

# Save missing value comparison
missing_comparison <- data.frame(
  Variable=names(titanic),
  Before=colSums(is.na(titanic))
)

missing_comparison <- missing_comparison %>%
  mutate(
    After=ifelse(
      Variable %in% c("Age", "Embarked"),
      0,
      ifelse(Variable == "Cabin", NA, Before)
    )
  )

write_csv(
  missing_comparison,
  "Outputs/Results/missing_value_comparison.csv"
)

# Missing value visualization
missing_plot_data <- data.frame(
  Variable=names(titanic),
  Missing=colSums(is.na(titanic))
) %>%
  filter(Missing > 0)

p2 <- ggplot(
  missing_plot_data,
  aes(x=reorder(Variable, Missing), y=Missing)
) +
  geom_col(fill="steelblue") +
  coord_flip() +
  labs(
    title="Missing Values in Original Titanic Dataset",
    x="Variables",
    y="Number of Missing Values"
  ) +
  theme_minimal()

ggsave(
  "Outputs/Graphs/missing_values.png",
  p2,
  width=8,
  height=5
)

cat("\n===== DATA CLEANING COMPLETED =====\n")
cat("Cleaned dataset saved successfully.\n")
cat("Graphs saved successfully.\n")
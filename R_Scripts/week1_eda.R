.libPaths(c(
  "C:/Users/Sahil/AppData/Local/R/win-library/4.6",
  .libPaths()
))

library(dplyr)
library(ggplot2)
library(readr)
library(corrplot)

dir.create("Outputs/Graphs", recursive=TRUE, showWarnings=FALSE)
dir.create("Outputs/Results", recursive=TRUE, showWarnings=FALSE)

data <- read_csv(
  "Outputs/Results/titanic_cleaned.csv",
  show_col_types=FALSE
)

# Prepare categorical variables
data <- data %>%
  mutate(
    Survived = as.numeric(Survived),
    Pclass = factor(Pclass),
    Sex = factor(Sex),
    Embarked = factor(Embarked)
  )

cat("\n===== 1. SURVIVAL DISTRIBUTION =====\n")

survival_summary <- data %>%
  count(Survived) %>%
  mutate(
    Status = ifelse(Survived == 1, "Survived", "Did not survive"),
    Percentage = round(n / sum(n) * 100, 2)
  )

print(survival_summary)

write_csv(
  survival_summary,
  "Outputs/Results/survival_summary.csv"
)

p1 <- ggplot(survival_summary, aes(x=Status, y=n, fill=Status)) +
  geom_col(width=0.6) +
  geom_text(aes(label=n), vjust=-0.5) +
  labs(
    title="Titanic Passenger Survival Distribution",
    x="Survival Status",
    y="Number of Passengers"
  ) +
  theme_minimal() +
  theme(legend.position="none")

ggsave(
  "Outputs/Graphs/survival_distribution.png",
  p1, width=8, height=5
)

cat("\n===== 2. SURVIVAL BY GENDER =====\n")

gender_summary <- data %>%
  group_by(Sex) %>%
  summarise(
    Total = n(),
    Survivors = sum(Survived == 1),
    Survival_Percentage = round(mean(Survived) * 100, 2),
    .groups="drop"
  )

print(gender_summary)

write_csv(
  gender_summary,
  "Outputs/Results/gender_survival.csv"
)

p2 <- ggplot(data, aes(x=Sex, fill=factor(Survived))) +
  geom_bar(position="dodge") +
  labs(
    title="Survival by Gender",
    x="Gender",
    y="Number of Passengers",
    fill="Survived (0=No, 1=Yes)"
  ) +
  theme_minimal()

ggsave(
  "Outputs/Graphs/survival_by_gender.png",
  p2, width=8, height=5
)

cat("\n===== 3. SURVIVAL BY PASSENGER CLASS =====\n")

class_summary <- data %>%
  group_by(Pclass) %>%
  summarise(
    Total = n(),
    Survivors = sum(Survived == 1),
    Survival_Percentage = round(mean(Survived) * 100, 2),
    .groups="drop"
  )

print(class_summary)

write_csv(
  class_summary,
  "Outputs/Results/class_survival.csv"
)

p3 <- ggplot(data, aes(x=Pclass, fill=factor(Survived))) +
  geom_bar(position="dodge") +
  labs(
    title="Survival by Passenger Class",
    x="Passenger Class",
    y="Number of Passengers",
    fill="Survived (0=No, 1=Yes)"
  ) +
  theme_minimal()

ggsave(
  "Outputs/Graphs/survival_by_class.png",
  p3, width=8, height=5
)

cat("\n===== 4. AGE DISTRIBUTION =====\n")

age_summary <- data %>%
  summarise(
    Mean_Age = mean(Age),
    Median_Age = median(Age),
    Minimum_Age = min(Age),
    Maximum_Age = max(Age),
    Standard_Deviation = sd(Age)
  )

print(age_summary)

write_csv(
  age_summary,
  "Outputs/Results/age_summary.csv"
)

p4 <- ggplot(data, aes(x=Age)) +
  geom_histogram(
    bins=30,
    fill="steelblue",
    color="white"
  ) +
  labs(
    title="Distribution of Passenger Ages",
    x="Age",
    y="Number of Passengers"
  ) +
  theme_minimal()

ggsave(
  "Outputs/Graphs/age_distribution.png",
  p4, width=8, height=5
)

cat("\n===== 5. FARE DISTRIBUTION =====\n")

fare_summary <- data %>%
  summarise(
    Mean_Fare = mean(Fare),
    Median_Fare = median(Fare),
    Minimum_Fare = min(Fare),
    Maximum_Fare = max(Fare),
    Standard_Deviation = sd(Fare)
  )

print(fare_summary)

write_csv(
  fare_summary,
  "Outputs/Results/fare_summary.csv"
)

p5 <- ggplot(data, aes(x=Fare)) +
  geom_histogram(
    bins=30,
    fill="darkseagreen",
    color="white"
  ) +
  labs(
    title="Distribution of Passenger Fares",
    x="Fare",
    y="Number of Passengers"
  ) +
  theme_minimal()

ggsave(
  "Outputs/Graphs/fare_distribution.png",
  p5, width=8, height=5
)

cat("\n===== 6. CORRELATION ANALYSIS =====\n")

correlation_data <- data %>%
  transmute(
    Survived = Survived,
    Pclass = as.numeric(as.character(Pclass)),
    Age = Age,
    SibSp = SibSp,
    Parch = Parch,
    Fare = Fare
  )

correlation_matrix <- cor(
  correlation_data,
  use="complete.obs",
  method="pearson"
)

print(round(correlation_matrix, 3))

correlation_output <- as.data.frame(correlation_matrix)
correlation_output <- tibble::rownames_to_column(
  correlation_output,
  var="Variable"
)

write_csv(
  correlation_output,
  "Outputs/Results/correlation_matrix.csv"
)

png(
  "Outputs/Graphs/correlation_heatmap.png",
  width=1000,
  height=800
)

corrplot(
  correlation_matrix,
  method="color",
  type="upper",
  addCoef.col="black",
  tl.col="black",
  tl.srt=45,
  number.cex=0.7,
  title="Titanic Dataset Correlation Matrix",
  mar=c(0,0,2,0)
)

dev.off()

cat("\n===== EDA COMPLETED SUCCESSFULLY =====\n")
cat("All EDA graphs and result files have been saved.\n")
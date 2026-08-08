## Menghasilkan grafik studi kasus Pertemuan 7 dari dataset Big Five (data/data.csv)
## Reverse-scoring mengikuti kunci skor standar IPIP-50 Big Five Markers (Goldberg, 1992)
## Dijalankan dari root repo literasi-data/

library(readr)
library(dplyr)
library(ggplot2)

d <- read_tsv("data/data.csv", show_col_types = FALSE)

# Item Extraversion yang dibalik skornya (reverse-scored): E2, E4, E6, E8, E10
d <- d %>%
  mutate(
    E2_r  = 6 - E2,
    E4_r  = 6 - E4,
    E6_r  = 6 - E6,
    E8_r  = 6 - E8,
    E10_r = 6 - E10
  )

# Bersihkan: gender valid (1=Laki-laki, 2=Perempuan), usia wajar, item lengkap (tanpa 0/missing)
item_cols <- c("E1", "E2_r", "E3", "E4_r", "E5", "E6_r", "E7", "E8_r", "E9", "E10_r")
raw_item_cols <- c("E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10")

clean <- d %>%
  filter(gender %in% c(1, 2)) %>%
  filter(age >= 13, age <= 90) %>%
  filter(if_all(all_of(raw_item_cols), ~ .x %in% 1:5)) %>%
  mutate(
    skor_extraversion = rowMeans(across(all_of(item_cols))),
    gender_label = factor(gender, levels = c(1, 2), labels = c("Laki-laki", "Perempuan"))
  )

cat("N setelah dibersihkan:", nrow(clean), "\n")

ringkasan <- clean %>%
  group_by(gender_label) %>%
  summarise(
    n = n(),
    mean = mean(skor_extraversion),
    sd = sd(skor_extraversion),
    se = sd / sqrt(n),
    ci_lower = mean - qt(0.975, n - 1) * se,
    ci_upper = mean + qt(0.975, n - 1) * se,
    .groups = "drop"
  )

print(ringkasan)
write_csv(ringkasan, "slides/libs/pertemuan7_ringkasan.csv")

## ---- "SEBELUM": grafik berantakan & sumbu-y dipotong (praktik yang menyesatkan) ----

p_before <- ggplot(ringkasan, aes(x = gender_label, y = mean, fill = gender_label)) +
  geom_col(width = 0.6) +
  coord_cartesian(ylim = c(2.85, 3.10)) +  # sumbu-y dipotong -> melebih-lebihkan perbedaan
  labs(title = "Chart 1", x = "", y = "") +
  theme_gray(base_size = 20) +
  theme(
    legend.position = "right",
    panel.grid.major = element_line(linewidth = 0.8),
    panel.grid.minor = element_line(linewidth = 0.5)
  )

ggsave("slides/libs/pertemuan7_before.png", p_before, width = 7, height = 5, dpi = 150)

## ---- "SESUDAH": prinsip storytelling with data diterapkan ----

n_l <- ringkasan$n[ringkasan$gender_label == "Laki-laki"]
n_p <- ringkasan$n[ringkasan$gender_label == "Perempuan"]

p_after <- ggplot(ringkasan, aes(x = gender_label, y = mean, fill = gender_label)) +
  geom_col(width = 0.55) +
  geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper), width = 0.12, linewidth = 0.7, color = "grey30") +
  geom_text(aes(label = sprintf("%.2f", mean), y = mean + 0.14), size = 6, fontface = "bold", color = "grey20") +
  scale_fill_manual(values = c("Laki-laki" = "grey75", "Perempuan" = "#14497F")) +
  scale_y_continuous(limits = c(0, 5), breaks = 1:5) +
  labs(
    title = "Skor Extraversion perempuan sedikit lebih tinggi dari laki-laki",
    subtitle = sprintf(
      "Rentang kepercayaan 95%% tidak tumpang tindih (n sangat besar), tapi selisihnya kecil secara praktis (~0,10 poin)\nLaki-laki n = %s | Perempuan n = %s",
      format(n_l, big.mark = "."), format(n_p, big.mark = ".")
    ),
    x = NULL, y = "Skor Extraversion (rata-rata, skala 1-5)",
    caption = "Sumber: Open-Source Psychometrics Project, dataset Big Five Personality Test (openpsychometrics.org/_rawdata/)"
  ) +
  theme_minimal(base_size = 16) +
  theme(
    legend.position = "none",
    panel.grid.major.x = element_blank(),
    panel.grid.minor = element_blank(),
    plot.title = element_text(face = "bold", size = 18),
    plot.subtitle = element_text(color = "grey30", size = 12),
    plot.caption = element_text(color = "grey50", size = 9, hjust = 0),
    axis.text = element_text(size = 13),
    plot.title.position = "plot",
    plot.caption.position = "plot"
  )

ggsave("slides/libs/pertemuan7_after.png", p_after, width = 10, height = 6, dpi = 150)

cat("Selesai.\n")

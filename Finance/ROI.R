
# Get the ROIs for BTC

if(!require("pacman")) install.packages("pacman")

p_load(quantmod, PerformanceAnalytics, glue, tidymodels, dplyr, lubridate, tsibble, feasts, ggplot2)

options(warn = -1)


## Getting Crypto Prices

today = Sys.Date()
from_to<-glue("2014-01-01::{today}")

portfolio = c("BTC-USD","ETH-USD")
getSymbols(portfolio, src="yahoo", from="2014-01-01")
btc = `BTC-USD`
eth = `ETH-USD`

chartSeries(`BTC-USD`, subset=from_to,TA="addBBands();addRSI();addMACD()")


# Convert ---------------------------------------------------------------------

btc = btc %>% fortify.zoo %>% as_tibble(.name_repair = "minimal") |> rename_all(tolower) 
eth = eth %>% fortify.zoo %>% as_tibble(.name_repair = "minimal") |> rename_all(tolower)

colnames(btc) <- sub('btc.usd.', "", colnames(btc))
colnames(eth) <- sub('eth.usd.', "", colnames(eth))

btc = btc |> mutate(ticker = "btc",
              year = year(index),
              month = month(index),
              day = day(index),
              month_day = format(index, "%m%d"),
              year_month = as.yearmon(index),
              year_month = yearmonth(year_month)) |> 
  group_by(year) |> 
  mutate(roi = (close / first(close))) |> 
  ungroup()

 
eth = eth |> mutate(ticker = 'eth',
              year = year(index),
              month = month(index),
              day = day(index),
              month_day = format(index, "%m%d"),
              year_month = as.yearmon(index),
              year_month = yearmonth(year_month)) |> 
  group_by(year) |> 
  mutate(roi = (close / first(close))) |> 
  ungroup()


df = rbind(btc, eth)

# Convert tibble to tsibble
df <- as_tsibble(df, key = c(ticker), index = index)

max_roi = round(max(df$roi)) + 5

# Get all the ROI lines
df |> 
  filter(ticker %in% c('btc')) |>
  gg_season(roi, period = 'year', polar = FALSE, labels = 'both') +
  xlab('Time YTD') +
  ylab('ROI') +
  theme_minimal() +
  scale_x_date(date_breaks = "1 month", date_labels = "%b") +
  scale_y_continuous(breaks = seq(1, max_roi, by = 1))

# Select only specific ones
pre_halving_years = c(2015, 2019, 2023)
halving_years = c(2016, 2020) # 2024
bullmarket_years = c(2017, 2021) # 2025
bearmarket_years = c(2014, 2018, 2022) # 2026

cycle = pre_halving_years

df |> 
  filter(ticker %in% c('btc'),
         year %in% cycle) |>
  tsibble::fill_gaps() |> 
  group_by(year) |> 
  gg_season(roi, period = 'year', polar = FALSE, labels = 'both') +
  xlab('Time YTD') +
  ylab('ROI') +
  theme_minimal() +
  scale_x_date(date_breaks = "1 month", date_labels = "%b") +
scale_y_continuous(breaks = seq(1, max_roi, by = 1))
  


# Plot the average as well  ----------------------------------------------------
# 
# test = df |> 
#   filter(ticker %in% c('btc'),
#          year %in% c(2015, 2019)) |> 
#   group_by(month_day) |> 
#   mutate(roi = mean(roi),
#          year = 20152019, 
#          ticker = 'avg') |> 
#   select(roi, year, ticker) |> ungroup() |> as_tibble()
# 
# test0 = df |> select(roi, month_day, year) |> as_tibble()
# test1 = dplyr::bind_rows(test0, test)
# test2 = as_tsibble(test1, key = c(ticker), index = index)
# 
# test2 |> 
#   filter(ticker %in% c('btc', 'avg'),
#          year %in% c(2015, 2019, 2023, 20152019)) |>
#   tsibble::fill_gaps() |> 
#   group_by(year) |> 
#   gg_season(roi, period = 'year', polar = FALSE, labels = 'both') +
#   xlab('Time YTD') +
#   ylab('ROI') +
#   theme_minimal() +
#   scale_x_date(date_breaks = "1 month", date_labels = "%b") +
#   scale_y_continuous(breaks = seq(1, max_roi, by = 1))
# 


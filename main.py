import requests
import json
# import myob
import util.parentimport
util.parentimport.add_parent_import()
from _myob.stock_news_normal_start import myob


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = myob.STOCK_API_KEY

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = myob.NEWS_API_KEY

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
response = requests.get(STOCK_ENDPOINT, stock_params)
response.raise_for_status()
data: dict = response.json()["Time Series (Daily)"]
# print(data)
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
print(yesterday_data)
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

# 2. - Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_data_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_data_closing_price)

# 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
positive_difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_data_closing_price))
print(positive_difference)

# 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = (positive_difference / float(yesterday_closing_price)) * 100
print(diff_percent)

# 5. - If TODO4 percentage is greater than 5 then print("Get News").
if diff_percent > 5:
    print("Get News")

## STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
if diff_percent > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
        # "qInTitle": "tesla borsa",
        # "language": "it"
    }
    response = requests.get(NEWS_ENDPOINT, params=news_params)
    response.raise_for_status()
    data: dict = response.json()["articles"]
    print(response.url)
    # print(data)

# 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
first3: list = data[:3]
print(json.dumps(first3, indent=4))

## STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

# 8. - Create a new list of the first 3 article's headline and description using list comprehension.
summaries = [f"Headline: {article['title']}\nBrief: {article['description']}" for article in first3]
for summary in summaries:
    print(summary)
# 9. - Send each article as a separate message via Twilio.
pass

# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

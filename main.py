import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "5XYPU296ZK1GM8TZ"
NEWS_API_KEY = "6da730ae30504238b20f206803be187d"

TWILIO_SID = "ACf8cdbcd2a0aa7b3e6395cb76711b9381"
TWILIO_AUTH_TOKEN = "f739c052740a2b388d354afa3e290111"

stock_params = {
    "function":"TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price =  yesterday_data["4. close"]
print(data_list)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
diff_percent = difference / float(yesterday_closing_price) * 100
if diff_percent > 3:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]

    formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from="+(606)6444759",
            to="+5551991255914",
        )



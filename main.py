from src.bots.reddit_bot import TradeBotReddit


def main():
    tb = TradeBotReddit()

    print(f"NVDA Sentiments : {tb.make_order_recommendation('NVDA')}")
  

if __name__ == "__main__":
    main()

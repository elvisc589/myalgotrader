import pandas as pd
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import emoji

from src.bots.base_trade_bot import OrderType, TradeBot
from src.utilities import RedditCredentials
from src.data import new_words

MINIMUM_CONSENSUS_BUY_SCORE = 0.3
MINIMUM_CONSENSUS_SELL_SCORE = -0.3


class TradeBotReddit(TradeBot):
    def __init__(self):
        """Logs user into their Robinhood account."""

        super().__init__()
        try:
        # Connect to the Reddit API
            reddit_credentials = RedditCredentials()
            auth = praw.Reddit(user_agent="Comment Extraction",
                            client_id=reddit_credentials.client_id,
                            client_secret=reddit_credentials.client_secret,
                            username=reddit_credentials.user,
                            password=reddit_credentials.password)
            self.reddit_api = auth
        except praw.exceptions.APIException as e:
            print("Authentication failed: ", e)
        else:
            print("Successfully logged into Reddit account.")

        # Set up the sentiment analyzer
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.sentiment_analyzer.lexicon.update(new_words)

    def retrieve_comments(self, ticker, max_count=100):
        """
        Retrieves posts from subreddits about ticker.

        :param ticker: A company's ticker symbol as a string
        :param max_count: The maximum number of tweets to retrieve
        :return: A list of strings of the retrieved tweets
        """

        all_comments = []
        subs = ['wallstreetbets']
        post_flairs = {'Discussion'}    # post flairs to be considered. None flair is considered automatically.
        ups = 4       # Amount of upvotes needed to be considered
        if not ticker:
            print("ERROR: param ticker cannot be a null value")
            return all_comments

        if max_count <= 0:
            print("ERROR: param max_count must be a positive number.")
            return all_comments
    
        for sub in subs:
            subreddit = self.reddit_api.subreddit(sub)
            monthly_comments = subreddit.search(f"{ticker}", time_filter="week")
            for submission in monthly_comments:
                flair = submission.link_flair_text 
                        
                if (flair in post_flairs or flair is None) and submission.ups>ups and not (("**User Report**" in submission.selftext or "://" in submission.selftext)):
                     all_comments.append(submission.selftext)

        return all_comments           

                            

    def analyze_comment_sentiments(self, comments):
        """
        Analyzes the sentiments of each post and returns the average sentiment.

        :param comments: A list of strings containing the text from comments
        :return: The mean of all the sentiment scores from the list of tweets
        """

        if not comments:
            print("ERROR: param comments cannot be a null value")
            return 0

        # Initialize an empty DataFrame.
        column_names = ["comment", "sentiment_score"]
        comment_sentiments_df = pd.DataFrame(columns=column_names)

        # Get the sentiment score for each comment and append the text and sentiment_score into the DataFrame.
        for full_comment in comments:
            comment = emoji.get_emoji_regexp().sub(u'', full_comment) # remove emojis
            score = self.sentiment_analyzer.polarity_scores(comment)["compound"]
            comment_sentiment = {"comment": comment, "sentiment_score": score}
            print(comment_sentiment)
            comment_sentiments_df = pd.concat(
                [comment_sentiments_df, pd.DataFrame([comment_sentiment])],
                ignore_index=True,
            )

        # Calculate the average sentiment score.
        average_sentiment_score = comment_sentiments_df["sentiment_score"].mean()

        return average_sentiment_score

    def make_order_recommendation(self, ticker):
        """
        Makes an order recommendation based on the sentiment of max_count tweets about ticker.

        :param ticker: A company's ticker symbol as a string
        :return: OrderType recommendation
        """

        if not ticker:
            print("ERROR: param ticker cannot be a null value")
            return None

        all_comments = self.retrieve_comments(ticker=ticker)
        consensus_score = self.analyze_comment_sentiments(all_comments)

        print(consensus_score)

        # Determine the order recommendation.
        if consensus_score >= MINIMUM_CONSENSUS_BUY_SCORE:
            return OrderType.BUY_RECOMMENDATION

        elif consensus_score <= MINIMUM_CONSENSUS_SELL_SCORE:
            return OrderType.SELL_RECOMMENDATION

        else:
            return OrderType.HOLD_RECOMMENDATION
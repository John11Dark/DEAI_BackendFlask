from . import SentimentAnalyzer

SA = SentimentAnalyzer()


class SentimentAnalysisAPI:
    def __init__(self, data, source, description):
        self.data = data
        self.source = source
        self.description = description

    def getSentiment(self):
        # Sentiment Analysis
        if self.source == "audio":
            return SA.audio(file=self.data, description=self.description)
        elif self.source == "review":
            return SA.review(file=self.data, description=self.description)
        elif self.source == "text":
            return SA.text(file=self.data, description=self.description)
        elif self.source == "image":
            return SA.image(file=self.data, description=self.description)
        elif self.source == "video":
            return SA.video(file=self.data, description=self.description)
        elif self.source == "web":
            return SA.web(file=self.data, description=self.description)
        else:
            return None

from datetime import datetime

import langid
langid.set_languages(["en", "ru"])

class LLM():
    def get_user_query_language(self, user_query):
        language, confidence = langid.classify(user_query)
        return language

    def stream_response(self, response):
        if len(response) < self.chunk_size:
            yield response
        else:
            for i in range(0, len(response), self.chunk_size):
                yield response[i:i + self.chunk_size]

        yield "\n\n"
        
    def profiling(self):
        now = datetime.now()
        now = now.strftime("%d.%m.%Y %H:%M:%S")
        return f"{now}" 
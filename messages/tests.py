import unittest
from sentences import Message


class SentenceParsingTest(unittest.TestCase):
    def test_reply_sense_check(self):
        sentence = "Производит духи высочайшего качества и средства для того, чтобы вы им перерезали себе горло"
        parsed_sentence_sentiment, parsed_sentence_array = Message(sentence).get_result()
        errors_in_parse = False
        for i in range(0, len(parsed_sentence_array)):
            if i == 0:
                if len(parsed_sentence_array[i]) == 0:
                    errors_in_parse = True
            else:
                for j in parsed_sentence_array[i]:
                    if not j[0]["word"] in sentence:
                        errors_in_parse = True

        # print(parsed_sentence_array, parsed_sentence_sentiment)
        # self.assertNotEqual(len(parsed_sentence_sentiment), 0)
        self.assertEqual(errors_in_parse, False)

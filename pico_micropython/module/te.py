# Tester file

import re
decoded_topic = "users/usr1/lamp/toggle"

print(type(decoded_topic))


class MatchTopic:
    def test(self, topic, target: str):
        print(re.match(target, topic).group(0))
        try:
            return re.match(target, topic).group(0).split('/')
        except:
            return False


# pattern =
# out = re.compile(r"users/[A-Za-z0-9]+/lamp/[a-zA-Z]+").match(decoded_topic)
# out =re.match
# out = re.split(r"users/[A-Za-z0-9]+/lamp/[a-zA-Z]+", decoded_topic)
if x := MatchTopic().test(decoded_topic, r"users/[A-Za-z0-9]+/lamp/[a-zA-Z]+"):
    print(x[1])
else:
    print('wrong')
print(MatchTopic().test(decoded_topic, r"users/[A-Za-z0-9]+/lamp/[a-zA-Z]+"))

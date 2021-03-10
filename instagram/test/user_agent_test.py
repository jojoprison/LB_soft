from user_agent import generate_user_agent, generate_navigator
from pprint import pprint
from user_agents import parse
from fake_useragent import UserAgent

if __name__ == '__main__':
    pprint(generate_navigator())

    ua_string = generate_user_agent()
    user_agent = parse(ua_string)

    print(user_agent.browser)
    print(user_agent.os)
    print(user_agent.device)

    print(str(user_agent))

    ua = UserAgent()
    ua.update()
    print(ua.random)


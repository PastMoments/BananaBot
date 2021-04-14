from itertools import cycle

PREFIX = "~"

# The minimum number of characters to match a subscription
MIN_MATCH = 3

bot_statuses = cycle([
        'A healthy source of vitamin C.',
        'Remember to eat your daily banana!',
        'Banana fibre can be used to make clothes',
        'with Apple',
        'Bananas attract spiders',
        'spending time with Monke'
    ])

responses = [
        "As I see it, yes.",
        "Don't count on it.",
        "It is certain.",
        "It is decidedly so.",
        "Most likely.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Outlook good.",
        "Signs point to yes.",
        "Very doubtful.",
        "Without a doubt.",
        "Yes.",
        "Yes - definitely.",
        "You may rely on it.",
        "Absolutely not.",
        "Of course!",
        "No, of course not.",
        "No, why would you even ask that?",
        "Did you even need to ask me? Hell yeah!",
        "I'm convinced you aren't even human if you asked me that.",
        "Do bananas have peels? Of course the answer is yes!"
        ]

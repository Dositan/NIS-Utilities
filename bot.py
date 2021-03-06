from utils.Bot import NisBot

bot = NisBot()

for ext in bot.config['bot']['exts']:
    bot.load_extension(ext)

if __name__ == '__main__':
    bot.run(bot.config['bot']['TOKEN'])

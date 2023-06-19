from .extension import GiphyExtension


def setup(bot):
    bot.add_cog(GiphyExtension(bot))

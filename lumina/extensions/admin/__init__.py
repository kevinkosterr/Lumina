from .extension import AdminExtension


def setup(bot):
    bot.add_cog(AdminExtension(bot))

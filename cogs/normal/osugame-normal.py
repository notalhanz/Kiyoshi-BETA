""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

import json
import os
import sys
import disnake
import requests

from disnake.ext import commands
from disnake.ext.commands import Context

from helpers import checks
from osu import osuAPIv2 as osu

# Only if you want to use variables that are in the config.json file.
if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

# Here we name the cog and create a new class for the cog.
class osugame(commands.Cog, name="osugame-normal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="osu",
        description="Check your osu!profile via 'osu <username>",
    )
    @checks.not_blacklisted()
    async def osu(self, ctx: Context, arg):
        """
        This is a testing command that does nothing.
        :param context: The context in which the command has been executed.
        """
        token = osu.get_token()

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        params = {
            'user': 'username',
            'mode': 'osu',
            'limit': 5
        }

        #for API
        response = requests.get(f'{osu.API_URL}/users/{arg}', params=params, headers=headers)
        player = response.json()
        avatar = response.json()["avatar_url"]
        stats = response.json()["statistics"]

        #getting information via JSON
        playstyle = player.get('playstyle')
        username = player.get('username')
        accuracy = stats.get('hit_accuracy')
        perfpoints = stats.get('pp')
        playerlvl = stats.get("level")
        mapranks = stats.get('grade_counts')

        playerurl = 'https://osu.ppy.sh/u/' + str(player.get('id'))

        #emojis for each map rankings
        rankingXH = self.bot.get_emoji(956815860587180052)
        rankingX = self.bot.get_emoji(956815860654309406)
        rankingSH = self.bot.get_emoji(956815860662665226)
        rankingS = self.bot.get_emoji(956815860650090516)
        rankingA = self.bot.get_emoji(956815860675256370)

        osuEmbed = disnake.Embed(description="**osu!stats for: " + f"[{username}]({playerurl})**", color=0x69ff96)
        osuEmbed.add_field(name="Performance:",
            value=(" **--- {:,.2f}**".format(perfpoints) +
             "\n **Global Rank:** #" + str(stats.get('global_rank')) + " (" + str(player.get('country_code')) + "#" + str(stats.get('country_rank')) + ")" +
             "\n **Accuracy:** " + str(round((accuracy), 2)) + "%" +
             "\n **Play Count:** " + str(stats.get('play_count')) +
             "\n **Level:** " + str(playerlvl.get('current')) +
             "\n **Play Style:** \n" + (', '.join(playstyle)).title() + "\n"
            ),
            inline=True
        )

        osuEmbed.add_field(name="Rank",
            value=f"{rankingXH} : " + str(mapranks.get('ssh')) +
            f"\n {rankingX} : " + str(mapranks.get('ss')) + 
            f"\n {rankingSH} : " + str(mapranks.get('sh')) + 
            f"\n {rankingS} : " + str(mapranks.get('ss')) +
            f"\n {rankingA} : " + str(mapranks.get('a')),
            inline=True
        )

        osuEmbed.set_thumbnail(url=avatar)
        osuEmbed.set_footer(text="WeebBot is currently on Heavy Maintenance! | requested by: {}".format(ctx.author.display_name))

        await ctx.send(embed=osuEmbed)

    @commands.command(
        name="osurecent",
        description="Check your osu! recent score via 'osurecent <username>",
    )
    @checks.not_blacklisted()
    async def osurecent(self, ctx, arg):
        token = osu.get_token()

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        params = {
            'user': 'username',
            'include_fails': 0,
            'mode': 'osu',
            'limit': 5
        }

        #Since there's no API to gather ID, this should be
        args = requests.get(f'https://osu.ppy.sh/api/get_user?k=fa78b3825600dfb1b7e4a3bd8c0b0e65f0d414dc&u={arg}&limit=1')
        gather_id = args.json()[0].get("user_id")

        #for API
        response = requests.get(f'{osu.API_URL}/users/'+ gather_id +'/scores/recent', params=params, headers=headers)
        stats = response.json()[0]
        beatmapset = response.json()[0].get("beatmapset")
        mods = response.json()[0].get("mods")
        beatmap = response.json()[0].get("beatmap")
        user = response.json()[0].get("user")
        pp = response.json()[0].get("pp")

        mapVersion = beatmap.get("version")
        mapTitle = beatmapset.get("title")
        diff_rating = beatmap.get("difficulty_rating")
        beatmap_url = beatmap.get("url")
        userrank = stats.get("rank")
        username = user.get("username")

        osursEmbed = disnake.Embed(color=0x69ff96)
        osursEmbed.set_author(name=f"{mapTitle} [{mapVersion}] {''.join(mods)} [{diff_rating}★]",
            url=beatmap_url,
            icon_url=user.get("avatar_url")
            )
        osursEmbed.add_field(name=f"Recent Score Stat of {username}",
            value=f"Rank: **{userrank}**" +
            f"\n PP: {str(round((pp), 2))}pp"
            )

        await ctx.send(embed=osursEmbed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(osugame(bot))

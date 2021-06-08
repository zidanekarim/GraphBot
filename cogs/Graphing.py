import asyncio
import io
import os
import numpy as np
import discord
import matplotlib.pyplot as plt
from discord.ext import commands
from dotenv import load_dotenv




class Graphing(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def graph(self, ctx):
        await ctx.send("Alright! Input your **x** coordinates! Separate them with a space!")
        def check(m):
            return m.author == ctx.author
        try:

            x = await self.client.wait_for('message', timeout=30, check=check)
            x = x.content.split()
            xlist = []
            for strx in x:
                xlist.append(int(strx))

            await ctx.send("Alright! Now input your **y** coordinates! Separate them with a comma!")

            y = await self.client.wait_for("message", timeout=30, check=check)
            y = y.content.split()
            ylist = []
            for stry in y:
                ylist.append(int(stry))


        

        except asyncio.TimeoutError:
            await ctx.send("You took too long!")
            return

        if len(ylist) != len(xlist) or len(xlist) < 1:
            await ctx.send("Hey! You entered too many or too little terms!")
            return


        plt.plot(xlist, ylist, 'o:b')
        plt.title(f"Graph for {ctx.author}")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(axis="both")
        out = io.BytesIO()
        out.name = 'graph.png'
        plt.savefig(out, bbox_inches='tight')
        plt.close()
        out.seek(0)

        await ctx.send(file=discord.File(out))


    @commands.command()
    async def circle(self, ctx):
        await ctx.send("Alright! Input your **center** coordinates! Separate them with a space!")
        def check(m):
            return m.author == ctx.author
        try:
            center = await self.client.wait_for('message', timeout=30, check=check)
            centerlist = [float(strcenter) for strcenter in center.content.split()]


        except asyncio.TimeoutError:
            await ctx.send("You took too long!")
            return
        await ctx.send("Alright! Input your **radius**!")
        try:
            radius = await self.client.wait_for('message', timeout=30, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You took too long!")
            return



        
        radius = float(radius.content)

        if len(centerlist) != 2:
            await ctx.send("You specified improper! coordinates!")
        


        fig, ax = plt.subplots()
        draw_circle = plt.Circle((centerlist[0],centerlist[1]), radius, fill=True)
        ax.set_aspect(1)
        ax.add_artist(draw_circle)
        plt.xlim([round(centerlist[0] - 10), round(centerlist[0] + 10)])
        plt.ylim([round(centerlist[1] - 10), round(centerlist[1] + 10)])
        plt.plot(centerlist[0], centerlist[1], color="black", marker='o')

        plt.title(f"Circle for {ctx.author}")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(axis="both")

                
        out = io.BytesIO()
        out.name = 'graph.png'
        plt.savefig(out, bbox_inches='tight')
        plt.close()
        out.seek(0)
        await ctx.send(file=discord.File(out))




    @commands.command()
    async def slope(self, ctx):
        def check(m):
            return m.author == ctx.author
        # try:
        #     points = await self.client.wait_for('message', timeout=30, check=check)
        #     points = [round(float(strcenter), 1) for strcenter in points.content.split()]


        # except asyncio.TimeoutError:
        #     await ctx.send("You took too long!")
        #     return


        await ctx.send("Input your slope!")
        try:
            slope = await self.client.wait_for('message', timeout=30, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You took too long!")
            return

        slope = round(float(slope.content), 1)

        await ctx.send("Input your y-intercept!")
        try:
            b = await self.client.wait_for('message', timeout=30, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You took too long!")
            return

        b = round(float(b.content), 1)

        xlist = np.array([finalx for finalx in np.arange(b+5)])




        print(xlist)

        ylist = np.array([finaly*slope + b for finaly in xlist])
        print(ylist)


        plt.plot(0, b, color='black', marker="o")
        plt.plot(xlist, ylist, color='black', marker="o")



        plt.title(f'Graph of y = {slope}x + {b} by {ctx.author}')
        plt.xlabel('X', color='#1C2833')
        plt.ylabel('Y', color='#1C2833')



        plt.grid()
        
        out = io.BytesIO()
        out.name = 'graph.png'
        plt.savefig(out, bbox_inches='tight')
        plt.close()
        out.seek(0)
        await ctx.send(content="Note: This is rounded to the nearest **tenth** in order to maximize precision",file=discord.File(out))
        


def setup(client):
  client.add_cog(Graphing(client))


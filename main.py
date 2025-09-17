import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import ButtonStyle
from discord import Color
import re
import json
import requests
from asyncio import sleep
from dotenv import load_dotenv
import os

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

TOKEN = os.getenv('TOKEN')

async def check_stock(interaction, store: str, item: str):
    reqUrl = "https://stockchecker.sainsburys.co.uk/api/store/search"

    headersList = {
     "Accept": "*/*",
     "Host": "stockchecker.sainsburys.co.uk",
     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
     "Accept-Language": "en-GB,en;q=0.5",
     "Accept-Encoding": "gzip, deflate, br",
     "Referer": "https://stockchecker.sainsburys.co.uk/",
     "Content-Type": "text/plain;charset=UTF-8",
     "Content-Length": "50",
     "Origin": "https://stockchecker.sainsburys.co.uk",
     "Connection": "keep-alive",
     "Sec-Fetch-Dest": "empty",
     "Sec-Fetch-Mode": "cors",
     "Sec-Fetch-Site": "same-origin",
     "TE": "trailers" 
    }
    payload = json.dumps({"store_type": "main,local", "complete": str(store)})

    response = requests.request("POST", reqUrl, data=payload, headers=headersList)
    jsonFile = json.loads(response.text)

    if jsonFile == None:
        print("empty datadict")
    
    emptyjson = {"page_meta": {"limit": 20, "offset": 0, "total": 0}, "results": []}
    if jsonFile == emptyjson:
        store_name = None
        return store_name


    try:
        store_list = jsonFile["results"][0] 
        store_code = store_list['code']
        store_name = store_list['name']
    except Exception as e:
        print(e)
        
    payload = json.dumps({"variables": {"store": store_code, "query": item, "pageNumber": 1}})

    response = requests.request("POST", "https://stockchecker.sainsburys.co.uk/api/products/search", data=payload, headers=headersList)

    jsonFile = json.loads(response.text)

    responsestr =  'Store name: '+store_name +"\n"

    global embed
    embed = discord.Embed(title="Stock for: " +store_name,colour=Color.orange()) # creating embed

    for product in jsonFile['data']['productSearch']['storeProducts']:
        sku = str(product['sku'])
        description = product['description']
        retail_price = str(product['store']['retailPrice']) if product['store'] and product['store'].get('retailPrice') else "N/A"
        onhand_stock = str(product['store']['stock']['onHand']) if product['store'] and product['store']['stock'] else "N/A"
        responsestr += description + ", £" + retail_price + ", stock: " + onhand_stock + "\n"
        if onhand_stock == "In Stock":
            embed.add_field(name="Item name: "+description, value="Price: £" + retail_price+ "\n" + "🟢 Stock: " + onhand_stock + "\n" + "SKU: " + sku,inline=False)
        elif onhand_stock == "N/A":
            embed.add_field(name="Item name: "+description, value="🔴 Out of stock",inline=False)
        else:
            embed.add_field(name="Item name: "+description, value="An error occured!",inline=False)
    return store_name

async def checkstorename(interaction, store: str):
    reqUrl = "https://stockchecker.sainsburys.co.uk/api/store/search"

    headersList = {
     "Accept": "*/*",
     "Host": "stockchecker.sainsburys.co.uk",
     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
     "Accept-Language": "en-GB,en;q=0.5",
     "Accept-Encoding": "gzip, deflate, br",
     "Referer": "https://stockchecker.sainsburys.co.uk/",
     "Content-Type": "text/plain;charset=UTF-8",
     "Origin": "https://stockchecker.sainsburys.co.uk",
     "Connection": "keep-alive",
     "Sec-Fetch-Dest": "empty",
     "Sec-Fetch-Mode": "cors",
     "Sec-Fetch-Site": "same-origin",
     "TE": "trailers" 
    }
    payload = json.dumps({"store_type": "main,local", "complete": str(store)})
    response = requests.request("POST", reqUrl, data=payload, headers=headersList)
    jsonFile = json.loads(response.text)
    store_names = []
    for stores in jsonFile["results"]:
        store_name = stores.get("other_name", "N/A")
        store_names.append(store_name)

    global embed
    embed = discord.Embed(title="Store name search for: "+store) # creating embed

    for i, store_name in enumerate(store_names[:5], start=1):
        embed.add_field(name=f"Store {i}", value=store_name, inline=False)
    return store_names

async def lorcana(interaction, store: str):
    reqUrl = "https://stockchecker.sainsburys.co.uk/api/store/search"

    headersList = {
     "Accept": "*/*",
     "Host": "stockchecker.sainsburys.co.uk",
     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
     "Accept-Language": "en-GB,en;q=0.5",
     "Accept-Encoding": "gzip, deflate, br",
     "Referer": "https://stockchecker.sainsburys.co.uk/",
     "Content-Type": "text/plain;charset=UTF-8",
     "Content-Length": "50",
     "Origin": "https://stockchecker.sainsburys.co.uk",
     "Connection": "keep-alive",
     "Sec-Fetch-Dest": "empty",
     "Sec-Fetch-Mode": "cors",
     "Sec-Fetch-Site": "same-origin",
     "TE": "trailers" 
    }
    payload = json.dumps({"store_type": "main,local", "complete": str(store)})

    response = requests.request("POST", reqUrl, data=payload, headers=headersList)
    jsonFile = json.loads(response.text)

    if jsonFile == None:
        print("empty datadict")
    
    emptyjson = {"page_meta": {"limit": 20, "offset": 0, "total": 0}, "results": []}
    if jsonFile == emptyjson:
        store_name = None
        return store_name

    try:
        store_list = jsonFile["results"][0]
        store_code = store_list['code']
        store_name = store_list['name']

    except Exception as e:
        print(e)
        
    payload = json.dumps({"variables": {"store": store_code, "query": "Disney Lorcana Tcg Booster", "pageNumber": 1}})

    response = requests.request("POST", "https://stockchecker.sainsburys.co.uk/api/products/search", data=payload, headers=headersList)

    jsonFile = json.loads(response.text)

    responsestr =  'Store name: '+store_name +"\n"

    global embed
    embed = discord.Embed(title="Stock for: " +store_name,colour=Color.orange())

    for product in jsonFile['data']['productSearch']['storeProducts']:
        sku = str(product['sku'])
        description = product['description']
        retail_price = str(product['store']['retailPrice']) if product['store'] and product['store'].get('retailPrice') else "N/A"
        onhand_stock = str(product['store']['stock']['onHand']) if product['store'] and product['store']['stock'] else "N/A"
        responsestr += description + ", £" + retail_price + ", stock: " + onhand_stock + "\n"
        if onhand_stock == "In Stock":
            embed.add_field(name="Item name: "+description, value="Price: £" + retail_price+ "\n" + "🟢 Stock: " + onhand_stock + "\n" + "SKU: " + sku,inline=False)
        elif onhand_stock == "N/A":
            embed.add_field(name="Item name: "+description, value="🔴 Out of stock",inline=False)
        else:
            embed.add_field(name="Item name: "+description, value="An error occured!",inline=False)
    return store_name



@bot.tree.command(name="checkstores")
async def check_store_wrapper(ctx, store: str):
    if not re.match("^[a-zA-Z ]+$", store):
        print(f"{username} searched for store {store} - used other characters")
        await ctx.response.send_message("Sorry, store search must only contain letters.", ephemeral=True)
        return
    
    try:
        username = ctx.user.name
    except:
        username = "[Unable to get name]"


    storenames = await checkstorename(ctx, store)
    if storenames == []:
        print(f"{username} searched for store {store} - no store found")
        await ctx.response.send_message("No stores found for your search.", ephemeral=True)
    elif storenames != []:
        print(f"{username} searched for store {store}")
        await ctx.response.send_message(embed=embed, ephemeral=True)
    else:
        print(f"{username} searched for store {store} - error occured")
        await ctx.response.send_message("An error occured.", ephemeral=True)

@bot.tree.command(name="checkstock")
async def check_stock_wrapper(ctx, store: str, item: str):
    try:
        username = ctx.user.name
    except:
        username = "[Unable to get name]"

    if not re.match("^[a-zA-Z ]+$", store):
        print(f"{username} checked stock at {store} - used other characters")
        await ctx.response.send_message("Store search must only contain letters.", ephemeral=True)
        return

    store_name = await check_stock(ctx, store, item)
    if store_name == None:
        print(f"{username} checked stock at {store} - no store found")
        await ctx.response.send_message('No store was found, please try using /checkstores', ephemeral=True)
    else:
        print(f"{username} checked stock at {store_name}")
        await ctx.response.send_message(content="Loading stock...",ephemeral=True)
        await ctx.edit_original_response(content="",embed=embed) 

@bot.tree.command(name="checklorcana")
async def check_stock_wrapper(ctx, store: str):
    try:
        username = ctx.user.name
    except:
        username = "[Unable to get name]"

    if not re.match("^[a-zA-Z ]+$", store):
        print(f"{username} checked stock at {store} - used other characters (Lorcana)")
        await ctx.response.send_message("Store search must only contain letters.", ephemeral=True)
        return

    store_name = await lorcana(ctx, store)
    if store_name == None:
        print(f"{username} checked stock at {store} - no store found (Lorcana)")
        await ctx.response.send_message('No store was found, please try using /checkstores', ephemeral=True)
    else:
        print(f"{username} checked stock at {store_name}")
        await ctx.response.send_message(content="Loading stock...",ephemeral=True)
        await ctx.edit_original_response(content="",embed=embed) 

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="stock levels!"))
    print("Bot is running")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

bot.run(TOKEN)   

import random
import aiohttp



async def get_logpose():
    try:
        onepiece_api_url = "https://api.api-onepiece.com/v2/"
        category=['characters/en','fruits/en','bounties','ships','islands']
        choice = random.randint(0,1)

        if choice == 0:
            async with aiohttp.ClientSession() as session:
                async with session.get(onepiece_api_url+category[0]) as response:
                    data = await response.json()
                    charecter_with_bounty=[]
                    for i in data:
                        if i.get("bounty"):
                            charecter_with_bounty.append(i)

                    num = random.randint(0,len(charecter_with_bounty)-1)

            name = charecter_with_bounty[num]["name"]
            bounty = charecter_with_bounty[num]["bounty"]
            # print("Name:", charecter_with_bounty[num]["name"])
            # print("Bounty:", charecter_with_bounty[num]["bounty"])
            return choice,name,bounty

        elif choice == 1:
            async with aiohttp.ClientSession() as session:
                async with session.get(onepiece_api_url+category[1]) as response:
                    data = await response.json()
                    num = random.randint(0,len(data)-1)
            name = data[num]["name"]
            descrption = data[num]["description"]
            # print("Fruit:", data[num]["name"])
            # print("Power:", data[num]["description"])
            return choice,name, descrption

        

        
    except Exception as e:
        print("Log Pose error:", e)
        return None
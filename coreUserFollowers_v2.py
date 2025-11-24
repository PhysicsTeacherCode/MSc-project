from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import requests

core_user = [
"randall.gobirds.online",
"msevelyn.bsky.social",
"lexicodex.bsky.social",
"garyrbs.bsky.social",
"jelle8591.bsky.social",
"aussieopinion.bsky.social",
"freebirdthirteen.bsky.social",
"janvan.bsky.social",
"lizettekodama.bsky.social",
"ludditebro.bsky.social",
"stellasjr.bsky.social",
"soupster16.bsky.social",
"niksea.bsky.social",
"bunnygabby.bsky.social",
"rst0868.bsky.social",
"yourcomicmuse.bsky.social",
"willcuthere.bsky.social",
"cionaod.bsky.social",
"aut-of-order.bsky.social",
"leandrot.bsky.social"
]

# -----------------------
# 1. Buscar seguidores
# -----------------------
def get_followers(actor_handle):
    url = "https://public.api.bsky.app/xrpc/app.bsky.graph.getFollowers"
    cursor = None
    followers = []

    while True:
        params = {
            "actor": actor_handle,
            "limit": 100
        }
        if cursor:
            params["cursor"] = cursor

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print("Erro:", response.status_code, response.text)
            break

        data = response.json()

        # lista de seguidores retornados na página atual
        for item in data.get("followers", []):
            followers.append(item.get("handle"))

        # pega o próximo cursor para continuar
        cursor = data.get("cursor")

        if not cursor:
            break

        # pequena pausa para respeitar limites
        # time.sleep(0.3)

    return actor_handle, followers

# -----------------------
# 2. Executando
# -----------------------
followers_list = []
collumnsName = []
with ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(get_followers, user) for user in core_user]
    for future in as_completed(futures):
        actor, users = future.result()
        followers_list.append(users)
        collumnsName.append(actor)

#df = pd.DataFrame(followers_list).T
#df.columns = collumnsName
#df.to_excel("all_followers.xlsx", index=False)

# -----------------------
# 3. Visualizando
# -----------------------
for x in followers_list:
   print(len(x),x)
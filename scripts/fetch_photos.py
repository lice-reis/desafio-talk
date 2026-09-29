"""Download free Unsplash photos for the demo and record photographer credits.

Run once: python3 scripts/fetch_photos.py
Every image saved is under the Unsplash License (free to use).
"""
import itertools, json, os, socket, subprocess, sys, time, urllib.request, urllib.parse
socket.setdefaulttimeout(20)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
CREDITS = {}
_c = os.path.join(ASSETS, "credits.json")
if os.path.exists(_c):
    CREDITS = json.load(open(_c))
SEEN = set()

def search(query, orientation, per_page=30, page=1):
    q = urllib.parse.urlencode({"query": query, "per_page": per_page, "page": page, "orientation": orientation})
    # the search endpoint rejects python's urllib but accepts curl, so shell out
    out = subprocess.run(["curl", "-s", f"https://unsplash.com/napi/search/photos?{q}"], capture_output=True, text=True, timeout=30).stdout
    data = json.loads(out)
    # skip Unsplash+ (premium) photos: they are not free
    return [p for p in data["results"] if "plus.unsplash.com" not in p["urls"]["raw"] and not p.get("premium")]

def grab(queries, orientation, folder, prefix, count, width):
    os.makedirs(os.path.join(ASSETS, folder), exist_ok=True)
    got, page = 0, 1
    # round-robin across queries so no single query dominates the folder
    lists = []
    for qq in queries:
        lists.append(search(qq, orientation))
        time.sleep(0.4)
    pool = [p for group in itertools.zip_longest(*lists) for p in group if p]
    for p in pool:
        if got >= count:
            break
        if p["id"] in SEEN:
            continue
        SEEN.add(p["id"])
        url = p["urls"]["raw"].split("?")[0] + f"?w={width}&q=80&fm=jpg&fit=crop"
        name = f"{prefix}-{got+1:02d}.jpg"
        dest = os.path.join(ASSETS, folder, name)
        try:
            urllib.request.urlretrieve(url, dest)
        except Exception as e:
            print("skip", p["id"], e)
            continue
        CREDITS[f"{folder}/{name}"] = {
            "photographer": p["user"]["name"],
            "profile": p["user"]["links"]["html"],
            "photo": p["links"]["html"],
        }
        got += 1
        with open(os.path.join(ASSETS, "credits.json"), "w") as f:
            json.dump(CREDITS, f, indent=2, ensure_ascii=False)
        print(folder, name, "<-", p["user"]["name"], flush=True)
        time.sleep(0.2)
    if got < count:
        print(f"WARNING: {folder} wanted {count}, got {got}", file=sys.stderr)

# Feed posts (4:5 / square crops handled by the UI)
#grab(["trail running mountain", "trail runner forest", "ultra trail race"], "squarish", "posts", "post", 10, 1080)
# Stories (vertical)
#grab(["trail running", "mountain trail sunrise", "hiking trail forest", "trail runner", "mountain summit runner"], "portrait", "stories", "story", 30, 1080)
# Discover grid tiles (other communities: cycling, surf, climbing, yoga, photography, road running, swimming, camping)
#grab(["road cycling", "surfing", "rock climbing", "yoga outdoor", "street photography", "marathon runners", "open water swimming", "camping tent night"], "squarish", "discover", "discover", 24, 640)
# Member avatars
#grab(["woman portrait smiling outdoor", "man portrait outdoor", "runner portrait face", "athlete headshot", "young woman portrait", "man smiling portrait", "hiker portrait face"], "squarish", "avatars", "avatar", 14, 400)
# Community profile pictures
grab(["mountain peak", "bicycle", "surfboard", "climbing wall", "yoga mat", "camera lens", "running track", "swimming pool lane", "campfire"], "squarish", "communities", "community", 9, 400)

print("done:", len(CREDITS), "photos")

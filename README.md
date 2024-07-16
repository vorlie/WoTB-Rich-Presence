# Discord Rich Presence for World of Tanks Blitz
If you plan to use the `.exe`, please consider adding it to your antivirus exceptions as it may trigger a false positive due to the hidden console output and lack of code signing. An alternate version with visible console output will be provided to avoid antivirus detection.



## Useful things to know
- You might want to check `C:\Users\USER\AppData\Local\wotblitz\DAVAProject\image_cache` for the avatar image.
  - Then upload it to an image host or a Discord server, and replace the "small_image" value with the direct image URL.


## Configuration
There is an app for easier configuration. []
- You can find the full json here:
  - `username` : Your in-game username.
  - `small_image`, `avatar_url` : Your in-game avatar URL. *You don't need to set the `avatar_url` as its not being used right now*
  - `clan_tag`, `clan_name` : Your clan tag and name.
  - `favorite_tank` : Your favorite tank.
  - `tanks` : Your tank list. Please add only the tanks you have in the garage.
> Don't change the "client_id", "icon", "hero" unless you know what you are doing. 

> This client ID is the same one the game uses, so the app will overwrite the presence and not create a new one.
```json
{
    "version": "0.0.1",
    "name": "World of Tanks Blitz RPC",
    "description": "Discord Rich Presence for World of Tanks Blitz",
    "author": "Made by @vorlie",

    "config": {
        "client_id": "419272031960432651",
        "icon": "assets/icon.ico",
        "hero": "assets/hero.png",
        "large_image": "https://cx.tixte.co/r/worldoftanksblitz.png",
        "small_image": "https://cx.tixte.co/r/2666185410.png" 
    },
    "variables": {
        "player": {
            "username": "_Gold_Is_for_Bots_", 
            "avatar_url": "https://cx.tixte.co/r/2666185410.png", 
            "clan_tag": "[P-_-L]",
            "clan_name": "Polish-Legends", 
            "favorite_tank": "XM551 Sheridan"
        },
        "replacements": {
            "Ă¶": "ö",
            "Ă¤": "ä"
        },
        "tanks": [
            {
                "name": "XM551 Sheridan",
                "type": "Tech Tree",
                "tier": "X"
            },
            {
                "name": "E 100 Jötunn",
                "type": "Tech Tree",
                "tier": "X"
            },
            {
                "name": "T-62A",
                "type": "Tech Tree",
                "tier": "X"
            },
            {
                "name": "Centurion Mk. 5/1 RAAC",
                "type": "Collector",
                "tier": "VIII"
            },
            {
                "name": "Strv 81 Kämpe",
                "type": "Collector",
                "tier": "VIII"
            },
            {
                "name": "E-10",
                "type": "Collector",
                "tier": "VII"
            },
            {
                "name": "Silencer",
                "type": "Collector",
                "tier": "VII"
            },
            {
                "name": "Churchill VIII",
                "type": "Collector",
                "tier": "VI"
            },
            {
                "name": "Y5 T-34",
                "type": "Premium",
                "tier": "V"
            },
            {
                "name": "Pz. III",
                "type": "Tech Tree",
                "tier": "III"
            },
            {
                "name": "Vae Type B",
                "type": "Tech Tree",
                "tier": "I"
            },
            {
                "name": "R35",
                "type": "Tech Tree",
                "tier": "I"
            }
        ]
    }
}
```
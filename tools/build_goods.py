"""Builds data/goods/*.json for Purveyor's Broadsheet (draft 0.1).
Run from anywhere:  python3 tools/build_goods.py
All values are first guesses to be tuned. Money is whole base units (cp=1, sp=10, gp=100).
"""
import json, os, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "goods")
os.makedirs(OUT, exist_ok=True)

ANCHOR = {
 'grain':'srd51_wheat','flour':'srd51_flour','rock_salt':'srd51_salt','sea_salt':'srd51_salt',
 'iron_bar':'srd51_iron','copper_bar':'srd51_copper','silver_bar':'srd51_silver','gold_bar':'srd51_gold',
 'cloth_canvas':'srd51_canvas','spice_ginger':'srd51_ginger','spice_pepper':'srd51_pepper',
 'spice_cinnamon':'srd51_cinnamon','spice_cloves':'srd51_cloves','spice_saffron':'srd51_saffron','silk':'srd51_silk',
}
goods = []
def g(id, name, grp, cat, unit, w, v, perish=None, tier=1, res=(), inp=(), demand='ordinary', tags=(), magic=None):
    d = {"id":id,"name":name,"group":grp,"category":cat,"unit":unit,"weightLb":w,"baseValue":v,
         "perishableDays":perish,"tier":tier,"resources":list(res),"inputs":list(inp),
         "demand":demand,"tags":list(tags),"source":["own"]}
    if magic: d["magicTier"]=magic
    if id in ANCHOR:
        d["anchoredTo"]=ANCHOR[id]; d["source"]=["own","srd-5.1"]
    goods.append(d)

S50='sack (50 lb)'
# ---- MINES
g('iron_ore','Iron ore','mines','raw',S50,50,150,None,1,['mines'],[],'ordinary',['metal','ore'])
g('copper_ore','Copper ore','mines','raw',S50,50,600,None,1,['mines'],[],'ordinary',['metal','ore'])
g('tin_ore','Tin ore','mines','raw',S50,50,1100,None,1,['mines'],[],'ordinary',['metal','ore'])
g('silver_ore','Silver ore','mines','raw',S50,50,5000,None,1,['mines'],[],'luxury',['metal','ore','precious'])
g('coal','Coal','mines','raw',S50,50,25,None,1,['mines'],[],'ordinary',['fuel'])
g('rock_salt','Rock salt','mines','raw',S50,50,220,None,1,['mines'],[],'necessity',['food','preservative'])
g('gems_rough','Rough precious stones','mines','raw','oz',0.0625,1500,None,1,['mines'],[],'luxury',['gem'])
# ---- QUARRIES
g('building_stone','Building stone','quarries','raw','cartload',2000,300,None,1,['quarries'],[],'ordinary',['building','stone'])
g('marble_rough','Marble, rough block','quarries','raw','block (1 cu ft)',170,800,None,1,['quarries'],[],'luxury',['building','stone','fine'])
g('lime','Quicklime','quarries','raw',S50,50,45,None,1,['quarries'],[],'ordinary',['building'])
g('clay','Clay','quarries','raw',S50,50,15,None,1,['quarries'],[],'ordinary',['craft material'])
# ---- FARMS
g('grain','Grain','farms','raw',S50,50,50,365,1,['farms'],[],'necessity',['food','grain'])
g('barley','Barley','farms','raw',S50,50,45,365,1,['farms'],[],'ordinary',['food','grain','brewing'])
g('oats','Oats','farms','raw',S50,50,35,365,1,['farms'],[],'ordinary',['food','grain','fodder'])
g('hay','Hay','farms','raw','bale (40 lb)',40,12,180,1,['farms'],[],'ordinary',['fodder'])
g('root_veg','Root vegetables','farms','raw',S50,50,40,90,1,['farms'],[],'necessity',['food'])
g('fruit_fresh','Fresh fruit','farms','raw','basket (20 lb)',20,40,10,1,['farms'],[],'ordinary',['food'])
g('flax','Flax','farms','raw','bundle (20 lb)',20,60,365,1,['farms'],[],'ordinary',['fiber'])
g('hops','Hops','farms','raw','lb',1,9,180,1,['farms'],[],'ordinary',['brewing'])
g('herbs','Culinary herbs','farms','raw','bundle (1 lb)',1,15,10,1,['farms'],[],'ordinary',['food','medicine'])
g('honey','Honey','farms','raw','lb',1,16,None,1,['farms','husbandry'],[],'ordinary',['food','sweetener'])
g('grapes','Wine grapes','farms','raw','basket (20 lb)',20,50,7,1,['farms'],[],'ordinary',['food','brewing'])
g('dye_plants','Dye plants','farms','raw','bundle (10 lb)',10,70,60,1,['farms'],[],'ordinary',['dye'])
# ---- FISHERIES
g('fish_fresh','Fresh fish','fisheries','raw','lb',1,2,3,1,['fisheries'],[],'necessity',['food'])
g('fish_salted','Salted fish','fisheries','processed','barrel (100 lb)',100,350,365,2,['fisheries'],['fish_fresh','sea_salt'],'necessity',['food','preserved'])
g('fish_smoked','Smoked fish','fisheries','processed','lb',1,5,120,2,['fisheries'],['fish_fresh'],'ordinary',['food','preserved'])
g('fish_oil','Fish oil','fisheries','raw','gallon',8,30,None,1,['fisheries'],[],'ordinary',['oil','lighting'])
g('pearls','Freshwater pearls','fisheries','raw','dozen',0.06,800,None,1,['fisheries'],[],'luxury',['gem'])
g('sea_salt','Sea salt','fisheries','raw',S50,50,180,None,1,['fisheries'],[],'necessity',['food','preservative'])
# ---- GAME
g('pelts_small','Small-game pelts','game','raw','each',1,20,None,1,['game'],[],'ordinary',['fur'])
g('pelts_fine','Fine furs','game','raw','each',1,300,None,1,['game'],[],'luxury',['fur','fine'])
g('hide_raw','Raw hide','game','raw','each',30,60,14,1,['game','husbandry'],[],'ordinary',['hide'])
g('venison','Venison','game','raw','lb',1,4,5,1,['game'],[],'ordinary',['food','meat'])
g('wildfowl','Wildfowl','game','raw','each',2,8,4,1,['game'],[],'ordinary',['food','meat'])
g('antler_bone','Antler and bone','game','raw','sack (20 lb)',20,50,None,1,['game'],[],'ordinary',['bone','craft material'])
g('feathers','Feathers','game','raw','lb',1,30,None,1,['game'],[],'ordinary',['feather'])
# ---- TIMBER
g('firewood','Firewood','timber','raw','cord',3000,300,None,1,['timber'],[],'necessity',['fuel'])
g('lumber_rough','Rough plank (12 ft)','timber','raw','each',30,18,None,1,['timber'],[],'ordinary',['building','wood'])
g('lumber_fine','Seasoned hardwood plank (12 ft)','timber','raw','each',45,90,None,1,['timber'],[],'ordinary',['wood','fine'])
g('beam','Timber beam (10 ft)','timber','raw','each',150,120,None,1,['timber'],[],'ordinary',['building','wood'])
g('charcoal','Charcoal','timber','raw','sack (30 lb)',30,55,None,1,['timber'],[],'ordinary',['fuel'])
g('pitch_tar','Pitch and tar','timber','raw','gallon',10,40,None,1,['timber'],[],'ordinary',['sealant'])
g('tanning_bark','Tanning bark','timber','raw','sack (40 lb)',40,30,None,1,['timber'],[],'ordinary',['craft material'])
# ---- HUSBANDRY
g('wool_raw','Raw wool','husbandry','raw','lb',1,8,None,1,['husbandry'],[],'ordinary',['fiber'])
g('milk','Milk','husbandry','raw','gallon',8.6,3,2,1,['husbandry'],[],'necessity',['food'])
g('cheese','Cheese','husbandry','processed','lb',1,6,120,2,['husbandry'],['milk'],'ordinary',['food'])
g('butter','Butter','husbandry','processed','lb',1,8,30,2,['husbandry'],['milk'],'ordinary',['food'])
g('eggs','Eggs','husbandry','raw','dozen',1.5,4,21,1,['husbandry'],[],'ordinary',['food'])
g('beeswax','Beeswax','husbandry','raw','lb',1,40,None,1,['husbandry'],[],'ordinary',['wax'])
g('tallow','Tallow','husbandry','raw','lb',1,4,180,1,['husbandry'],[],'ordinary',['fat'])
g('manure','Manure','husbandry','raw','cartload',2000,30,None,1,['husbandry'],[],'ordinary',['fertilizer'])
g('lamb','Lamb','husbandry','raw','each',60,70,None,1,['husbandry'],[],'ordinary',['livestock'])
# ---- CRAFT / PROCESSED
g('flour','Flour','craft','processed',S50,50,110,180,2,[],['grain'],'necessity',['food','grain'])
g('bread','Bread loaf','craft','processed','loaf (1 lb)',1,3,3,2,[],['flour'],'necessity',['food'])
g('ale','Ale','craft','processed','cask (9 gal)',80,100,60,2,[],['barley','hops'],'ordinary',['drink'])
g('wine_common','Common wine','craft','processed','cask (9 gal)',80,300,365,3,[],['grapes'],'ordinary',['drink'])
g('wine_fine','Fine wine','craft','processed','bottle',2,300,None,4,[],['grapes'],'luxury',['drink','fine'])
g('cloth_wool','Wool cloth','craft','processed','sq yd',1,40,None,3,[],['wool_raw'],'ordinary',['cloth'])
g('cloth_linen','Linen cloth','craft','processed','sq yd',0.5,120,None,3,[],['flax'],'ordinary',['cloth'])
g('cloth_canvas','Canvas','craft','processed','sq yd',1,12,None,2,[],['flax'],'ordinary',['cloth','heavy'])
g('broadcloth_fine','Fine dyed wool','craft','processed','sq yd',1.5,260,None,4,[],['cloth_wool','dye_common'],'luxury',['cloth','fine'])
g('yarn','Yarn','craft','processed','lb',1,25,None,2,[],['wool_raw'],'ordinary',['fiber'])
g('rope','Hemp rope (50 ft)','craft','processed','each',10,80,None,2,[],['flax'],'ordinary',['cordage'])
g('leather','Tanned leather','craft','processed','hide',15,250,None,3,[],['hide_raw','tanning_bark'],'ordinary',['leather'])
g('iron_bar','Iron bar','craft','processed','lb',1,10,None,3,[],['iron_ore','charcoal'],'ordinary',['metal'])
g('steel_bar','Steel bar','craft','processed','lb',1,45,None,4,[],['iron_bar','charcoal'],'ordinary',['metal','fine'])
g('copper_bar','Copper ingot','craft','processed','lb',1,50,None,3,[],['copper_ore','charcoal'],'ordinary',['metal'])
g('bronze_ingot','Bronze ingot','craft','processed','lb',1,70,None,3,[],['copper_bar','tin_ore'],'ordinary',['metal'])
g('silver_bar','Silver bar','craft','processed','lb',1,500,None,3,[],['silver_ore','charcoal'],'luxury',['metal','precious'])
g('gold_bar','Gold bar','craft','processed','lb',1,5000,None,4,[],[],'luxury',['metal','precious'])
g('nails','Nails','craft','processed','lb',1,12,None,3,[],['iron_bar'],'ordinary',['hardware'])
g('tools_basic','Hand tool (hoe, axe, hammer)','craft','processed','each',3,150,None,3,[],['iron_bar','lumber_rough'],'ordinary',['tool'])
g('pottery','Earthenware pottery','craft','processed','dozen pieces',12,60,None,2,[],['clay','firewood'],'ordinary',['household'])
g('bricks','Fired brick','craft','processed','hundred',500,300,None,2,[],['clay','firewood'],'ordinary',['building'])
g('candles_tallow','Tallow candles','craft','processed','dozen',2,12,None,2,[],['tallow'],'ordinary',['lighting'])
g('candles_wax','Beeswax candles','craft','processed','dozen',2,90,None,3,[],['beeswax'],'ordinary',['lighting'])
g('soap','Soap','craft','processed','lb',1,10,None,2,[],['tallow'],'ordinary',['household'])
g('lamp_oil','Lamp oil','craft','processed','flask',1,8,None,2,[],['fish_oil'],'ordinary',['lighting'])
g('barrel_empty','Barrel, empty','craft','processed','each',40,120,None,3,[],['lumber_rough','iron_bar'],'ordinary',['container'])
g('dye_common','Common dye','craft','processed','lb',1,60,None,3,[],['dye_plants'],'ordinary',['dye'])
# ---- LUXURY / IMPORTS
g('spice_ginger','Root spice (ginger type)','trade','luxury','lb',1,90,None,3,[],[],'luxury',['spice'])
g('spice_pepper','Hot spice (pepper type)','trade','luxury','lb',1,180,None,3,[],[],'luxury',['spice'])
g('spice_cinnamon','Bark spice (cinnamon type)','trade','luxury','lb',1,230,None,3,[],[],'luxury',['spice'])
g('spice_cloves','Bud spice (clove type)','trade','luxury','lb',1,340,None,3,[],[],'luxury',['spice'])
g('spice_saffron','Thread spice (saffron type)','trade','luxury','lb',1,1600,None,4,[],[],'luxury',['spice','fine'])
g('silk','Silk','trade','luxury','sq yd',0.3,900,None,4,[],[],'luxury',['cloth','fine'])
g('incense','Incense','trade','luxury','lb',1,300,None,3,[],[],'luxury',['ritual'])
g('perfume','Perfume oil','trade','luxury','vial (1 oz)',0.1,500,None,4,[],[],'luxury',['fine'])
g('sugar','Sugar','trade','luxury','lb',1,60,None,3,[],[],'luxury',['food','sweetener'])
g('ivory','Tusk ivory','trade','luxury','lb',1,350,None,3,[],[],'luxury',['fine','craft material'])
g('book','Bound hand-copied book','trade','luxury','each',3,2500,None,5,[],[],'luxury',['fine','knowledge'])
g('jewelry_silver','Silver jewelry','trade','luxury','piece',0.2,1500,None,4,[],['silver_bar'],'luxury',['fine','jewelry'])
g('jewelry_gold','Gold jewelry','trade','luxury','piece',0.2,6000,None,5,[],['gold_bar'],'luxury',['fine','jewelry'])
g('tapestry','Tapestry','trade','luxury','each',25,5000,None,5,[],['cloth_wool','dye_fine'],'luxury',['fine','cloth'])
g('dye_fine','Fine dye (deep crimson type)','trade','luxury','oz',0.0625,350,None,4,[],[],'luxury',['dye','fine'])
g('gem_cut_common','Cut semi-precious stone','trade','luxury','each',0.01,800,None,4,[],['gems_rough'],'luxury',['gem'])
g('gem_cut_fine','Cut precious stone','trade','luxury','each',0.01,6000,None,5,[],['gems_rough'],'luxury',['gem'])
# ---- FANTASTICAL (invented names; the GM can rename)
g('glowmoss','Glowmoss (cold-light lichen)','fantastic','fantastic','lb',1,60,60,3,['quarries'],[],'luxury',['magic','lighting'],1)
g('emberstone','Emberstone (heat-holding rock)','fantastic','fantastic','lb',1,150,None,3,['mines'],[],'luxury',['magic','fuel'],1)
g('skyfall_iron','Skyfall iron (meteoric metal)','fantastic','fantastic','lb',1,600,None,4,['mines'],[],'luxury',['magic','metal'],2)
g('whisperwool','Whisperwool (sound-dampening wool)','fantastic','fantastic','lb',1,200,None,3,['husbandry'],[],'luxury',['magic','fiber'],2)
g('dreamroot','Dreamroot (sleep herb)','fantastic','fantastic','oz',0.0625,100,30,3,['farms'],[],'luxury',['magic','medicine'],1)
g('stormglass','Stormglass (weather-reactive crystal)','fantastic','fantastic','oz',0.0625,500,None,4,['mines'],[],'luxury',['magic','gem'],2)
g('beast_hide','Great-beast hide','fantastic','fantastic','each',60,3000,None,4,['game'],[],'luxury',['magic','hide'],3)
g('beast_bone','Great-beast bone','fantastic','fantastic','lb',1,300,None,4,['game'],[],'luxury',['magic','bone'],3)
g('wellspring_water','Wellspring water (blessed spring)','fantastic','fantastic','vial',0.5,800,None,3,[],[],'luxury',['magic','ritual'],2)
g('shimmerdust','Shimmerdust (glittering powder)','fantastic','fantastic','oz',0.0625,400,None,4,['mines'],[],'luxury',['magic','dye'],2)

# ---- validation
ids=[x['id'] for x in goods]
assert len(ids)==len(set(ids)), 'duplicate ids'
idset=set(ids); problems=[]
byid={x['id']:x for x in goods}
for x in goods:
    assert isinstance(x['baseValue'],int) and x['baseValue']>0, x['id']
    assert x['weightLb']>0, x['id']
    for i in x['inputs']:
        if i not in idset: problems.append("%s: unknown input %s" % (x['id'], i))
    if x['inputs']:
        a=byid[x['inputs'][0]]
        dens=lambda z: z['baseValue']/z['weightLb']
        if dens(x) < dens(a):
            problems.append("WARN %s (%.2f/lb) cheaper per lb than first input %s (%.2f/lb)" % (x['id'],dens(x),a['id'],dens(a)))
for a in ANCHOR:
    assert a in idset, a

header = {
 "schemaVersion": 1,
 "pack": "own",
 "title": "Purveyor's Broadsheet - own goods list",
 "status": "draft 0.1; every value is a first guess to tune",
 "moneyUnit": "Values are whole numbers in base units. Suggested presets: 10 base units = 1 silver-style coin, 100 = 1 gold-style coin. The GM names the coins.",
 "calibration": "Goods with an anchoredTo field were priced against the SRD 5.1 Trade Goods table (see srd-5.1-trade-goods.json). The app must show the SRD 5.1 attribution whenever any such good is enabled.",
 "fields": {
   "group": "Where it comes from: a resource, craft, trade or fantastic.",
   "category": "raw, processed, luxury or fantastic.",
   "unit": "What baseValue is quoted per.",
   "weightLb": "Weight of one unit, in pounds; drives transport cost.",
   "perishableDays": "Days until it spoils, or null.",
   "tier": "1-5: how skilled a maker and how large a market it needs.",
   "resources": "Resource checkboxes that can supply it.",
   "inputs": "Goods used to make it.",
   "demand": "necessity, ordinary or luxury: how strongly demand reacts to price and income.",
   "magicTier": "Fantastic goods only: 1 common, 2 fine, 3 rare, 4 marvelous.",
   "source": "own, or own plus srd-5.1 when priced against an SRD anchor."
 },
 "resourceKeys": ["mines","quarries","farms","fisheries","game","timber","husbandry"],
 "goods": goods,
}
with open(os.path.join(OUT,'goods.own.json'),'w',encoding='utf-8') as f:
    json.dump(header,f,indent=2,ensure_ascii=False); f.write('\n')

# ---- SRD 5.1 pack (Trade Goods table, SRD 5.1 p. 72): cp=1, sp=10, gp=100
srd=[
 ('wheat','Wheat','lb','staples',1),('flour','Flour','lb','staples',2),('chicken','Chicken','each','livestock',2),
 ('salt','Salt','lb','staples',5),('iron','Iron','lb','metals',10),('canvas','Canvas','sq yd','cloth',10),
 ('copper','Copper','lb','metals',50),('cotton_cloth','Cotton cloth','sq yd','cloth',50),('ginger','Ginger','lb','spices',100),
 ('goat','Goat','each','livestock',100),('cinnamon','Cinnamon','lb','spices',200),('pepper','Pepper','lb','spices',200),
 ('sheep','Sheep','each','livestock',200),('cloves','Cloves','lb','spices',300),('pig','Pig','each','livestock',300),
 ('silver','Silver','lb','metals',500),('linen','Linen','sq yd','cloth',500),('silk','Silk','sq yd','cloth',1000),
 ('cow','Cow','each','livestock',1000),('saffron','Saffron','lb','spices',1500),('ox','Ox','each','livestock',1500),
 ('gold','Gold','lb','metals',5000),('platinum','Platinum','lb','metals',50000),
]
pack={
 "schemaVersion":1,"pack":"srd-5.1","title":"SRD 5.1 Trade Goods","license":"CC-BY-4.0",
 "sourcePage":"System Reference Document 5.1, Trade Goods table, p. 72",
 "attribution":"This work includes material taken from the System Reference Document 5.1 (“SRD 5.1”) by Wizards of the Coast LLC and available at https://dnd.wizards.com/resources/systems-reference-document. The SRD 5.1 is licensed under the Creative Commons Attribution 4.0 International License available at https://creativecommons.org/licenses/by/4.0/legalcode.",
 "moneyUnit":"Whole numbers in base units: 1 copper piece = 1, 1 silver piece = 10, 1 gold piece = 100.",
 "goods":[{"id":"srd51_"+i,"name":n,"unit":u,"group":gr,"category":"trade good","baseValue":v,"source":["srd-5.1"]} for i,n,u,gr,v in srd],
}
with open(os.path.join(OUT,'srd-5.1-trade-goods.json'),'w',encoding='utf-8') as f:
    json.dump(pack,f,indent=2,ensure_ascii=False); f.write('\n')

print("own goods:",len(goods),"| srd pack goods:",len(srd))
print("by category:",dict(collections.Counter(x['category'] for x in goods)))
print("by group:",dict(collections.Counter(x['group'] for x in goods)))
print("anchored to SRD 5.1:",sum(1 for x in goods if 'anchoredTo' in x))
print("problems:",problems if problems else "none")
d2=sorted(goods,key=lambda z:z['baseValue']/z['weightLb'])
print("lowest value/lb:",[(z['id'],round(z['baseValue']/z['weightLb'],2)) for z in d2[:5]])
print("highest value/lb:",[(z['id'],round(z['baseValue']/z['weightLb'])) for z in d2[-5:]])

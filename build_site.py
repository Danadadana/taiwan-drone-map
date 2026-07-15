# -*- coding: utf-8 -*-
"""組裝最終 HTML：companies_merged + geocode_cache + logo_pack + geojson → drone_map.html"""
import json, math, re

db = json.load(open('companies_merged.json'))
cache = json.load(open('geocode_cache.json'))
logos = json.load(open('logo_pack.json'))
geo = json.load(open('tw_county_simplified.geojson'))

addr2ll = {}
for v in cache.values():
    if v.get('lat') and v.get('addr'):
        addr2ll[v['addr']] = (v['lat'], v['lng'], v['precision'])

REGIONS = ['台北市','新北市','基隆市','桃園市','新竹市','新竹縣','苗栗縣','台中市','彰化縣','南投縣','雲林縣','嘉義市','嘉義縣','台南市','高雄市','屏東縣','宜蘭縣','花蓮縣','台東縣','澎湖縣','金門縣','連江縣']
def region_of(addr):
    if not addr:
        return None
    a = str(addr).replace('臺', '台')
    a = re.sub(r'^(新竹科學園區|新竹科學工業園區|中部科學園區|南部科學園區|南部科學工業園區|科學園區)', '', a)
    for rg in REGIONS:
        if a.startswith(rg):
            return rg
    return None

companies = []
for k, r in db.items():
    ll = addr2ll.get(r.get('address') or '')
    c = {
        'n': r['nameZh'],
        'r': r['roles'],
        'a': r['apps'],
        'f': r['flags'],
        'sp': r['special'],
        'addr': None if (r.get('address') or '').strip() == '暫不提供' else r.get('address'),
        'lat': round(ll[0], 5) if ll else None,
        'lng': round(ll[1], 5) if ll else None,
        'w': r.get('website'),
        'u': r.get('url104'),
        'j': r.get('jobCount') or 0,
        'p': re.sub(r'\s+', ' ', r.get('profile') or '')[:220],
        'lg': r.get('logo') if r.get('logo') in logos else None,
        'cap': None if (r.get('capital') or '').strip() == '暫不提供' else r.get('capital'),
        'emp': None if (r.get('empNo') or '').strip() == '暫不提供' else r.get('empNo'),
        'ind': r.get('industry'),
        'src': r.get('sources', []),
        'rg': region_of(r.get('address')),
    }
    companies.append(c)

# 抖動：同座標的公司散成小圓環
groups = {}
for c in companies:
    if c['lat'] is None:
        continue
    key = (round(c['lat'], 4), round(c['lng'], 4))
    groups.setdefault(key, []).append(c)
for key, items in groups.items():
    if len(items) < 2:
        continue
    n = len(items)
    rad = 0.0022 * (1 + n / 14)
    for idx, c in enumerate(items):
        ang = 2 * math.pi * idx / n
        c['lat'] = round(c['lat'] + rad * math.sin(ang), 5)
        c['lng'] = round(c['lng'] + rad * math.cos(ang) / 0.9163, 5)

companies.sort(key=lambda c: (c['sp'] or '', c['n']))
for i, c in enumerate(companies):
    c['i'] = i

# 瘦身 geojson properties
for f in geo['features']:
    f['properties'] = {'name': f['properties'].get('name') or f['properties'].get('COUNTYNAME', '')}

tpl = open('site_template.html', encoding='utf-8').read()
out = tpl.replace('/*__DATA__*/[]', json.dumps(companies, ensure_ascii=False, separators=(',', ':')))
out = out.replace('/*__GEO__*/{}', json.dumps(geo, ensure_ascii=False, separators=(',', ':')))
out = out.replace('/*__LOGOS__*/{}', json.dumps(logos, separators=(',', ':')))
policy = json.load(open('policy_timeline.json'))
out = out.replace('/*__POLICY__*/{"updated":"","industry":[],"defense":[]}', json.dumps(policy, ensure_ascii=False, separators=(',', ':')))
open('drone_map.html', 'w', encoding='utf-8').write(out)

withll = sum(1 for c in companies if c['lat'])
print(f'companies {len(companies)} | with coords {withll} | html KB {len(out.encode())//1024}')

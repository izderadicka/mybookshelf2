from cli.action import Action
from time import time


class Test(Action):
    
    def do(self):
        print("Request to API")
        resp = self.http.get('/api/ebooks', params={'page':1,'page_size':10})
        data = resp.json()
        print("Got %d ebooks of %d"% (len(data['items']), data['total']))
        print("Calling remote method sleep 1")
        now =time()
        res=self.client.call('sleep',1)
        print("Done result is %s took %f"%(res['result'], time()-now))
        print("Calling remote method date")
        now=time()
        res=self.client.call('date', '%d-%m-%Y %H:%M %Z')
        print("Done result is %s took %f"%(res['result'], time()-now))
        
        print("Calling remote method sleep 1 with no_wait")
        now =time()
        res=self.client.call_no_wait('sleep',1)
        print("Done task id is is %s took %f"%(res, time()-now))
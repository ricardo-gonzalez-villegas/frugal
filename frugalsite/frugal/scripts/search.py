from .meijer import search_on_meijer
from .kroger import search_on_kroger
from .walmart import search_on_walmart
import threading
 
class SearchThread():
    def __init__(self, request) -> None:
        self.product = request.GET["search"]
        self.meijer = bool(request.GET.get("meijer", False))
        self.kroger = bool(request.GET.get("kroger", False))
        self.walmart = bool(request.GET.get("walmart", False))
        self.results = dict()
        self.run()
        
    def meijer_search(self) -> None:
        self.results["meijer"] = search_on_meijer(self.product)
    
    def kroger_search(self) -> None:
        self.results["kroger"] = search_on_kroger(self.product)
        
    def walmart_search(self) -> None:
        self.results["walmart"] = search_on_walmart(self.product)
    
    def run(self):
        threads = list()
        if self.meijer:
            thread = threading.Thread(target=self.meijer_search)
            thread.start()
            threads.append(thread)
        
        if self.kroger:
            thread = threading.Thread(target=self.kroger_search)
            thread.start()
            threads.append(thread)
        
        if self.walmart:
            thread = threading.Thread(target=self.walmart_search)
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
            
    def get_results(self) -> dict:
        return self.results
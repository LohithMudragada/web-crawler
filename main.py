import cfg
import myspyder
import time
import threading


spy = myspyder.spyder()
visited = 0
table = spy.connectDb()

class myThread (threading.Thread):
   def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        obj = table.find_one({"Link":cfg.source})
        if obj is None:
            obj = {
                "Link":cfg.source,
                "SourceLink":"",
                "IsCrawled":False,
                "LastCrawlDate":None,
                "ResponseStatus":None,
                "Contenttype":None,
                "ContentLength": None,
                "Filepath":"",
                "CreatedDate":myspyder.datetime.datetime.utcnow()
            }
            table.insert_one(obj).inserted_id
        self.obj = obj
        
   def run(self):
        while True:
            try:
                global visited
                spy.getlinks(self.obj,table)
                threadLock.acquire()
                self.obj = spy.getnextlink(table)
                print("Visited : ",visited, "visiting : ",self.obj['Link'])
                visited+=1
                if visited == cfg.maxLinks or self.obj is None:
                    time.sleep(cfg.sleep)
                    visited=0
                    self.obj = table.find_one({'Link':cfg.source})
                    print("Crawled Successfully!!")
                threadLock.release()
            except Exception as inst:
                print(inst)
                pass



threadLock = threading.Lock()
threads = []
# Create new threads
thread1 = myThread(1)
thread2 = myThread(2)
thread3 = myThread(3)
thread4 = myThread(4)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()

# Add threads to thread list
threads.append(thread1)
threads.append(thread2)
threads.append(thread3)
threads.append(thread4)

# Wait for all threads to complete
for t in threads:
    t.join()
print("Exiting Main Thread")

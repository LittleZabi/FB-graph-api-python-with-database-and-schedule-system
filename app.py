from datetime import datetime
from facebook_api import FACEBOOK
import schedule
import time
from db import SQL
import os


class App:
    def __init__(self):
        self.db = SQL()
        self.fb = FACEBOOK()

    def __id__(self, post_id):
        try:
            return int(post_id['id'].split('_')[1])
        except:
            return int(post_id['post_id'].split('_')[1])

    def checkIsFile(self, paths):
        for path in paths:
            if os.path.isfile(path):
                return path
        return False

    def sharePost(self):
        print('Posting Terminal is blasting now!')
        posts = self.getTodayPost()
        for post in posts:
            print('Posting... id: ', post[0])
            try:
                id_ = post[0]
                type_ = post[1]
                source_ = post[2]
                cap = post[3]
                pid = 0
                if type_ == 'text':
                    post_id = self.fb.post_text(message=source_)
                    self.db.posted(id_, post_id=self.__id__(post_id))
                    print(f'Successfully posted: \n source -> {source_}')
                elif type_ == 'image':
                    image = self.checkIsFile([source_, cap])
                    if image == False:
                        image = source_
                    post_id = self.fb.postImage(image, caption=cap)
                    self.db.posted(id_, post_id=self.__id__(post_id))
                    print(f'Successfully posted: \n source -> {source_}')
                elif type_ == 'link':
                    post_id = self.fb.addLink(source_, message=cap)
                    self.db.posted(id_, post_id=self.__id__(post_id))
                    print(f'Successfully posted: \n source -> {source_}')
                else:
                    print(
                        'unknown type of post only support(text, image, link) current type is: ', type_)
            except Exception as e:
                print("Error -> sharePost post: ", post, e)
        print('done!')

    def getTodayPost(self):
        return self.db.getByDate(self.getDate(date=False))

    def getDate(self, date=False):
        """
            get Date take date parameter if its false then its return today date
            Enter date format like dd/mm/yyyy
        """
        if date == False:
            return datetime.now().strftime("%Y-%m-%d 00:00:00")
        d = date.split('/')[0]
        m = date.split('/')[1]
        y = date.split('/')[2]
        return datetime(int(y), int(m), int(d)).strftime("%d/%m/%Y")

    def compareToToday(self, date):
        now = datetime.now()
        today = now.strftime("%d/%m/%Y")
        post_date = self.getDate(date)
        return {
            'isEqual': post_date == today,
            'isGreater': post_date > today,
            'isLess': post_date < today,
        }

    def startReactor(self):
        print('Reactor is started.... :)')
        schedule.every().day.at('12:00').do(self.sharePost)
        # schedule.every().minute.do(self.sharePost)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    app = App()
    # c = app.sharePost()
    app.startReactor()

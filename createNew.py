from db import SQL
from datetime import datetime


class CreateNew:
    def __init__(self):
        self.db = SQL()
        print("""
create new post
1 - new
2 - get post
3 - help
        """)
        option = str(input('Enter Option number: '))
        if option == '1':
            self.new()
        elif option == '2':
            self.get()
        else:
            with open('./guid.txt', 'r') as file:
                print(file.read())
                self.__init__()

        pass

    def getPost(self, id):
        self.db.getPost(id)

    def createDate(self, date):
        """ 
        Date format dd/mm/yyyy
        like 05/09/2022
        """
        d = date.split('/')[0]
        m = date.split('/')[1]
        y = date.split('/')[2]
        date = datetime(int(y), int(m), int(d))
        return date

    def new(self):
        type_ = self.getInput(
            'Enter post type(link, image, text): ', required=True)
        source_ = self.getInput(
            'Enter post source(link, image path or message): ', required=True)
        caption_ = self.getInput(
            'Enter post caption(only work on link and image): ', required=False)
        post_on_ = self.getInput(
            'Enter post schedule time(dd/mm/yyyy or empty for now): ', required=False)
        if post_on_ == '':
            post_on_ = datetime.now().strftime('%Y-%m-%d 00:00:00')
        else:
            post_on_ = self.createDate(post_on_)

        self.db.newPost(type=type_, source=source_,
                        caption=caption_, post_on=post_on_)
        self.db.close()

    def getInput(self, placeholder, required=False):
        if required:
            while True:
                t = str(input(placeholder))
                if t != '':
                    return t
                else:
                    print('Input is empty. This is required!')

        return str(input(placeholder))


if __name__ == '__main__':
    CreateNew()

import csv
import facebook as fb
import requests
import json
from pathlib import Path


class FACEBOOK:
    def __init__(self, setOutPutFilename='./posted-posts.csv'):
        self.token = self.readCredentials(self.credentialFile())
        self.fb = fb.GraphAPI(self.token['access_token'])
        self.output_filename = setOutPutFilename
        self.write_posted_ids = False

    def credentialFile(self):
        filename = './credentials.json'
        if Path(filename).is_file():
            return filename
        print('Your credentials file is not located')
        print('Please enter the full path of your credentials.json file')
        filename = input('Enter credentials file paht: ')
        return filename

    def readCredentials(self, file):
        '''
        Store API credentials in a safe place.
        If you use Git, make sure to add the file to .gitignore
        '''
        with open(file) as f:
            credentials = json.load(f)
        return credentials

    def post_text(self,  message, pObject='me', location='feed'):
        if message == '':
            return 'Message is empty!'
        post_id = self.fb.put_object(pObject, location, message=message)
        self.write(text=message, id=post_id['id'])
        return post_id

    def write(self, start='text', text='', id='', end=' '):
        with open(self.output_filename, 'a') as file:
            file.write(f'{start}, {id}, {text}, {end}\n')

    def deleteObject(self, post_id):
        """
            Deletes the object with the given ID from the graph.
            Note: only works on API version v2.4 and less
            return Object
        """
        return self.fb.delete_object(post_id)

    def addLink(self, link, message=''):
        """
            Add a link and write a message about it.
            return object
        """
        c = self.fb.put_object(
            parent_object='me', connection_name='feed', message=message, link=link)
        if self.write_posted_ids:
            self.write(start='Link', text=message, id=c['id'], end=link)
        return c

    def likePost(self, post_id):
        """
            Writes a like to the given object.
            Note: only works on API version v2.4 and less
            return Object
        """
        return self.fb.put_like(object_id=post_id)

    def getPost(self, id):
        return self.fb.get_object(id)

    def postImage(self, image, caption=''):
        try:
            post_id = self.fb.put_photo(open(image, 'rb'), message=caption)
            if self.write_posted_ids:
                self.write(start='image', text=image, id=post_id['id'])
            return post_id
        except Exception as e:
            print('PostImage Error: ', e)
    # def postVideo(self, video, title='', description=''):
    #     try:
    #         self.fb.video

    def commentOnPost(self, id, message):
        try:
            post_id = self.fb.put_object(id, 'comments', message=message)
            if self.write_posted_ids:
                self.write(start='comment', text=message,
                           id=post_id['id'], end='post: '+id)
            return post_id
        except Exception as e:
            print('CommentOnPost: Error ', e)

    def fanCount(self, page_id):
        url = f'https://graph.facebook.com/{page_id}?fields=fan_count&access_token={self.token}'
        o = requests.get(url).json()
        print(o)
        return o

    def getFriends(self):
        """
            Get active friends
            return Object
        """
        c = self.fb.get_connections(id='me', connection_name='friends')
        return c

    def getComments(self, post_id):
        """
            Get comments on a post
            return Object
        """
        c = self.fb.get_connections(id=post_id, connection_name='comments')
        return c

    def searchPlaces(self, center='37.4845306,-122.1498183', fields='name,location'):
        """
            search for places near (the latitude and longitude)
            only work on API version 8.0 and less
            return Array
        """
        return self.fb.search(type='place', center=center, fields=fields)

    def getPostsTime(self, posts_id=[]):
        """
            Get the time two different posts were created
            only work on API version 2.4 and less
            return Array
        """
        return self.fb.get_objects(ids=posts_id, fields='created_time')


# post = FACEBOOK()
# post.post_text(messages=['test message 1', 'test message 2'])
# print(Post(access_token).getPost('108772264386266_449491797235139'))
# post.postImage(image='F:\pexels-pixabay-2156.jpg',
#                caption='Life on the BlueSky [Test post]')
# print(post.commentOnPost('449498603901125', 'Here test comment'))
# print(post.getComments(post_id='449498603901125'))
# print(post.addLink('https://youtube.com', 'this is a test link!'))
# print(post.likePost('449788647205454'))
# print(post.postToAllGroups(message="Subscribe Blueterminal for coding and Best UI's!", groups=['1211645802304086', '1465824016974338'],
#       link='https://www.youtube.com/channel/UCMJTfB8cZLxjvUht3o0E3qQ'))


# def readCsv():
#     with open("./posts.csv", 'r') as file:
#         csvreader = csv.reader(file)
#         for row in csvreader:
#             print(row)


# readCsv()

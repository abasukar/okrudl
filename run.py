from requests import get
import re,html,json,os,sys,argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--link", help="link to streaming video", type=str, required = True)
parser.add_argument("-o", "--output_dir", help="path to store the downloaded file", type=str, default = "/mnt/500apple/finished")
parser.add_argument("-f", "--file_name", help="how to name your file (without mp4 extension)", type=str, required = True)
args = parser.parse_args()

dir = args.output_dir

class OkRuDl:
    def __init__(self,video_url,user_title):
        self.url = video_url
    def sizes(self,size):
        for x in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0
        return size
    def getb(self,frame_url,title):
        x = get(frame_url)
        xx = open(f"{dir}/{title}.mp4","ab")
        xx.write(x.content)
        return x.content
    @property
    def download(self):
            bb = bytearray()
            r = get(self.url,headers={"User-agent":"Mozilla/5.0 (Linux; Android 9; Redmi Note 5A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36"})
            v = re.search(r'data\-video\=\"(.*?)\"',r.text).group(1)
            data = json.loads(html.unescape(v))
            video_title = user_title.replace(" ","_").replace(".","_").replace("/","_")
            print(f"\nPreparing to download \033[92m{video_title}\033[0m")
            url = data["videoSrc"]
            v = get(url,headers={"User-agent":"Mozilla/5.0 (Linux; Android 9; Redmi Note 5A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36"})

            w = re.findall(r'http[s]:\/\/.*?\/video\/',v.text)
            x = get(w[0]).text

            y = re.findall(r'[(LOWEST)|(MEDIUM)|(HIGH)].*?.ts',x) # list of *.ts files in playlist
            frames = []
            print("target folder content:")
            print(str(os.listdir(dir)))
            x = os.popen("df -h | grep -e Size -e 500")
            print("available space in system:")
            print(x.read())
            print("Starting..")
            for frame in y:
                b = self.getb(w[0]+frame,video_title)
                bb += b
                frames.append(frame)
                print(f"\rDownloading progres: \033[92m{round((len(frames)/len(y))*100)}%\033[0m [\033[92m{self.sizes(len(bb))}\033[0m]..",end="",flush=True)

            print(f"\nVideo successfully downloaded.\nVideo saved to \033[92m{dir}/{video_title}.mp4\033[0m\nFor other program : \033[92mhttps://karjokpangesty.blogspot.com\033[0m")
            print("target folder content:" + str(os.listdir(dir)))
if __name__=='__main__':
    os.system("clear")
    print(f"""\033[0m
           _
      ___ | | __  _ __ _   _
     / _ \| |/ / | '__| | | |
    | (_) |   < _| |  | |_| |
     \___/|_|\_(_)_|   \__,_|
\033[92mVideo Downloader \033[0m|\033[92m Karjok Pangesty\033[0m

""")
    urlz = args.link
#    urlz = re.search("http[s]\:\/\/[m\.]+ok\.ru",url)
    user_title = args.file_name
    if urlz:
        ok = OkRuDl(urlz,user_title)
        ok.download
    else:
        print("Invalid URL!")

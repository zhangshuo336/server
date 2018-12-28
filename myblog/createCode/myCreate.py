#coding: utf-8
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os,string,random
def initChars():
    nums = [str(i) for i in range(2,10)]
    letterCase = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z'
    ]
    upperCase = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
    'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
    'W', 'X', 'Y', 'Z',
    ]
    return(nums+letterCase+upperCase)
class picChecker():

        #DEFAULT_FONT_PATH = os.path.join(os.path.dirname(__file__),'simsun.ttc').replace('\\','/')
    def __init__(self,chars = initChars(),size = (91,38),fontsize = 18,
        begin = (1,3),outputType = 'PNG',mode = 'RGB' ,
        backgroundColor = (random.randint(100,255),random.randint(100,255),random.randint(100,255)),
                 foregroundColor = (random.randint(0,200),random.randint(0,200),random.randint(0,200)),
        fonttype = "DejaVuSans-Bold.ttf",length = 4,jamNum = (2,2),
        pointBorder = (50,51)):

        #验证码配置
        #允许的字符串
        self.chars = chars
        #图片大小
        self.size = size
        #字符起始插入点
        self.begin = begin
        #字符串长度
        self.length = length
        #输出类型
        self.outputType = outputType
        #字符大小
        self.fontsize = fontsize
        #图片模式
        self.mode = mode
        #背景色
        self.backgroundColor = backgroundColor
        #前景色
        self.foregroundColor = foregroundColor
        #干扰线条数
        self.jamNum = jamNum
        #散点噪音界限
        self.pointBorder = pointBorder
        #字体库路径
        self.fonttype = fonttype
        #设置字体,大小默认为18
        self.font = ImageFont.truetype(self.fonttype, self.fontsize)
    def getPicString(self):

        #初始化字符串长度
        length = self.length
        #初始化字符集合
        chars = self.chars
        #获得字符集合
        selectedChars = random.sample(chars,length)
        charsToStr = string.join(selectedChars,'')
        return(charsToStr)
    def createJam(self,draw):

        #干扰线条数
        lineNum = random.randint(self.jamNum[0],self.jamNum[1])
        for i in range(lineNum):
            begin = (random.randint(0,self.size[0]),random.randint(0,self.size[1]))
            end = (random.randint(0,self.size[0]),random.randint(0,self.size[1]))
            draw.line([begin,end],fill = (0,0,0))
    def createPoints(self,draw):

        #散点噪音
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                flag = random.randint(0,self.pointBorder[0])
                if flag > self.pointBorder[1]:
                    draw.point((x,y),fill = (0,0,0))
                del flag
    def createChecker(self):

        #获得验证码字符串
        randStr = self.getPicString()
        #将字符串加入空格
        randStr1 = string.join([i+" " for i in randStr],"")
        #创建图形
        im = Image.new(self.mode,self.size,self.backgroundColor)
        #创建画笔
        draw = ImageDraw.Draw(im)
        #输出随机文本
        draw.text(self.begin, randStr1, font=self.font,fill=self.foregroundColor)
        #im = self.drawText(draw,randStr,im)
        #干扰线
        self.createJam(draw)
        #散点噪音
        self.createPoints(draw)
        #图形扭曲
        para = [1-float(random.randint(1,2))/100,
        0,
        0,
        0,
        1-float(random.randint(1,10))/100,
        float(random.randint(1,2))/500,
        0.001,
        float(random.randint(1,2))/500
        ]
        #print randStr,para
        im = im.transform(im.size, Image.PERSPECTIVE,para)
        #图像滤镜
        im=im.filter(ImageFilter.EDGE_ENHANCE_MORE)
        return ([randStr,im])
if __name__ == '__main__':
    c = picChecker()
    t = c.createChecker()
    with open('./picaaa.txt','a')as f:
        f.write(t[0])
        f.write(t[1])
    print t


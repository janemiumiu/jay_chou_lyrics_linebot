#coding:utf-8
import re
from transitions.extensions import GraphMachine
from utils import send_button_message
from utils import send_text_message
import random
from linebot.models import MessageEvent, TextMessage, TextSendMessage ,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction
album_and_song_dict={"Jay":["可愛女人","完美主義","星晴","娘子","鬥牛","黑色幽默","伊斯坦堡","印第安老斑鳩","龍捲風","反方向的鐘"],"范特西":["愛在西元前","爸 我回來了","簡單愛","忍者","開不了口","上海 一九四三","對不起","威廉古堡","雙節棍","安靜"],"八度空間":["半獸人","半島鐵盒","暗號","龍拳","火車叨位去","分裂","爺爺泡的茶","回到過去","米蘭的小鐵匠","最後的戰役"],"葉惠美":["以父之名","懦夫","晴天","三年二班","東風破","妳聽得到","同一種調調","她的睫毛","愛情懸崖","梯田","雙刀"],"七里香":["我的地盤","七里香","藉口","外婆","將軍","擱淺","亂舞春秋","困獸之鬥","園遊會","止戰之殤"],"11月的蕭邦":["夜曲","藍色風暴","髮如雪","黑色毛衣","四面楚歌","楓","浪漫手機","逆鱗","麥芽糖","珊瑚海","飄移","一路向北"],"依然范特西":["夜的第七章","聽媽媽的話","千里之外","本草綱目","退後","紅模仿","心雨","白色風車","迷迭香","菊花台","霍元甲"],"我很忙":["牛仔很忙","彩虹","青花瓷","陽光宅男","蒲公英的約定","無雙","我不配","扯","甜甜的","最長的電影"],"魔杰座":["龍戰騎士","給我一首歌的時間","蛇舞","花海","魔術先生","說好的幸福呢","蘭亭序","流浪詩人","時光機","喬克叔叔","稻香"],"跨時代":["跨時代","說了再見","煙花易冷","免費教學錄影帶","好久不見","雨下一整晚","嘻哈空姐","我落淚情緒零碎","愛的飛行日記","自導自演","超人不會飛"],"驚嘆號":["驚嘆號","迷魂曲","Mine Mine","公主病","你好嗎","療傷燒肉粽","琴傷","水手怕水","世界未末日","皮影戲","超跑女神"],"12新作":["四季列車","手語","公公偏頭痛","明明就","傻笑","比較大的大提琴","愛你沒差","紅塵客棧","夢想啟動","大笨鐘","哪裡都是你","烏克麗麗"],"哎呦，不錯喔":["陽明山","竊愛","算什麼男人","天涯過客","怎麼了","一口氣全唸對","我要夏天","手寫的從前","鞋子特大號","聽爸爸的話","美人魚","聽見下雨的聲音"],"周杰倫的床邊故事":["床邊故事","說走就走","一點點","前世情人","英雄","不該","土耳其冰淇淋","告白氣球","Now You See Me","愛情廢柴"],"范特西Plus":["蝸牛","你比從前快樂","世界末日"],"尋找周杰倫 EP":["軌跡","斷了的弦"],"霍元甲 EP":["霍元甲","獻世"],"黃金甲 EP":["黃金甲"]}
album_list=["Jay","范特西","八度空間","葉惠美","七里香","11月的蕭邦","依然范特西","我很忙","魔杰座","跨時代","驚嘆號","12新作","哎呦，不錯喔","周杰倫的床邊故事","范特西Plus","尋找周杰倫 EP","霍元甲 EP","黃金甲 EP"]
def is_song_exist(search_song):
    for album,songs in album_and_song_dict.items():
        for s in songs:
            if search_song == s:
                return True     
    return False
def is_album_exist(search):
    for a in album_list:
        if search == a:
            return True
    return False  
def find_album_by_song_name(search_song):
    for album,songs in album_and_song_dict.items():
        for s in songs:
            if search_song == s:
                target_album = album
                message= target_album  
                return message    
    message= "查無此歌曲，請重新輸入！"
    return message
def album_introdution(album):
    if album == "Jay":
        message = "《Jay》是周杰倫首張錄音室專輯，由台灣博德曼音樂於2000年11月7日發行。該專輯獲得第12屆台灣金曲獎最佳流行音樂演唱專輯獎與2001年IFPI香港唱片銷量大獎十大銷量國語唱片獎。歌曲《可愛女人》於Hit FM聯播網2000年度百首單曲位列74名。"
    elif album =="范特西":
        message = "《范特西》是周杰倫第二張錄音室專輯，由台灣博德曼音樂於2001年9月14日發行。專輯名《范特西》來自英文「Fantasy」音譯。"
    elif album =="八度空間":
        message="《八度空間》是周杰倫發行的第三張國語專輯。「八度空間」意味著1979年1月18日出生的杰倫可在西方八度音階的空間內，揮灑自如、遊刃有餘、創造驚奇、不按排理出牌的個性，讓人在既定的「八度框框」內，突破享受到無遠弗屆的異想世界；當大家在聆聽旋律之餘，閱讀「創作名筆」方文山瑰麗縝密的詞藻，更使聽眾像是觀賞第八藝術的「電影」般，就像是音樂領域中的第八藝術！"
    elif album =="葉惠美":
        messaget="《葉惠美》是周杰倫的第四張錄音室專輯，由台灣新力音樂於2003年7月31日發行。專輯名稱使用周杰倫母親「葉惠美」的名字作為專輯名，原因是周杰倫認為專輯主打歌叫《以父之名》，為了「平衡」就用了母親的名字作專輯名。"
    elif album =="七里香":
        message="《七里香》是台灣歌手周杰倫發行第五張國語專輯。由台灣新力音樂於2004年8月3日發行。"
    elif album =="11月的蕭邦":
        message = "《11月的蕭邦》是周杰倫發行第六張國語專輯，並於2005年10月19日至10月31日在多個地區預售。大碟中除收錄10首新曲外，還特別格外加收周杰倫為電影《頭文字D》創作及演唱的主題曲《飄移》及插曲《一路向北》一共12首。專輯取名自周杰倫最欣賞的音樂家蕭邦。"
    elif album == "依然范特西":
        message ="《依然范特西》是周杰倫的第七張專輯，由阿爾發音樂製作，由新力音樂於2006年9月5日代理發行。專輯原定於同年9月8日發行，惟母帶被洩漏而提前3日至9月5日發行。取名靈感來自於周杰倫於2001年發行第2張專輯《范特西》，范特西來自於英文Fantasy的音譯，意即想像、幻想。而《依然范特西》專輯預購宣傳廣告語為：「想像依然無限大，感覺依然說不完，音樂依然范特西 。」"
    elif album =="我很忙":
        message = "《我很忙》是周杰倫發行第八張國語專輯，總全台銷售量十二萬張。《我很忙》是周杰倫在自己組建的杰威爾音樂發行的首張個人專輯，專輯中周杰倫在保留自己風格的同時力求突破，走美國西部牛仔風的主打歌《牛仔很忙》、男兒勵志歌曲《陽光宅男》、可愛甜美的《甜甜的》無不體現出這點。每張專輯必有的中國風歌曲此次是到達新的程度，歌曲《青花瓷》在推出之後迅速竄紅，成為繼《髮如雪》、《菊花台》之後的經典歌曲。2014年的美國喜劇電影《採訪》在影片中曾使用《牛仔很忙》作為電影背景音樂，《陽光宅男》亦為電影《愛情無全順》主題曲。"
    elif album =="魔杰座":
        message = "《魔杰座》是周杰倫發行第九張國語專輯。《魔杰座》的名稱來源於周杰倫的星座摩羯座，本張專輯以「撲克牌」作為專輯主題，周杰倫化身成魔術師與小丑。其中主打歌《稻香》率先於9月22日各大電台播放。《魔杰座》未能逃脫以往專輯遭洩露的命運，所有曲目在官方發行之前被網站提前洩密曝光。因此本應在10月9日發行的《魔杰座》被唱片公司推遲到10月14日發行。"
    elif album =="跨時代":
        message ="《跨時代》是周杰倫發行第十張國語專輯。也是首度打破一年發行一張專輯慣例的專輯，首支主打歌是《超人不會飛》。整張專輯11首歌曲皆拍攝成MV。"
    elif album =="驚嘆號":
        message="《驚嘆號》是周杰倫發行第十一張國語專輯。首支主打歌是《驚嘆號》。而周杰倫還是按照慣常，整張專輯11首歌曲都會拍攝成音樂影片。"
    elif album =="12新作":
        message ="《12新作》是周杰倫的第十二張錄音室專輯，收錄12首歌曲，2012年12月12日開始預購，12月28日發行，發行3天的時間就成為五大唱片2012年年榜第5名。2013年，專輯入圍第24屆金曲獎「最佳國語專輯獎」，周杰倫憑藉這張專輯入圍「最佳專輯製作人獎」以及「最佳國語男歌手獎」，黃雨勛憑藉收錄於這張專輯中的歌曲《比較大的大提琴》入圍「最佳編曲人獎」。"
    elif album=="哎呦，不錯哦":
        message ="《哎呦，不錯哦》是周杰倫的第十三張錄音室專輯，2014年12月10日開始預購，12月26日正式發行。專輯名稱來自於周杰倫本人的口頭禪。"
    elif album =="周杰倫的床邊故事":
        message ="《周杰倫的床邊故事》是周杰倫的第十四張錄音室專輯，2016年6月8日開始預購，6月24日正式發行。新專輯以床邊故事命名，專輯設計打造成有聲書概念，訴說10個與眾不同、充滿想像的音樂故事。專輯中與張惠妹首度合唱，是繼《依然范特西》專輯中的《千里之外》與費玉清的合作後，再次跨公司與線上歌手合唱，並且收錄於專輯中。"
    elif album =="范特西Plus":
        message ="《范特西Plus》是周杰倫的第1張迷你專輯，由博德曼音樂於2001年12月24日發行，收錄周杰倫在桃園巨蛋演唱會上，重新演唱吳宗憲的《你比從前快樂》、咻比嘟嘩的《世界末日》及許茹芸為世界展望會獻唱的《蝸牛》三首歌曲與MV，以及范特西專輯10首歌曲的MV。"
    elif album =="尋找周杰倫 EP":
        message ="《尋找周杰倫 EP》是周杰倫的第2張迷你專輯，由新力音樂於2003年11月1日發行，收錄了電影尋找周杰倫主題曲〈軌跡〉、〈斷了的弦〉，以及專輯《葉惠美》中的11首歌曲MV。專輯封面寫著的序號「vmp65l3 5. ru 6xjp6」是「尋找周杰倫」在鍵盤上的相對注音字符。"
    elif album =="霍元甲 EP":
        message ="《霍元甲 EP》是周杰倫的第3張迷你專輯，由阿爾發音樂於2006年1月20日發行，收錄了于仁泰導演、李連杰主演的電影《霍元甲》的同名主題曲《霍元甲》，以及2004年周杰倫於香港紅磡體育館舉行的「無與倫比演唱會」上演唱的粵語歌曲《獻世》的現場版本，這首歌是周杰倫在2003年寫給陳小春的，而DVD則收錄了《11月的蕭邦》12首歌曲的音樂影片。"
    elif album =="黃金甲 EP":
        message ="《黃金甲 EP》是台灣男歌手周杰倫的第4張迷你專輯，由台灣索尼音樂娛樂於2006年12月7日發行，收錄了張藝謀導演的電影《滿城盡帶黃金甲》的主題曲〈黃金甲〉，DVD收錄了《依然范特西》10首歌曲的音樂錄影帶。"
    else :
        message ="查無此專輯，請重新輸入！"
    return message
def find_all_songs_in_album(search):
    message=""
    for album,songs in album_and_song_dict.items():
        if search == album:
            for s in songs:
                message+=(s+" ") 
    return message

def recommand_song_by_album(album):
    if album == "Jay":
        message = "可愛女人 星晴 黑色幽默 龍捲風 反方向的鐘"
    elif album =="范特西":
        message = "愛在西元前 簡單愛 開不了口 安靜"
    elif album =="八度空間":
        message="半島鐵盒 暗號 爺爺泡的茶 回到過去 最後的戰役"
    elif album =="葉惠美":
        message="晴天 妳聽得到 她的睫毛 愛情懸崖"
    elif album =="七里香":
        message="七里香 擱淺 園遊會"
    elif album =="11月的蕭邦":
        message = "夜曲 髮如雪 楓 浪漫手機 麥芽糖 一路向北"
    elif album == "依然范特西":
        message ="聽媽媽的話 退後 心雨 白色風車"
    elif album =="我很忙":
        message = "牛仔很忙 彩虹 青花瓷 陽光宅男 我不配 甜甜的 最長的電影"
    elif album =="魔杰座":
        message = "給我一首歌的時間 花海 說好的幸福呢 時光機 稻香"
    elif album =="跨時代":
        message ="說了再見 雨下一整晚 我落淚情緒零碎 超人不會飛"
    elif album =="驚嘆號":
        message="Mine Mine 公主病 療傷燒肉粽 超跑女神"
    elif album =="12新作":
        message ="手語 明明就 傻笑 愛你沒差 夢想啟動 大笨鐘"
    elif album=="哎呦，不錯哦":
        message ="算什麼男人 天涯過客 怎麼了 手寫的從前 聽爸爸的話 美人魚"
    elif album =="周杰倫的床邊故事":
        message ="不該 告白氣球 愛情廢柴"
    elif album =="范特西Plus":
        message ="你比從前快樂"
    elif album =="尋找周杰倫 EP":
        message ="軌跡 斷了的弦"
    elif album =="霍元甲 EP":
        message ="霍元甲"
    elif album =="黃金甲 EP":
        message ="黃金甲"
    else :
        message ="查無此專輯，請重新輸入！" 
    return message   
def search_url(album):
    if album == "Jay":
        message = "https://cdn.shopify.com/s/files/1/1283/2797/products/500x500-3_580x.jpg?v=1465703750"
    elif album =="范特西":
        message = "https://upload.wikimedia.org/wikipedia/zh/8/87/Jay_2001_ablum_cover.jpg"
    elif album =="八度空間":
        message="https://upload.wikimedia.org/wikipedia/zh/thumb/4/4e/Jay_2002_ablum_cover.jpg/220px-Jay_2002_ablum_cover.jpg"
    elif album =="葉惠美":
        message="https://upload.wikimedia.org/wikipedia/zh/thumb/4/48/Jay_2003_ablum_cover.jpg/220px-Jay_2003_ablum_cover.jpg"
    elif album =="七里香":
        message="https://upload.wikimedia.org/wikipedia/zh/thumb/b/bc/Jay_Chou-Common_Jasmin_Orange_2004_Cover.jpg/220px-Jay_Chou-Common_Jasmin_Orange_2004_Cover.jpg"
    elif album =="11月的蕭邦":
        message = "https://upload.wikimedia.org/wikipedia/zh/9/93/Jay_chopin_cover270.jpg"
    elif album == "依然范特西":
        message ="https://upload.wikimedia.org/wikipedia/zh/e/ea/Jay_Chow_Still_Fantasy_CDCover.jpg"
    elif album =="我很忙":
        message = "https://upload.wikimedia.org/wikipedia/zh/thumb/1/12/Jay_Chou_on_the_run.jpg/220px-Jay_Chou_on_the_run.jpg"
    elif album =="魔杰座":
        message = "https://upload.wikimedia.org/wikipedia/zh/thumb/c/cb/Capricorn_%28album%29_cover2.jpg/220px-Capricorn_%28album%29_cover2.jpg"
    elif album =="跨時代":
        message ="https://i.kfs.io/album/global/147597,1v1/fit/500x500.jpg"
    elif album =="驚嘆號":
        message="https://i.kfs.io/album/tw/308575,0v3/fit/500x500.jpg"
    elif album =="12新作":
        message ="https://i.kfs.io/album/tw/525523,1v3/fit/500x500.jpg"
    elif album=="哎呦，不錯哦":
        message ="https://img.discogs.com/0XOHISwq1hyEjb5pA7bT-Csrnd8=/fit-in/600x600/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-16375869-1607364480-8589.jpeg.jpg"
    elif album =="周杰倫的床邊故事":
        message ="https://upload.wikimedia.org/wikipedia/zh/b/b2/JayChouBedtimeStories-2016_Cover.jpg"
    elif album =="范特西Plus":
        message ="https://img.discogs.com/4OQLK7bq4ttOpGlCd2dknwQQYG4=/fit-in/559x480/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-3837633-1346363791-8939.jpeg.jpg"
    elif album =="尋找周杰倫 EP":
        message ="https://i.kfs.io/album/tw/47735,0v3/fit/500x500.jpg"
    elif album =="霍元甲 EP":
        message ="https://upload.wikimedia.org/wikipedia/zh/4/4a/Fearless_Jay_Chou.jpg"
    elif album =="黃金甲 EP":
        message ="https://upload.wikimedia.org/wikipedia/zh/thumb/7/7d/Curse_of_the_Golden_Flower_EP_Cover.jpg/220px-Curse_of_the_Golden_Flower_EP_Cover.jpg"
    return message
def random_song_choose():
    p = random.randint(1,18)
    if p ==1:
        message = "收錄在"+"Jay這張專輯中的"+random.choice(album_and_song_dict['Jay'])
    if p ==2:
        message = "收錄在"+"范特西這張專輯中的"+random.choice(album_and_song_dict['范特西'])
    if p ==3:
        message = "收錄在"+"八度空間這張專輯中的"+random.choice(album_and_song_dict['八度空間']) 
    if p ==4:
        message = "收錄在"+"葉惠美這張專輯中的"+random.choice(album_and_song_dict['葉惠美'])
    if p ==5:
        message = "收錄在"+"七里香這張專輯中的"+random.choice(album_and_song_dict['七里香'])
    if p ==6:
        message = "收錄在"+"11月的蕭邦這張專輯中的"+random.choice(album_and_song_dict['11月的蕭邦'])
    if p ==7:
        message = "收錄在"+"依然范特西這張專輯中的"+random.choice(album_and_song_dict['依然范特西'])
    if p ==8:
        message = "收錄在"+"我很忙這張專輯中的"+random.choice(album_and_song_dict['我很忙'])
    if p ==9:
        message = "收錄在"+"魔杰座這張專輯中的"+random.choice(album_and_song_dict['魔杰座'])
    if p ==10:
        message = "收錄在"+"跨時代這張專輯中的"+random.choice(album_and_song_dict['跨時代'])
    if p ==11:
        message = "收錄在"+"驚嘆號這張專輯中的"+random.choice(album_and_song_dict['驚嘆號'])
    if p ==12:
        message = "收錄在"+"12新作這張專輯中的"+random.choice(album_and_song_dict['12新作'])
    if p ==13:
        message = "收錄在"+"哎呦，不錯哦這張專輯中的"+random.choice(album_and_song_dict['哎呦，不錯哦']) 
    if p ==14:
        message = "收錄在"+"周杰倫的床邊故事這張專輯中的"+random.choice(album_and_song_dict['周杰倫的床邊故事'])
    if p ==15:
        message = "收錄在"+"范特西Plus這張專輯中的"+random.choice(album_and_song_dict['范特西Plus'])
    if p ==16:
        message = "收錄在"+"尋找周杰倫 EP這張專輯中的"+random.choice(album_and_song_dict['尋找周杰倫 EP'])   
    if p ==17:
        message = "收錄在"+"霍元甲 EP這張專輯中的"+random.choice(album_and_song_dict['霍元甲 EP'])  
    if p ==18:
        message = "收錄在"+"黃金甲 EP這張專輯中的"+random.choice(album_and_song_dict['黃金甲 EP']) 
    print("**********************************")
    print(message)  
    return message
def introdice_jay():
    message = "周杰倫（英語：Jay Chou Chieh-lun，1979年1月18日－），臺灣華語流行歌曲男歌手、音樂家、編曲家、唱片製片人、魔術師。同時是演員、導演、電子競技職業戰隊J Team的老闆。在2000年，周杰倫發行了他的首張專輯《Jay》，從屬於唱片公司阿爾發音樂。從此以後，他的音樂獲得了遍及亞洲的榮譽，尤其在臺灣、中國大陸、馬來西亞、香港、新加坡、印度尼西亞、韓國、日本和西方國家——例如美國和澳大利亞——的亞裔社群中。周杰倫是華語流行音樂歷史上最具影響力的音樂人之一，其在本土臺灣共有247萬張專輯的銷量並獲得了許多針對他的音樂工作的獎項，包括15座臺灣金曲獎，2座MTV亞洲大獎。周杰倫也為其他藝術家寫歌。在2003年，他是《時代》雜誌（亞洲版）的封面故事，被稱為「亞洲流行音樂的新天王」。他其後開展了六個世界巡演，在世界各地的城市中對超過1000萬人表演。周杰倫在電影《頭文字D》（2005）中開始了他的電影事業；他從此涉足許多其他的電影企劃。周杰倫也管理他自己的唱片和經紀公司杰威爾音樂。2011年首度進入好萊塢，主演《青蜂俠》之助理Kato；而後在2016年，他再次進入了好萊塢，在電影《出神入化2》中扮演小李。"
    return message
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.song_reg =""
        self.album_reg=""
    def is_going_to_search_album_by_song(self, event):
        text = event.message.text
        self.song_reg = text
        return is_song_exist(text)

    def is_going_to_intro_album(self, event):
        text = event.message.text
        return text.lower() == "介紹專輯"
    
    def is_going_to_indtro_album_other_song(self, event):
        text = event.message.text
        return text.lower() == "專輯裡的其他首歌"

    def is_going_to_recommand_song(self, event):
        text = event.message.text
        return text.lower() == "推薦的歌"

    def is_going_to_recommand_song_by_album(self, event):
        text = event.message.text
        self.album_reg = text
        return is_album_exist(text)

    def is_going_to_random_collect_song(self, event):
        text = event.message.text
        return text.lower() == "隨機"

    def is_going_to_about_jay(self, event):
        text = event.message.text
        return text.lower() == "關於周杰倫"  
    
    def is_going_to_initial(self, event):
        text = event.message.text
        return text.lower() == "返回" 

    def on_enter_search_album_by_song(self, event):
        #print("I'm entering state1")
        reply_token = event.reply_token
        text1 =find_album_by_song_name(self.song_reg)
        self.album_reg=text1
        #send_text_message(reply_token,text+"\n輸入:介紹專輯 就會介紹本專輯\n輸入:介紹專輯裡的其他首歌 就會介紹專輯裡的其他首歌")
        url=search_url(self.album_reg)
        title = text1
        text =" "
        btn = [
            MessageTemplateAction(label="介紹專輯",text="介紹專輯"),
            MessageTemplateAction(label="介紹專輯裡的其他首歌",text="專輯裡的其他首歌")]
        
        send_button_message(event.reply_token,title,text,btn,url)
    def on_enter_intro_album(self, event):
        reply_token = event.reply_token
        text = album_introdution(self.album_reg)
        print(self.album_reg)
        send_text_message(reply_token,text+"\n輸入:返回")

    def on_enter_indtro_album_other_song(self, event):
        reply_token = event.reply_token
        text = find_all_songs_in_album(self.album_reg)
        send_text_message(reply_token,text+"\n輸入:返回")
    
    def on_enter_recommand_song(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token,"輸入:返回\n輸入:專輯名稱 會依據專輯推薦歌曲\n輸入:隨機 會隨機挑選歌曲")
    
    def on_enter_recommand_song_by_album(self, event):
        reply_token = event.reply_token
        text = recommand_song_by_album(self.album_reg)
        send_text_message(reply_token,text+"\n輸入:返回")

    def on_enter_random_collect_song(self, event):
        reply_token = event.reply_token
        text = random_song_choose()
        send_text_message(reply_token,"來聽聽"+text+"吧\n輸入:返回")

    def on_enter_about_jay(self, event):
        reply_token = event.reply_token
        text = introdice_jay()
        send_text_message(reply_token,text+"吧\n輸入:返回")

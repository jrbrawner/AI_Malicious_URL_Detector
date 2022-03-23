#url features obtained by using external entities
import whois

url = 'http://www.crestonwood.com/router.php'

urlList = ['url', 'http://www.crestonwood.com/router.php',
           'http://shadetreetechnology.com/V4/validation/a111aedc8ae390eabcfa130e041a10a4',
           'https://support-appleld.com.secureupdate.duilawyeryork.com/ap/89e6a3b4b063b8d/?cmd=_update&dispatch=89e6a3b4b063b8d1b&locale=_',
           'http://rgipt.ac.in',
           'http://www.iracing.com/tracks/gateway-motorsports-park/',
           'http://appleid.apple.com-app.es/',
           'http://www.mutuo.it',
           'http://www.shadetreetechnology.com/V4/validation/ba4b8bddd7958ecb8772c836c2969531',
           'http://vamoaestudiarmedicina.blogspot.com/',
           'https://parade.com/425836/joshwigler/the-amazing-race-host-phil-keoghan-previews-the-season-27-premiere/',
           'https://sura.careervidi.com/mot?fg=Z4Nwk2pibWKclbF2k29kaHd1YKCWjJyepKZdaXy0j2lj/koenig-sandra@online.de',
           'https://magalu-crediarioluiza.com/Produto_20203/produto.php?sku=1962067',
           'https://oki.si/pkginfo/change/sitekeyverification.php?origin=cob&check=yes&destination=authentication',
           'http://www.strykertoyhaulers.com/wp-admin/js/online/order.php?email%5Cu003dabuse@euroflightinternational.com',
           'https://monovative-my.sharepoint.com:443/:o:/g/personal/user_monovative_onmicrosoft_com/EmCzKJnKZgxDtejtstZ67qQBlkNaRN4Da620KjAjE91eWQ?e=5:wesEg8&amp;at=9',
           'http://98.126.214.77/ap/signin?openid.pape.max_auth_age=0&amp;openid.return_to=https://www.amazon.co.jp/?ref_=nav_em_hd_re_signin&amp;openid.identity=http://specs.openid.net/auth/2.0/identifier_select&amp;openid.assoc_handle=jpflex&amp;openid.mode=checkid_setup&amp;key=a@b.c&amp;openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&amp;openid.ns=http://specs.openid.net/auth/2.0&amp;&amp;ref_=nav_em_hd_clc_signin',
           'http://swallowthisbitchpics.com/jpg/www.global.visa.com/myca/oce/emea/action/request_type=un_Activation/visa.html',
           'http://107.180.44.78/login.php?cmd=login_submit&amp;id=d38dd677c4dd931661bdc94df4bafb23d38dd677c4dd931661bdc94df4bafb23&amp;session=d38dd677c4dd931661bdc94df4bafb23d38dd677c4dd931661bdc94df4bafb23',
           'https://bit.ly/2E6D7J1',
           'http://u.to/x9AVFg']




#months since domain was registered
def months_since_creation(url):
    w = whois.whois(url)
    creation_date = w.creation_date
    print(creation_date)



months_since_creation(url)
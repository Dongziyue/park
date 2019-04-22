var defaultOpt = {
    mapDataUrl: '../data',
    mapThemeUrl: '../data/theme',
    mapID: "test666",
    themeID:1004
}
	function getQueryString(name){
	     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
	     var r = window.location.search.substr(1).match(reg);
	     if(r!=null)return  unescape(r[2]); return null;
}
(function(){
    var bp = document.createElement('script');
    var curProtocol = window.location.protocol.split(':')[0];
    if (curProtocol === 'https') {
        bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
    }
    else {
        bp.src = 'http://push.zhanzhang.baidu.com/push.js';
    }
    var s = document.getElementsByTagName("script")[0];
    s.parentNode.insertBefore(bp, s);
})();

//baidu
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?eaa22075ffedfde4dc734cdbc709273d";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();

//360
(function(){
var src = (document.location.protocol == "http:") ? "http://js.passport.qihucdn.com/11.0.1.js?ff2c88bec7d3be1f59ccc8ed92ea5b04":"https://jspassport.ssl.qhimg.com/11.0.1.js?ff2c88bec7d3be1f59ccc8ed92ea5b04";
document.write('<script src="' + src + '" id="sozz"><\/script>');
})();

(function(){
	   document.write('<script async src="https://www.googletagmanager.com/gtag/js?id=UA-123411334-1"><\/script>');
	   window.dataLayer = window.dataLayer || [];
	   function gtag(){dataLayer.push(arguments);}
	   gtag('js', new Date());

	   gtag('config', 'UA-123411334-1');
    })();

//tips
(function(){
    window.MaskLayer = {
        _layer: null,
        show: function (element) {
            var _this = this;
            element = element || document.body;
            if (MaskLayer._layer && MaskLayer._layer.parentNode) {
                MaskLayer._layer.parentNode.removeChild(MaskLayer._layer);
            }
            MaskLayer._layer = document.createElement("div");
            MaskLayer._layer.className = "mask-layer-container";
            element.appendChild(MaskLayer._layer);
            var outer = document.createElement("div");
            outer.className = "tip-outer";
            var inner = document.createElement("div");
            inner.className = "tip-inner"
        
            var content = "<h2 class='t-1'> <small>左键</small>平移</h2> <h2 class='t-2'> <small>右键</small>旋转</h2><h2 class='t-3'> <small>滚轮</small>缩放</h2> <div class='t-close'>知道了</div>";
            inner.innerHTML = content;

            outer.appendChild(inner);
            MaskLayer._layer.appendChild(outer);
            outer.style.cssText = " position: absolute; z-index: 999;width:100%;height: 100%; background: rgba(0,0,0,0.6);display: flex;justify-content: center;align-items:center;color:#fff;";
            inner.style.position = "relative";
            inner.style.background = "url('../image/tips.png') no-repeat";
            inner.style.width = "300px";
            inner.style.height = "300px";
            
            document.querySelector(".tip-outer h2:nth-of-type(1)").style.cssText = "position:absolute;bottom:97px;left:-106px;letterSpacint:3px;";
            document.querySelector(".tip-outer h2:nth-of-type(2)").style.cssText = "position:absolute;right:-103px;top:32px;letterSpacint:3px;";
            document.querySelector(".tip-outer h2:nth-of-type(3)").style.cssText = "position:absolute;bottom:83px;right:-104px;letterSpacint:3px;";
            var tclose = document.querySelector(".tip-inner  .t-close");
            tclose.style.cssText = "position:absolute;bottom:-97px;left:50%;margin-left:-37px;padding:10px 28px;border:2px solid #fff;border-radius:8px;cursor:pointer;font-size:20px;font-weight:600";

            var layer =  document.querySelector(".mask-layer-container");
            layer.style.cssText = "position: fixed; left: 0; right: 0; top: 0; bottom: 0; background-color: rgba(0,0,0,0.6); opacity: 0;transition:opacity 0.5s; -webkit-transition: opacity 0.5s; z-index: 800;";

            tclose.onclick = function(){
                _this.hide();
            }
            window.setTimeout(function () {
                MaskLayer._layer.className = MaskLayer._layer.className + " show";
                var layershow =  document.querySelector(".mask-layer-container.show");
                layershow.style.opacity = 1;
            }, 10);
        },
        hide: function () {
            if (!MaskLayer._layer) return;
            MaskLayer._layer.className = MaskLayer._layer.className.replace(/show/g, "");
            window.setTimeout(function () {
                if (!MaskLayer._layer) return;
                MaskLayer._layer.parentNode.removeChild(MaskLayer._layer);
                MaskLayer._layer = null;
            }, 200);
        }
    };
    var tiped = window.localStorage.getItem("esmap_tiped");
    if(!tiped){
        setTimeout(function(){
            window.MaskLayer.show();
            localStorage.setItem("esmap_tiped",true)
        },3000)
    }
})();

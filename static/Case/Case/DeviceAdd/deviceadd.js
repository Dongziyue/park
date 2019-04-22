var seg, im, line1;
var fnum, line;
var flag = false;
var boundFlag = false;
var coordsData = null;
var coordIndex = 0;
var mapCoord;
//定义map、floorLayer全局变量
var map;
var floorLayer;
var centerFlag = false;
var boundFlag = false;
var linelayer;
var devicelayer;
var id = getQueryString('id') || defaultOpt.mapID;
var styleid = getQueryString("styleid") || defaultOpt.themeID;
var container = document.getElementById('map-container');
map = new esmap.ESMap({
    container: container, //渲染dom
    mapDataSrc: "../../data", //地图数据位置
    mapThemeSrc: "../../data/theme", //主题数据位置
    themeID: styleid //样式ID
});
var floorControl;
//楼层控制控件配置参数(选几楼)
var ctlOpt = new esmap.ESControlOptions({
    position: esmap.ESControlPositon.RIGHT_TOP,
    imgURL: "image/wedgets/"
});

//打开地图数据
map.openMapById(id);
map.showCompass = true;

map.on("loadComplete", function () {
    //创建楼层控件
    floorControl = new esmap.ESScrollFloorsControl(map, ctlOpt);
    bingEvents();

    for(var i=0;i<map.floorNames.length;i++)
    {
        $("#fid").append('<option value="'+(i+1)+'">'+(map.floorNames[i])+'</option>')
    }
    $("#fid").value = 1;
});
//载入json数据
$.getJSON("data/devicelist.json", function (data) {
    coordsData = data.rows;
});
//地图点击事件  获取地图坐标x,y坐标
map.on("mapClickNode", function (e) {
    mapCoord = e.hitCoord || null;
})

//点击事件 
map.on('mapClickNode', function(event) {
    if (event.nodeType == esmap.ESNodeType.FLOOR||event.nodeType ==esmap.ESNodeType.MODEL)
    {
        var focusFloorNum = map.focusFloorNum;
        if (centerFlag) {
            $("#angletype").val(10); //摄像头角度值
            drawPoints(event.hitCoord.x, event.hitCoord.y, focusFloorNum);
            flag = true; //添加摄像头以后，图层存在 打开开关 
            $('#latitude').val(event.hitCoord.x.toFixed(6)); //摄像头经度值
            $('#longtitude').val(event.hitCoord.y.toFixed(6)); //摄像头纬度值
            $("#deviceid").val(++coordIndex); //摄像头id
        }
        if (boundFlag) {
            drawLine1(event.hitCoord.x, event.hitCoord.y, focusFloorNum);
        }
    }
});
var maintype = $("#maintype");
//添加摄像头图片标注
function drawPoints(x, y, focusFloorNum) {
    devicelayer.removeAll();
    im = new esmap.ESImageMarker({
        x: x,
        y: y,
        height: 2,
        url: 'image/camera1.png',
        size: 12,
        seeThrough: true,
        showLevel: 24,
        angle: 10, //控制标注随着地图旋转。(size需要重新设置)
        zoom: 0 //控制标注随着地图缩小
    });
    //切换摄像头类型
    var maintype = $("#maintype");
    maintype.change(function () {
        im.url = $(this).val();
    });
    devicelayer.addMarker(im);
}
//添加线的 点标注
function drawLinePoints(x, y, focusFloorNum) {
    var im = new esmap.ESImageMarker({
        x: x,
        y: y,
        url: 'image/user.png',
        size: 32,
        height: 1,
        seeThrough: true,
        showLevel: 24
    });
    linelayer.addMarker(im);
}
//切换楼层
var fid = $("#fid");
fid.change(function () {
    map.changeFocusFloor($(this).val());
    reset.click();
    map.clearLineMarkById("bline"); //清除边框线
    floorLayer = null;
    line = null;
    seg = null;
    centerFlag = false;
    boundFlag = false;
});

function addAngle() { //改变角度  增加旋转角度
    var angle = $("#angletype").val();
    angle = Number(angle) + 10;
    $("#angletype").val(angle);
    fnum = map.focusFloorNum;
    updateMakerAngle(angle, fnum);
}

function cutAngle() { //改变角度  减少旋转角度
    var angle = $("#angletype").val();
    angle = Number(angle) - 10;
    $("#angletype").val(angle);
    fnum = map.focusFloorNum;
    updateMakerAngle(angle, fnum);
}

function updateMakerAngle(angle, fnum) { //刷新摄像头角度
    var floor = map.getFloor(fnum);
    floor.traverse(function (obj) { //obj-->imageMarker
        //摄像头角度旋转
        if (obj.nodeType == 31) {
            obj.rotateTo(angle);
        }
    })
}

//重置按钮
var reset = document.getElementById("reset");
reset.onclick = function () {
    $('#latitude').val(null); //摄像头经度值
    $('#longtitude').val(null); //摄像头纬度值
    $("#deviceid").val(null); //摄像头id
    $("#angletype").val(null); //摄像头角度

    if (devicelayer) devicelayer.removeAll();
    if (linelayer) linelayer.removeAll(); //删除所有标注
    map.clearLineMarkById("bline"); //清除边框线
    if (seg)
        seg = [];
    centerFlag = false;
    boundFlag = false;
}

//线型
var lineStyle = {
    color: "#F00000",
    lineWidth: 2,
    alpha: 0.8,
    offsetHeight: 0,
    seeThrough: true,
    lineType: esmap.ESLineType.DOT_DASH,
    dash: {
        size: 2,
        gap: 1
    }
};

// 点击添加摄像头
$("#addCenter").click(function () { //添加摄像头位置
    centerFlag = true;
    boundFlag = false;
    if (devicelayer) devicelayer.removeAll();
    floorLayer = map.getFloor(map.focusFloorNum); //获取图层
    devicelayer = new esmap.ESLayer('imageMarker');
    floorLayer.addLayer(devicelayer);
    if (seg)
        seg = [];

});
//添加监控范围
var addBound = $("#addBound");
addBound.click(function () {
    boundFlag = true;
    centerFlag = false;
    map.clearLineMarkById("bline"); //清除边框线
    if (linelayer) linelayer.removeAll(); //删除所有线标注
    floorLayer = map.getFloor(map.focusFloorNum); //
    linelayer = new esmap.ESLayer('imageMarker');
    floorLayer.addLayer(linelayer);
    if (seg)
        seg = [];
    alert('请按顺序在地图上点击选择至少3个边界点！');
});

//画边界线
function drawLine1(x1, y1, fnum) {
    if (!seg) {
        seg = [];
    }
    seg.push({
        x: x1,
        y: y1,
        fnum: fnum
    });
    var cnt = seg.length;
    var newseg = [].concat(seg);
    var value = '';
    newseg.push(seg[0]);
    if (cnt > 2) {
        var isok = true;
        for (var i = 0; i < cnt - 2; i++) {
            var flag, distance;
            distance = Math.sqrt(Math.pow(seg[cnt - 1].x - seg[i].x, 2) + Math.pow(seg[cnt - 1].y - seg[i].y, 2));
            //点的位置与其它点太近
            if (distance < 1) {
                isok = false;
                break;
            }
            //判断最后一条线和其他所有线段有没有交点
            flag = segmentsIntr(seg[i], seg[i + 1], seg[cnt - 2], seg[cnt - 1]);
            if (flag) { //如果有交点
                isok = false;
                break;
            } else {
                //判断最后第二条线和其他所有线段有没有交点
                flag = segmentsIntr(seg[i], seg[i + 1], seg[cnt - 1], seg[0]);
                if (flag) {
                    isok = false;
                    break;
                }
            }
            value += '(' + seg[i].x.toFixed(6) + ',' + seg[i].y.toFixed(6) + '),'; //监控边界值
        }
        value += '(' + seg[cnt-2].x.toFixed(6) + ',' + seg[cnt-2].y.toFixed(6) + '),'; //监控边界值
        value += '(' + seg[cnt-1].x.toFixed(6) + ',' + seg[cnt-1].y.toFixed(6) + ')'; //监控边界值
        $('#gpsbounds').val(value);

        if (isok) {
            map.clearLineMarkById("bline");
            drawLinePoints(x1, y1, fnum); //添加摄像头的位置  一个点
            var line = new esmap.ESLineMarker("bline", newseg, lineStyle);
            map.drawLineMark(line);
        } else { //不满足条件 抛弃新点
            seg.pop();
        }
    } else if (cnt > 1) { //有两个点画一条直线
        drawLinePoints(x1, y1, fnum);
        map.clearLineMarkById("bline");
        var line1 = new esmap.ESLineMarker("bline", newseg, lineStyle);
        map.drawLineMark(line1);
    } else {
        drawLinePoints(x1, y1, fnum);
    }
}
//判断两条直线是否相交，相交返回交点，不相交返回false
function segmentsIntr(a, b, c, d) {

    if ((a.x == c.x && a.y == c.y) || (b.x == c.x && b.y == c.y) || (a.x == d.x && a.y == d.y) || (b.x == d.x && b.y == d.y))
        return false;
    // 三角形abc 面积的2倍  
    var area_abc = (a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x);
    // 三角形abd 面积的2倍  
    var area_abd = (a.x - d.x) * (b.y - d.y) - (a.y - d.y) * (b.x - d.x);
    // 面积符号相同则两点在线段同侧,不相交 (对点在线段上的情况,本例当作不相交处理);  
    if (area_abc * area_abd > 0) {
        return false;
    }

    // 三角形cda 面积的2倍  
    var area_cda = (c.x - a.x) * (d.y - a.y) - (c.y - a.y) * (d.x - a.x);
    // 三角形cdb 面积的2倍  
    // 注意: 这里有一个小优化.不需要再用公式计算面积,而是通过已知的三个面积加减得出.  
    var area_cdb = area_cda + area_abc - area_abd;
    if (area_cda * area_cdb > 0) {
        return false;
    }

    //计算交点坐标  
    var t = area_cda / (area_abd - area_abc);
    var dx = t * (b.x - a.x),
        dy = t * (b.y - a.y);
    return {
        x: a.x + dx,
        y: a.y + dy
    };
}

//绑定事件
function bingEvents() {
    document.getElementById('btn3D').onclick = function () {
        if (map.viewMode == esmap.ESViewMode.MODE_2D) {
            map.viewMode = esmap.ESViewMode.MODE_3D; //2D-->3D
            document.getElementById('btn3D').style.backgroundImage = "url('image/wedgets/3D.png')";
        } else {
            map.viewMode = esmap.ESViewMode.MODE_2D; //3D-->2D
            document.getElementById('btn3D').style.backgroundImage = "url('image/wedgets/2D.png')";
        }
    }
}
//保存按钮
var submit = document.getElementById("submit");
submit.onclick = function () {
    alert("当前楼层：" + map.focusFloorNum + "楼" + "\n" +
        "摄像头类型：" + $("#maintype").find("option").html() + "\n" +
        "摄像头ID：" + $('#deviceid').val() + "\n" +
        "摄像头角度：" + $("#angletype").val() + "\n" +
        "摄像头经度：" + $('#latitude').val() + "\n" +
        "摄像头纬度：" + $('#longtitude').val() + "\n" +
        "请自行编写后台接口！");
}
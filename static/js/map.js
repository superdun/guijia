/**
 * Created by dun on 17-2-28.
 */

var map = null;
function init() {
    map = new Dituhui.Map("myMap", "http://dev.dituhui.com/sdk/1.0.0/swfs/", "100000", Dituhui.MapType.BUBBLE, "setData", "onError", "zh_cn");
}

function setData() {
    $.ajax({
        url: "api/mapData",
        dataType: 'json',
        success: function (result) {
            var mapData = result;
            //markerSymbol:circle,square,star,triangle
            var mapStyles = [
                {min: 1, max: 1, fillColor: '#377EB8'},
                {min: 2, max: 2, fillColor: '#984EA3'},
                {min: 3, fillColor: '#FFFF33'}];
            var titleStyle = {fontSize: 25, fontColor: '#000000'};
            var option =
                {
                    data: mapData,
                    styles: mapStyles,
                    title: "今日走失情况实时图",
                    titleStyle: titleStyle,
                    valueField: 'count',
                    fillColorType: 'red',
                    mapFillColor: '#eec3c0',
                    backgroundColor: "#F5F5F5",
                    subtitle:'本站信息均来源于网络与个人登记，本站不对信息真实性负责',
                    legendVisible: false,
                    events: [{eventName: "mousemove", isShowTooltip: true}]
                };
            map.setMapOptions(option);
        }
    });

}
function onError(errorcode) {
    /*errorcode：错误编码，有关错误编码的详细描述可参考:
     "开发指南"-->"API参考"-->"错误编码"*/
    alert(errorcode);
}

window.onload = init;



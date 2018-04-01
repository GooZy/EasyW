/**
 * Created by guoziyao on 2018/3/30.
 */
// 上传图片前预览
function previewImage(file, id, MAXWIDTH, MAXHEIGHT) {
    var img = document.getElementById(id);
    img.title = id;
    if (file.files && file.files[0]) {
        img.onload = function () {
            var rect = getZoomParam(MAXWIDTH, MAXHEIGHT, img.offsetWidth, img.offsetHeight);
            img.width = rect.width;
            img.height = rect.height;
        };
        var reader = new FileReader();
        reader.onload = function (evt) {
            img.src = evt.target.result;
        };
        reader.readAsDataURL(file.files[0]);
      } else {
          //兼容IE
          file.select();
          var src = document.selection.createRange().text;
          img.filters.item('DXImageTransform.Microsoft.AlphaImageLoader').src = src;
      }
}


// 获取缩放的尺寸
function getZoomParam(maxWidth, maxHeight, width, height) {
    var param = { top: 0, left: 0, width: width, height: height };
    if (width > maxWidth || height > maxHeight) {
        rateWidth = width / maxWidth;
        rateHeight = height / maxHeight;
        if (rateWidth > rateHeight) {
            param.width = maxWidth;
            param.height = Math.round(height / rateWidth);
        } else {
            param.width = Math.round(width / rateHeight);
            param.height = maxHeight;
        }
    }
    param.left = Math.round((maxWidth - param.width) / 2);
    param.top = Math.round((maxHeight - param.height) / 2);
    return param;
}


//展示
function showBigPic(filepath) {

    var img = document.getElementById('pre_view');
    //将文件路径传给img大图
    img.src = filepath;
    //获取大图div是否存在
    var div = document.getElementById("bigPic");
    if (!div) {
        return;
    }
    // 缩放
    var rect = getZoomParam(400, 400, img.naturalWidth, img.naturalHeight);
    img.width = rect.width;
    img.height = rect.height;
    //如果存在则展示
    div.style.display="block";
    //获取鼠标坐标
    var intX = window.event.clientX;
    var intY = window.event.clientY;
    console.log('x:', intX, 'y', intY);
    console.log(window.screen.height);
    if (intY * 2 >= window.screen.height) {
        //设置大图左上角起点位置
        div.style.left = intX + 5 + "px";
        div.style.top = intY - img.height + "px";
    }
    else {
        //设置大图左上角起点位置
        div.style.left = intX + 5 + "px";
        div.style.top = intY + 5 + "px";
    }
}


//隐藏
function closeImg(){
    document.getElementById("bigPic").style.display="none";
}
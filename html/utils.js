//整数%2d格式化
//num 可以是整数，浮点数或者字符串
//n表示格式化几位数
function fix(num, n) {
    //爱几个0就几个，够用就行
    var y = '000000000' + parseInt(num);
    return y.substr(y.length - n);
}

// 时间戳转换为北京时间 2017-10-22 09:23:06
function timestamp2timestr(timestamp) {
    var date = new Date(timestamp * 1000 + 8 * 60 * 60 * 1000);
    return date.getUTCFullYear() + "-" + fix(date.getUTCMonth() + 1, 2) + "-" + fix(date.getUTCDate(), 2) + " " + fix(date.getUTCHours(), 2) + ":" + fix(date.getUTCMinutes(), 2) + ":" + fix(date.getUTCSeconds(), 2);
}


// 使用Post请求
function login() {
    // 获取用户名和密码输入值
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // 发送 AJAX 请求到登录端点
    $.ajax({
        url: 'http://192.168.8.32:8010/login',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ user_name: username, pwd: password }),
        success: function(response) {
            alert('登录成功！');
        },
        error: function() {
            alert('登录失败，请重试。');
        }
    });
}


function register() {
    // 获取新用户注册输入值
    var newUsername = document.getElementById('newUsername').value;
    var newPassword = document.getElementById('newPassword').value;
    var phoneNumber = document.getElementById('phoneNumber').value;
    var email = document.getElementById('email').value;
    
    // 发送 AJAX 请求到注册端点
    $.ajax({
        url: 'http://192.168.8.32:8010/register',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ user_name: newUsername, pwd: newPassword, phone: phoneNumber, email: email }),
        success: function(response) {
            alert('注册成功！');
        },
        error: function() {
            alert('注册失败，请重试。');
        }
    });
}

// // 使用Get请求
// function login() {
//     // 获取用户名和密码输入值
//     var username = document.getElementById('username').value;
//     var password = document.getElementById('password').value;

//     // 构建带有参数的URL
//     var url = `http://192.168.8.32:8010/login?user_name=${username}&pwd=${password}`;

//     // 发送 AJAX 请求到登录端点
//     $.ajax({
//         url: url,
//         type: 'GET',
//         contentType: 'application/json',
//         success: function(response) {
//             alert('登录成功！');
//         },
//         error: function() {
//             alert('登录失败，请重试。');
//         }
//     });
// }

// function register() {
//     // 获取新用户注册输入值
//     var newUsername = document.getElementById('newUsername').value;
//     var newPassword = document.getElementById('newPassword').value;
//     var phoneNumber = document.getElementById('phoneNumber').value;
//     var email = document.getElementById('email').value;

//     // 构建带有参数的URL
//     var url = `http://192.168.8.32:8010/register?user_name=${newUsername}&pwd=${newPassword}&phone=${phoneNumber}&email=${email}`;

//     // 发送 AJAX 请求到注册端点
//     $.ajax({
//         url: url,
//         type: 'GET',
//         contentType: 'application/json',
//         success: function(response) {
//             alert('注册成功！');
//         },
//         error: function() {
//             alert('注册失败，请重试。');
//         }
//     });
// }

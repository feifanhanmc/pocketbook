//app.js
App({
  onLaunch: function () {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // wx.setStorageSync('acc_user', 'test')
    // var acc_user = wx.getStorageSync('acc_user') || ''
    // if (acc_user == ''){
    //   console.log('login')
    //   wx.setStorageSync('acc_user', 'acc_user')
    // }else{
    //   console.log('acc_user')
    //   console.log(acc_user)
    // }
    
    
    
    // // 登录
    // wx.login({
    //   success: resp => {
    //     // 发送 res.code 到后台换取 openId, sessionKey, unionId
    //     console.log(resp);
    //     var that = this;
    //     // 获取用户信息
    //     wx.getSetting({
    //       success: res => {
    //         console.log('getSetting')
    //         console.log(res)
    //         if (res.authSetting['scope.userInfo']) {
    //           // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
    //           wx.getUserInfo({
    //             success: userResult => {
    //               var platUserInfoMap = {}
    //               platUserInfoMap["encryptedData"] = userResult.encryptedData;
    //               platUserInfoMap["iv"] = userResult.iv;
    //               wx.request({
    //           url: 'https://sun.liuyihua.com/wxuser/login_init',
    //           data: { 
    //             platCode: resp.code,
    //                   platUserInfoMap: platUserInfoMap,
    //           },
    //           header: {
    //             "Content-Type": "application/json"
    //           },
    //           method: 'POST',
    //           dataType:'json',
    //           success: function (res) {
    //             console.log(res)
    //                   wx.setStorageSync("userinfo", res.userinfo) //设置本地缓存
    //           },
    //           fail: function (err) { },//请求失败
    //           complete: function () { }//请求完成后执行的函数
    //         })
    //             }
    //           })
    //         } 
    //       }
    //     })
    //   }
    // })  
    // 获取用户信息
    // wx.getSetting({
    //   success: res => {
    //     if (res.authSetting['scope.userInfo']) {
    //       // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
    //       wx.getUserInfo({
    //         success: res => {
    //           // 可以将 res 发送给后台解码出 unionId
    //           this.globalData.userInfo = res.userInfo
    //           console.log(res.userInfo);
    //           // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
    //           // 所以此处加入 callback 以防止这种情况
    //           if (this.userInfoReadyCallback) {
    //             this.userInfoReadyCallback(res)
    //           }
    //         }
    //       })
    //     }
    //   }
    // })
  },
  onError: function(err){
    console.log(err)
    // 可将报错信息发送至服务器后台
  },
  globalData: {
    userInfo: null
  }
})
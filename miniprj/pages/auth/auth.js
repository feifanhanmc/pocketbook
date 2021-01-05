// pages/auth/auth.js
import regeneratorRuntime from '../..//utils/runtime/runtime';
import { request } from "../../utils/request/request.js";
import { login } from "../../utils/asyncwx.js";

const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    // UserData
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
  },
  async handleGetUserInfo(e) {
    const userInfo=e.detail.userInfo || {};
    if (JSON.stringify(userInfo) !== "{}"){
      try {
        // 0 将用户信息放进缓存等
        wx.setStorageSync('userInfo', userInfo)
        this.setData({
          userInfo,
          hasUserInfo: true
        })
        // 1 获取用户信息
        const { encryptedData, rawData, iv, signature } = e.detail;
        // 2 获取小程序登录成功后的code
        const {code} = await login();
        // 3 发送请求 获取用户的token
        const loginParams={ encryptedData, rawData, iv, signature ,code};
        const {token} = await request({url:"/wxuser/login_init",data:loginParams,method:"post"});
        // 4 把token(即acc_user)存入缓存中
        wx.setStorageSync("token", token);  
        // 5 认证完成后，返回home页面
        console.log('Auth Success!')
        // RefreshFlag
        wx.setStorageSync('flagRefreshAssetsList', true);
        wx.setStorageSync('flagRefreshAccountData', true);
        wx.switchTab({
          url: '/pages/home/home',
        })
      } catch (error){
        console.log(error)
      }
    }

  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    const userInfo = wx.getStorageSync('userInfo') || {}
    if (JSON.stringify(userInfo) !== "{}"){
      this.setData({
        userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回，所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          wx.setStorageSync('userInfo', res.userInfo)
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})
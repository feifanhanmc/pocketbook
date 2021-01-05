// pages/home/home.js
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
    
    // AccountData
    amountMonthExpend: 0.0,
    amountMonthIncome: 0.0,
    amountMonthRemainingBudget: 0.0,
    amountNetAssets: 0.0,
    amountTotalAssets: 0.0,
    amountTotalLiability: 0.0,

    // AssetsData
    assetsList: [],

    // OtherData
    assetIconPath: "/data/icons/asset/",
  },
  async showAssetsList() {
    const {assets} = await request({url:"/wxassets/show_assets",data:{},method:"post"});
    this.setData({
      assetsList: assets
    })
  },
  handleAssetAdd(e){
    wx.navigateTo({
      url: '/pages/assetsAddStep0/assetsAddStep0',
    })
  },
  handleTap(e){
    console.log(e);
    wx.navigateTo({
      url: '/pages/transAdd/transAdd',
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // RefreshFlag
    wx.setStorageSync('flagRefreshAssetsList', true);
    wx.setStorageSync('flagRefreshAccountData', true);

    // 获取缓存中的userInfo
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
      const { code } = await login();
      // 3 发送请求 获取用户的token
      const loginParams={ encryptedData, rawData, iv, signature ,code};
      const {token} = await request({url:"/wxuser/login_init",data:loginParams,method:"post"});
      // 4 把token(即acc_user)存入缓存中
      wx.setStorageSync("token", token);  
    } catch (error){
      console.log(error)
    }
    }
    // 5 初次创建后，再次调用onShow函数，以更新页面
    this.onShow()
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
    if(wx.getStorageSync('flagRefreshAssetsList')){
      this.showAssetsList()
      wx.setStorageSync('flagRefreshAssetsList', false)
    }
    

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
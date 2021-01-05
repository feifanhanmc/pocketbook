// pages/home/home.js
import regeneratorRuntime from '../..//utils/runtime/runtime';
import { request } from "../../utils/request/request.js";
import { login } from "../../utils/asyncwx.js";

Page({

  /**
   * 页面的初始数据
   */
  data: {  
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
    // 获取缓存中的userInfo，若没有用户信息则说明是新用户，跳转至认证界面
    const userInfo = wx.getStorageSync('userInfo') || {}
    if (JSON.stringify(userInfo) === "{}"){
      wx.redirectTo({
        url: '/pages/auth/auth'
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
    if(wx.getStorageSync('flagRefreshAssetsList')){
      this.showAssetsList()
      wx.setStorageSync('flagRefreshAssetsList', false)
    }
    if(wx.getStorageSync('flagRefreshAccountData')){
      // this.showAssetsList()
      wx.setStorageSync('flagRefreshAccountData', false)
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
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
    amt_expend_month: 0,
    amt_income_month: 0,
    amt_budget_surplus: 0,
    amt_asset_net: 0,
    amt_asset_total: 0,
    amt_debt_total: 0,
    amt_budget: 0,  
    amt_budget_temp: "",

    // ViewData
    inputHidden: true,

    // AssetsData
    assetsList: [],

    //ImageData
    imageNoDataHome: "nodata_home",

    // OtherData
    assetIconPath: "/data/icons/asset/",
    nodataIconPath: "/data/icons/nodata/",
  },
  handleSetBudget(e){
    this.setData({
      inputHidden: false
    })
  },
  handleCancelBudget(){
    this.setData({
      inputHidden: true,
      amt_budget_temp: ""
    })
  },
  async handleSubmitBudget(e){
    var amt_budget_temp = parseFloat(this.data.amt_budget_temp)
    if((amt_budget_temp.toString() == "NaN") || (amt_budget_temp==0)){
      wx.showToast({
        title: '输入有误',
        icon: 'none',
        duration: 3000 
      })
      this.setData({
        inputHidden: true,
        amt_budget_temp: ""
      })
    }else{     
      this.setData({
        inputHidden: true,
      })
      const {result} = await request({url:"/wxstatistics/set_budget",data:{'amt_budget': amt_budget_temp},method:"post"});
      if(result){
        this.setData({
          amt_budget: amt_budget_temp
        })
        wx.showToast({
          title: '设置成功',
          icon: 'success',
          duration: 3000
        })
        this.showStatistics()
      }else{
        wx.showToast({
          title: '设置失败，请稍后再试',
          icon: 'none',
          duration: 3000 
        })
      }
    }
  },
  handleInput(e){
    this.setData({
      amt_budget_temp: e.detail.value
    })
  },
  async showAssetsList() {
    const {assets} = await request({url:"/wxassets/show_assets",data:{},method:"post"});
    this.setData({
      assetsList: assets
    })
    wx.setStorageSync('assetsList', assets)
  },
  async showStatistics() {
    const {statistics} = await request({url:"/wxstatistics/show_statistics",data:{},method:"post"});
    if(JSON.stringify(statistics) != '{}'){
      const {amt_expend_month, amt_income_month, amt_budget_surplus, amt_asset_net, amt_asset_total, amt_debt_total, amt_budget} = statistics
      this.setData({
        amt_expend_month,
        amt_income_month,
        amt_budget_surplus,
        amt_asset_net,
        amt_asset_total,
        amt_debt_total,
        amt_budget,  
      })
      wx.setStorageSync('statistics', statistics)
    }
    
  },
  handleAssetAdd(e){
    wx.navigateTo({
      url: '/pages/assetsAdd/assetsAdd',
    })
  },
  handleTap(e){
    wx.navigateTo({
      url: '/pages/transModify/transModify',
    })
  },
  async wxlogin(){
    const {code} = await login();
    const {token} = await request({url:"/wxuser/login_init",data:{'code': code},method:"post"});
    if(token){
      // 把token(即acc_user)存入缓存中
      wx.setStorageSync("token", token);  
    }
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 请求登陆，保存或返回token，完成token-openid的绑定
    if(!wx.getStorageSync('token')){
      this.wxlogin()
    }

    // 参数初始化
    wx.setStorageSync('flagRefreshAssetsList', true)
    wx.setStorageSync('flagRefreshStatisticsData', true)
    wx.setStorageSync('flagRefreshTransData', true)
    wx.setStorageSync('flagRefreshTranstypesData', true)
    wx.setStorageSync('flagRefreshReportData', true)
    wx.setStorageSync('flagRefreshCurrentAssetTransData', true)
    wx.setStorageSync('flagRefreshUserinfo', false)
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
    if(wx.getStorageSync('flagRefreshStatisticsData')){
      this.showStatistics()
      wx.setStorageSync('flagRefreshStatisticsData', false)
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
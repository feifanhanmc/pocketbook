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
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    assetsData: [
    {
      id: 0,
      acc_asset: "asfsdf",
      nam_asset: "农业银行",
      amt_asset: -99.99,
      icon_asset: "/data/icons/asset/bank.png"
    },
    {
      id: 1,
      acc_asset: "sdgdgf",
      nam_asset: "微信钱包",
      amt_asset:200,
      icon_asset: "/data/icons/asset/wechat.png"
    },
    {
      id: 2,
      acc_asset: "rjfgdfs",
      nam_asset: "蚂蚁花呗",
      amt_asset: -100,
      icon_asset: "/data/icons/asset/ant.png"
    }],
    checkedList: [],
    amt_month_out: 70.48,
    amt_month_in: 9.60,
    amt_asset: 80000,
    inputNum: 0,
    testData: "Hello World",
    sex: 0,
    person: {
      age: 11,
      name: "AA",
      nickName: "BB"
    },
    list: [
      {
        id: 0,
        name: "A"
      },
      {
        id: 1,
        name: "B"
      },
      {
        id: 2,
        name: "C"
      }
    ]
  },
  handleTap(e){
    console.log(e);
    wx.navigateTo({
      url: '/pages/transAdd/transAdd',
    })
  },
  handleInput(e){
    console.log(e.detail.value);
    this.setData({
      inputNum: e.detail.value
    })
  },
  handleAssetAdd(e){
    wx.navigateTo({
      url: '/pages/assetsAdd/assetsAdd',
    })
  },
  handleClick(e){
    console.log(e);
    console.log(e.currentTarget.dataset.operation);
    const operation = e.currentTarget.dataset.operation;
    this.setData({
      inputNum: this.data.inputNum*1 + operation*1
    })
  },
  handleChange(e){
    
    const checkedList = e.detail.value;
    console.log(e)
    console.log(checkedList);
    this.setData({
      checkedList
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
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
    
    console.log('showAssets')
    const token = wx.getStorageSync('token')
    // const {token} = await request({url:"/wxuser/login_init",data:loginParams,method:"post"});

  },
  async handleGetUserInfo(e) {
    console.log('handleGetUserInfo');
    console.log(e);
    const userInfo=e.detail.userInfo || {};
    console.log(userInfo)
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
      //  3 发送请求 获取用户的token
      const loginParams={ encryptedData, rawData, iv, signature ,code};
      const {token} = await request({url:"/wxuser/login_init",data:loginParams,method:"post"});
      // 4 把token(即acc_user)存入缓存中
      wx.setStorageSync("token", token);  
    } catch (error){
      console.log(error)
    }
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
// pages/setting/setting.js
import regeneratorRuntime from '../..//utils/runtime/runtime';
import { request } from "../../utils/request/request.js";
import { login } from "../../utils/asyncwx.js";

Page({

  /**
   * 页面的初始数据
   */
  data: {
    // UserData
    nickName: "",
    avatarUrl: "",

    //ImageData
    imageFeedback: "feedback",
    imageLike: "like",
    imageExport: "export",
    imageShare: "share",
    imageBudget: "budget",
    imageAuth: "auth",

    // OtherData
    setIconPath: "/data/icons/set/",
  },
  handleSaveUserinfo(e){
    wx.navigateTo({
      url: '/pages/auth/auth',
    })
  },
  async handleExport(e){
    if(!wx.getStorageSync('userInfo')){
      wx.showToast({
        title: '请先完善信息',
        icon: 'none',
        duration: 3000
      })
    }else{
      const {url} = await request({url:"/wxtrans/export_trans",data:{},method:"post"});
      if(url){
        // 复制到用户剪切板
        wx.setClipboardData({
          data: url,
          success (res) {
            wx.getClipboardData({
              success (res) {
                console.log(res.data) // data
              }
            })
            wx.showToast({
              title: '链接已复制',
              icon: 'success',
              duration: 3000
            })
          }
        })
      }else{
        wx.showToast({
          title: '导出失败，请稍后再试！',
          icon: 'none',
          duration: 3000 
        })
      }
    }
  },
  async loadUserinfo(){
    if((!wx.getStorageSync('userInfo')) && (w.getStorageSync('flagRefreshUserinfo'))){
      const {userInfo} = await request({url:"/wxuser/show_userinfo",data:{},method:"post"});
      if(JSON.stringify(userInfo)!='{}'){
        wx.setStorageSync('userInfo', userInfo)
      }
    }
    const userInfo = wx.getStorageSync('userInfo')
    const {nickName, avatarUrl} = userInfo
    this.setData({userInfo, nickName, avatarUrl})
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

    
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
    // 初始化用户数据
    this.loadUserinfo()
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
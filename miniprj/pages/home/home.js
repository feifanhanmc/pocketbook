// pages/home/home.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    assetsData: [
    {
      id: 0,
      nam_asset: "农业银行信用卡",
      amt_asset: -99.99,
      icon_asset: "https://sun.liuyihua.com/static/icons/icon_daily.png"
    },
    {
      id: 1,
      nam_asset: "中国银行储蓄卡",
      amt_asset:200,
      icon_asset: "https://sun.liuyihua.com/static/icons/icon_business.png"
    },
    {
      id: 2,
      nam_asset: "蚂蚁花呗",
      amt_asset: -100,
      icon_asset: "https://sun.liuyihua.com/static/icons/icon_clothes.png"
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
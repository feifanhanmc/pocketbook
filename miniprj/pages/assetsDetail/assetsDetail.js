// pages/assetsDetail/assetsDetail.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    // AssetData
    acc_asset: "",
    ico_asset: "other",
    nam_asset: "",
    rmk_asset: "",
    tye_asset: "",
    amt_asset: 0.0,

    // StockInfo & FundInfo
    products: [],
    
    // TransData 
    transactions: [],

    // Flag
    isStockFund: false,

    // OtherData
    assetIconPath: "/data/icons/asset/",
  },
  handleAssetsModify(e){
    console.log(e)
    wx.navigateTo({
      url: '/pages/assetsModify/assetsModify',
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
    // 初始化
    let pages = getCurrentPages();
    let currentPage = pages[pages.length - 1];
    let options = currentPage.options;
    const accAssetIndex = parseInt(options.accAssetIndex);
    const {acc_asset, ico_asset, nam_asset, rmk_asset, tye_asset, amt_asset} = wx.getStorageSync('assetsList')[accAssetIndex]
    this.setData({
      acc_asset, 
      ico_asset, 
      nam_asset,
      rmk_asset,
      tye_asset,
      amt_asset
    })

    // 判断是否是股票基金类账户，并进行初始化操作
    if(["股票","基金"].includes(this.data.nam_asset)){
      this.setData({
        isStockFund: true
      })
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
// pages/assetsDetail/assetsDetail.js
import regeneratorRuntime from '../..//utils/runtime/runtime';
import { request } from "../../utils/request/request.js";
import { login } from "../../utils/asyncwx.js";

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
    accAssetIndex: 0,

    // StockInfo & FundInfo
    products: [],
    
    // TransData 
    lastAccAsset: "",
    currentTransList: [],

    // Flag
    isStockFund: false,

    // ImageData
    imageNoDataBill: "nodata_bill2",
        
    // OtherData
    assetIconPath: "/data/icons/asset/",
    tranIconPath: "/data/icons/tran/",
    nodataIconPath: "/data/icons/nodata/",
  },
  handleModifyTrans(e){
    const index = parseInt(e.currentTarget.id)
    const trans = this.data.currentTransList[index]
    const {tye_flow} = trans
    if(tye_flow=='adjust'){
      wx.showToast({
        title: '仅支持长按删除',
        icon: 'none',
        duration: 3000 
      })
    }else{
      wx.navigateTo({
        url: "/pages/transModify/transModify?transStr="+JSON.stringify(trans)
      })
    }   
  },
  handleAssetsModify(e){
    wx.navigateTo({
      url: '/pages/assetsModify/assetsModify?type=modify&accAssetIndex='+this.data.accAssetIndex,
    })
  },
  async showCurrentTransList() {
    // 如果缓存中的流水信息和这次要请求的信息不一致（包括缓存中没有数据），或者有flag标识需要刷新，则请求服务器返回数据；否则从缓存中获取
    if((wx.getStorageSync('lastAccAsset')!=this.data.acc_asset)){
      const {trans} = await request({url:"/wxtrans/show_trans",data:{"acc_asset":this.data.acc_asset},method:"post"});
      wx.setStorageSync('currentTransList', trans)
      wx.setStorageSync('lastAccAsset', this.data.acc_asset)
    }else if(wx.getStorageSync('flagRefreshCurrentAssetTransData')){
      const {trans} = await request({url:"/wxtrans/show_trans",data:{"acc_asset":this.data.acc_asset},method:"post"});
      wx.setStorageSync('currentTransList', trans)
      wx.setStorageSync('lastAccAsset', this.data.acc_asset)
      wx.setStorageSync('flagRefreshCurrentAssetTransData', false)
    }
    this.setData({
      currentTransList: wx.getStorageSync('currentTransList')
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
      amt_asset,
      accAssetIndex
    })

    // 判断是否是股票基金类账户，并进行初始化操作
    if(["股票","基金"].includes(this.data.nam_asset)){
      this.setData({
        isStockFund: true
      })
    }

    // 加载账单流水数据
    this.showCurrentTransList()

    
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
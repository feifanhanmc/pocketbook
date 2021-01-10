// 定义公共的url
var baseUrl="https://sun.liuyihua.com";

// 同时发送异步代码的次数
let ajaxTimes=0;
export const request=(params)=>{
  // 在发送的请求中带上token，即：acc_user
  params.data["token"] = wx.getStorageSync("token");
  
  ajaxTimes++;
  // 显示加载中 效果
  wx.showLoading({
    title: "加载中",
    mask: true
  });
    
  return new Promise((resolve,reject)=>{
    wx.request({
      ...params,
      url:baseUrl+params.url,
      success:(result)=>{
        resolve(result.data.data);
      },
      fail:(err)=>{
        reject(err);
      },
      complete:()=>{
      ajaxTimes--;
      if(ajaxTimes===0){
        //  关闭正在等待的图标
        wx.hideLoading();
      }
      }
    });
  })
}